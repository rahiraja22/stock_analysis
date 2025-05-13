
import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt

# MySQL connection setup
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Rajarahi@22',
    db='newdatabase'
)

# Query top 10 most volatile stocks

query = "SELECT * FROM volatility_analysis"


df = pd.read_sql(query, connection)

# Close connection
connection.close()

# Streamlit visualization
st.title("📊 Top 10 Most Volatile Stocks")

# Convert volatility column to numeric if needed
df['Volatility'] = pd.to_numeric(df['Volatility'], errors='coerce').head(10)

# Plot bar chart
fig, ax = plt.subplots(figsize=(12,6))
ax.bar(df['Ticker'], df['Volatility'], color='orange')
ax.set_xlabel("Stock Ticker")
ax.set_ylabel("Volatility (Std Dev)")
ax.set_title("Top 10 Most Volatile Stocks")

st.pyplot(fig)




connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Rajarahi@22',
    db='newdatabase'
)

# 📥 Read cumulative return data
query = "SELECT * FROM cumulative_return"
df = pd.read_sql(query, connection)
connection.close()

# Clean the data
df['date'] = pd.to_datetime(df['date'])
df['cumulative_return'] = pd.to_numeric(df['cumulative_return'], errors='coerce')

# Get top 5 performing tickers at year end
latest_date = df['date'].max()
top5 = df[df['date'] == latest_date].sort_values(by='cumulative_return', ascending=False).head(5)
top5_tickers = top5['Ticker'].tolist()

# Filter data for only those tickers
df_top5 = df[df['Ticker'].isin(top5_tickers)]

# Line chart
st.title("📈 Top 5 Performing Stocks - Line Chart")

for ticker in top5_tickers:
    stock_data = df_top5[df_top5['Ticker'] == ticker]
    st.line_chart(stock_data.set_index('date')['cumulative_return'], height=300, use_container_width=True)
    st.caption(f"📊 {ticker}")





connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Rajarahi@22',
    db='newdatabase'
)

# 📥 Read cumulative return data
query = "SELECT * FROM sector_performance"
df = pd.read_sql(query, connection)
connection.close()


# Clean columns
df.columns = df.columns.str.strip()
df['Yearly_Return'] = pd.to_numeric(df['Yearly_Return'], errors='coerce')


# Dropdown to select sector
sectors = df['sector'].unique().tolist()
selected_sector = st.selectbox("📂 Choose a Sector", sectors)

# Filter data
filtered_df = df[df['sector'] == selected_sector]

# Set title
st.subheader("📈 Ticker-wise Yearly Return in '{selected_sector}' Sector")

# ✅ Loop through each ticker and show return
for index, row in filtered_df.iterrows():
    ticker = row['Ticker']
    yearly_return = row['Yearly_Return']


    unique_tickers = filtered_df['Ticker'].unique().tolist()
for ticker in unique_tickers:
    st.write(f"✅ {ticker}")    
    
    
    #st.write("📌 **{Ticker}** ({year}) ➤ {yearly_return:.2f}%")

    # Optional: Mini bar chart for each ticker
    fig, ax = plt.subplots(figsize=(3, 0.4))
    ax.barh([ticker], [yearly_return], color='skyblue')
    ax.set_xlim([0, max(filtered_df['Yearly_Return']) * 1.1])  # scale
    ax.set_xlabel("Return (%)")
    ax.set_yticks([])  # Hide y ticks
    st.pyplot(fig)


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Rajarahi@22',
    db='newdatabase'
)

import seaborn as sns
#  Read cumulative return data
query = "SELECT * FROM stock_correlation"

df = pd.read_sql(query, connection)
connection.close()
df.set_index(df.columns[0], inplace=True)
# Convert all values to float (if any stray string exit)
df = df.apply(pd.to_numeric, errors='coerce')

# Plot the heatmap
st.title("📉 Stock Price Correlation Heatmap")

st.subheader("🔍 Correlation Matrix Preview")


st.subheader("🔥 Heatmap Visualization")

    # Plotting
fig, ax = plt.subplots(figsize=(16, 18))  # Adjust for large matrix

    # Create the heatmap
sns.heatmap(
        df,
        annot=False,
        cmap="coolwarm",
        linewidths=0.3,
        xticklabels=True,
        yticklabels=True,
        square=True,
        cbar_kws={'shrink': 0.5}
    )

    # Rotate labels for readability
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=8)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)


plt.tight_layout()

st.pyplot(plt)


#use slicing
df_10 = df.iloc[:10, :10]

# 🔥 Displaying 10x10 correlation matrix
st.subheader("🔟 First 10 Tickers Correlation Matrix")
#st.dataframe(df_10)

# 📊 Plot the 10x10 heatmap
st.subheader("📌 Heatmap for First 10 Tickers")

fig, ax = plt.subplots(figsize=(10, 8))  # Smaller figure since only 10x10

sns.heatmap(
    df_10,
    annot=True,  # ✅ values show panna
    cmap="coolwarm",
    linewidths=0.3,
    xticklabels=df_10.columns,
    yticklabels=df_10.index,
    square=True,
    cbar_kws={'shrink': 0.5}
)

# ✅ Rotate labels for readability
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

plt.tight_layout()
st.pyplot(fig)




connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Rajarahi@22',
    db='newdatabase'
)
#  Load monthly return data into a DataFrame
query = "SELECT * FROM monthly_top_5"
df = pd.read_sql(query, connection)

# Streamlit app title
st.title("📊 Monthly Top 5 Gainers and Losers Dashboard")



# Loop through each month
for month in range(1, 13):
    st.subheader(f"📅 Month {month}")


    df = pd.read_sql(query, connection)

    if df.empty:
        st.write("No data available for this month.")
        continue

    gainers = df[df['Type'] == 'Top Gainer'].head(5)
    losers = df[df['Type'] == 'Top Loser'].head(5)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(gainers['Ticker'], gainers['return'], color='green', label='Top 5 Gainers')
    ax.bar(losers['Ticker'], losers['return'], color='red', label='Top 5 Losers')

    ax.set_ylabel("Return (%)")
    ax.set_title(f"Top Gainers and Losers - Month {month}")
    ax.legend()

    st.pyplot(fig)



