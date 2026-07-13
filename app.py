import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# ---------------------------------------------------------------
# Page config
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------------
# Load Data
# ---------------------------------------------------------------
@st.cache_data
def load_data():

    csv_path = Path(__file__).parent / "data" / "sales_data.csv"

    if not csv_path.exists():
        st.error(f"CSV file not found:\n{csv_path}")
        st.stop()

    df = pd.read_csv(csv_path)

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b %Y")

    df["Profit_Margin"] = (
        df["Profit"] / df["Sales"] * 100
    ).round(2)

    return df


df = load_data()

# ---------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------
st.sidebar.title("🔍 Filters")

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

segments = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["Customer_Segment"].unique()),
    default=sorted(df["Customer_Segment"].unique())
)

min_date = df["Order_Date"].min()
max_date = df["Order_Date"].max()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date)
)

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
else:
    start_date = min_date
    end_date = max_date

filtered = df[
    (df["Order_Date"] >= start_date) &
    (df["Order_Date"] <= end_date) &
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Customer_Segment"].isin(segments))
]

if filtered.empty:
    st.warning("No data found.")
    st.stop()

# ---------------------------------------------------------------
# Title
# ---------------------------------------------------------------
st.title("📊 Sales Analytics Dashboard")

# ---------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------
sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order_ID"].nunique()

avg = sales / orders if orders else 0
margin = (profit / sales * 100) if sales else 0

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Sales", f"${sales:,.0f}")
c2.metric("Profit", f"${profit:,.0f}")
c3.metric("Orders", orders)
c4.metric("Average Order", f"${avg:,.2f}")
c5.metric("Margin", f"{margin:.2f}%")

st.divider()

# ---------------------------------------------------------------
# Monthly Trend
# ---------------------------------------------------------------
left, right = st.columns([2, 1])

with left:

    trend = filtered.groupby("Month")[["Sales", "Profit"]].sum().reset_index()

    fig = px.line(
        trend,
        x="Month",
        y=["Sales", "Profit"],
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    cat = filtered.groupby("Category")["Sales"].sum().reset_index()

    fig = px.pie(
        cat,
        names="Category",
        values="Sales",
        hole=.4
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# Top Products
# ---------------------------------------------------------------
left, right = st.columns(2)

with left:

    top = (
        filtered.groupby("Product")[["Sales", "Profit"]]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top.sort_values("Sales"),
        x="Sales",
        y="Product",
        orientation="h",
        color="Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    region = (
        filtered.groupby("Region")[["Sales", "Profit"]]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region,
        x="Region",
        y=["Sales", "Profit"],
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# Profit Margin
# ---------------------------------------------------------------
left, right = st.columns(2)

with left:

    margin_df = (
        filtered.groupby("Category")
        .agg({"Sales":"sum","Profit":"sum"})
        .reset_index()
    )

    margin_df["Profit_Margin"] = (
        margin_df["Profit"] /
        margin_df["Sales"] * 100
    )

    fig = px.bar(
        margin_df,
        x="Category",
        y="Profit_Margin",
        color="Profit_Margin"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    seg = (
        filtered.groupby("Customer_Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        seg,
        x="Customer_Segment",
        y="Sales",
        color="Customer_Segment"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# Data Table
# ---------------------------------------------------------------
st.divider()

with st.expander("View Raw Data"):

    st.dataframe(filtered, use_container_width=True)

    st.download_button(
        "Download CSV",
        filtered.to_csv(index=False),
        "filtered_sales_data.csv",
        "text/csv"
    )

st.caption("Built with Streamlit")
