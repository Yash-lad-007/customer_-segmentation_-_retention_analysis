import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retail Analytics", layout="wide")

st.title("📊 Retail Analytics Dashboard")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
else:
    df = pd.read_csv("online_retail.csv", encoding="ISO-8859-1")

# -----------------------------
# Data Cleaning
# -----------------------------
df.dropna(subset=["CustomerID"], inplace=True)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Country",
    df["Country"].unique(),
    default=df["Country"].unique()[:5]
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df["InvoiceDate"].min(), df["InvoiceDate"].max()]
)

filtered = df[
    (df["Country"].isin(country)) &
    (df["InvoiceDate"].dt.date >= date_range[0]) &
    (df["InvoiceDate"].dt.date <= date_range[1])
]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Revenue", f"${filtered['Revenue'].sum():,.0f}")
c2.metric("Orders", filtered["InvoiceNo"].nunique())
c3.metric("Customers", filtered["CustomerID"].nunique())
c4.metric("Avg Order Value",
          f"${filtered['Revenue'].sum()/filtered['InvoiceNo'].nunique():.2f}")

# -----------------------------
# Sales Trend
# -----------------------------
st.subheader("Revenue Over Time")

time_sales = filtered.groupby(
    filtered["InvoiceDate"].dt.to_period("M")
)["Revenue"].sum()

fig, ax = plt.subplots()
time_sales.plot(ax=ax)
st.pyplot(fig)

# -----------------------------
# Top Products
# -----------------------------
st.subheader("Top Products")

top_products = (
    filtered.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots()
top_products.plot(kind="barh", ax=ax2)
st.pyplot(fig2)

# -----------------------------
# RFM Segmentation
# -----------------------------
st.subheader("Customer Segmentation (RFM)")

snapshot_date = filtered["InvoiceDate"].max()

rfm = filtered.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
    "InvoiceNo": "nunique",
    "Revenue": "sum"
})

rfm.columns = ["Recency", "Frequency", "Monetary"]

st.dataframe(rfm.head())

# -----------------------------
# Download Data
# -----------------------------
st.download_button(
    "Download Filtered Data",
    filtered.to_csv(index=False),
    "filtered_data.csv"
)

# -----------------------------
# Raw Data Toggle
# -----------------------------
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered)

st.success("Dashboard Ready")
