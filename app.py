import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Online Retail Dashboard",
    layout="wide"
)

st.title("📊 Online Retail Analytics App")

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("online_retail.csv", encoding="ISO-8859-1")
    return df

df = load_data()

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Country",
    options=df["Country"].dropna().unique(),
    default=df["Country"].dropna().unique()[:5]
)

filtered_df = df[df["Country"].isin(countries)]

# ---------------------------
# Data Preview
# ---------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

# ---------------------------
# Basic Metrics
# ---------------------------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rows", len(filtered_df))
col2.metric("Unique Customers", filtered_df["CustomerID"].nunique())
col3.metric("Unique Products", filtered_df["StockCode"].nunique())

# ---------------------------
# Sales Analysis
# ---------------------------
st.subheader("Sales by Country")

sales = (
    filtered_df
    .groupby("Country")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots()
sales.plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---------------------------
# Optional Raw Data
# ---------------------------
if st.checkbox("Show Raw Data"):
    st.write(filtered_df)

st.success("App running successfully!")
