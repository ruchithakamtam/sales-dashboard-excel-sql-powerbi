import pandas as pd
import streamlit as st
import plotly.express as px

st.title("📊 Sales Data Dashboard")

df = pd.read_csv("sales_data.csv", parse_dates=["Date"])

region = st.sidebar.multiselect("Select Region", options=df["Region"].unique(), default=df["Region"].unique())
salesperson = st.sidebar.multiselect("Select Salesperson", options=df["SalesPerson"].unique(), default=df["SalesPerson"].unique())

filtered_df = df[(df["Region"].isin(region)) & (df["SalesPerson"].isin(salesperson))]

total_sales = filtered_df["TotalSales"].sum()
total_units = filtered_df["UnitsSold"].sum()
unique_products = filtered_df["Product"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("📦 Units Sold", total_units)
col3.metric("🛍️ Products", unique_products)

st.subheader("Sales by Region")
fig_region = px.bar(filtered_df.groupby("Region")["TotalSales"].sum().reset_index(),
                    x="Region", y="TotalSales", color="Region", title="Sales by Region")
st.plotly_chart(fig_region)

st.subheader("Sales Over Time")
fig_time = px.line(filtered_df, x="Date", y="TotalSales", title="Sales Over Time")
st.plotly_chart(fig_time)

st.subheader("Product-wise Sales")
fig_product = px.pie(filtered_df, names="Product", values="TotalSales", title="Sales by Product")
st.plotly_chart(fig_product)

st.dataframe(filtered_df)
