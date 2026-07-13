"""
Sales Data Analytics Dashboard
--------------------------------
A Streamlit dashboard to analyze sales trends, profits, top-selling products,
and regional performance.

Run locally:
    streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------
# Page config
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------
@st.cache_data
def load_data(path: str = "data/sales_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Order_Date"])
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b %Y")
    df["Profit_Margin"] = (df["Profit"] / df["Sales"] * 100).round(2)
    return df


df = load_data()

# ---------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------
st.sidebar.title("🔎 Filters")

min_date, max_date = df["Order_Date"].min(), df["Order_Date"].max()
date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

regions = st.sidebar.multiselect(
    "Region", options=sorted(df["Region"].unique()), default=sorted(df["Region"].unique())
)
categories = st.sidebar.multiselect(
    "Category", options=sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
)
segments = st.sidebar.multiselect(
    "Customer segment",
    options=sorted(df["Customer_Segment"].unique()),
    default=sorted(df["Customer_Segment"].unique()),
)

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date, end_date = min_date, max_date

mask = (
    (df["Order_Date"] >= start_date)
    & (df["Order_Date"] <= end_date)
    & (df["Region"].isin(regions))
    & (df["Category"].isin(categories))
    & (df["Customer_Segment"].isin(segments))
)
fdf = df.loc[mask].copy()

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(fdf):,}** of {len(df):,} orders")

# ---------------------------------------------------------------
# Header
# ---------------------------------------------------------------
st.title("📊 Sales Data Analytics Dashboard")
st.caption("Sales trends, profitability, top products, and regional performance at a glance.")

if fdf.empty:
    st.warning("No data matches the selected filters. Please broaden your filter selection.")
    st.stop()

# ---------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------
total_sales = fdf["Sales"].sum()
total_profit = fdf["Profit"].sum()
total_orders = fdf["Order_ID"].nunique()
avg_order_value = total_sales / total_orders if total_orders else 0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Sales", f"${total_sales:,.0f}")
k2.metric("Total Profit", f"${total_profit:,.0f}")
k3.metric("Total Orders", f"{total_orders:,}")
k4.metric("Avg Order Value", f"${avg_order_value:,.2f}")
k5.metric("Profit Margin", f"{profit_margin:.1f}%")

st.markdown("---")

# ---------------------------------------------------------------
# Row 1: Sales trend + Category split
# ---------------------------------------------------------------
c1, c2 = st.columns((2, 1))

with c1:
    st.subheader("📈 Monthly Sales & Profit Trend")
    trend = (
        fdf.groupby("Month", as_index=False)[["Sales", "Profit"]]
        .sum()
        .sort_values("Month")
    )
    fig_trend = px.line(
        trend, x="Month", y=["Sales", "Profit"], markers=True,
        labels={"value": "Amount ($)", "Month": "Month", "variable": "Metric"},
    )
    fig_trend.update_layout(legend_title_text="", hovermode="x unified")
    st.plotly_chart(fig_trend, use_container_width=True)

with c2:
    st.subheader("🧩 Sales by Category")
    cat = fdf.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_cat = px.pie(cat, names="Category", values="Sales", hole=0.45)
    fig_cat.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_cat, use_container_width=True)

# ---------------------------------------------------------------
# Row 2: Top products + Regional performance
# ---------------------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.subheader("🏆 Top 10 Products by Sales")
    top_products = (
        fdf.groupby("Product", as_index=False)[["Sales", "Profit"]]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    fig_top = px.bar(
        top_products.sort_values("Sales"),
        x="Sales", y="Product", orientation="h",
        color="Profit", color_continuous_scale="Blues",
        labels={"Sales": "Sales ($)"},
    )
    st.plotly_chart(fig_top, use_container_width=True)

with c4:
    st.subheader("🗺️ Regional Performance")
    region_perf = fdf.groupby("Region", as_index=False)[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False)
    fig_region = px.bar(
        region_perf, x="Region", y=["Sales", "Profit"], barmode="group",
        labels={"value": "Amount ($)", "variable": "Metric"},
    )
    fig_region.update_layout(legend_title_text="")
    st.plotly_chart(fig_region, use_container_width=True)

# ---------------------------------------------------------------
# Row 3: Profit margin by category + Customer segment
# ---------------------------------------------------------------
c5, c6 = st.columns(2)

with c5:
    st.subheader("💰 Profit Margin by Category")
    margin = fdf.groupby("Category", as_index=False).apply(
        lambda g: pd.Series({"Profit_Margin": g["Profit"].sum() / g["Sales"].sum() * 100})
    ).sort_values("Profit_Margin", ascending=False)
    fig_margin = px.bar(margin, x="Category", y="Profit_Margin", color="Profit_Margin",
                         color_continuous_scale="Greens", labels={"Profit_Margin": "Margin (%)"})
    st.plotly_chart(fig_margin, use_container_width=True)

with c6:
    st.subheader("👥 Sales by Customer Segment")
    seg = fdf.groupby("Customer_Segment", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_seg = px.bar(seg, x="Customer_Segment", y="Sales", color="Customer_Segment",
                      labels={"Sales": "Sales ($)"})
    fig_seg.update_layout(showlegend=False)
    st.plotly_chart(fig_seg, use_container_width=True)

# ---------------------------------------------------------------
# Raw data explorer
# ---------------------------------------------------------------
st.markdown("---")
with st.expander("🔍 View filtered raw data"):
    st.dataframe(fdf.sort_values("Order_Date", ascending=False), use_container_width=True)
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", data=csv, file_name="filtered_sales_data.csv", mime="text/csv")

st.markdown("---")
st.caption("Built with Streamlit · Sample data is synthetically generated for demonstration purposes.")
