
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Nassau Candy Shipping Efficiency", layout="wide")

st.title("Factory-to-Customer Shipping Route Efficiency Analysis")

@st.cache_data
def load_data():
    return pd.read_csv("data/nassau_orders.csv", parse_dates=["Order Date", "Ship Date"])

df = load_data()

df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df[df["Lead Time"] >= 0]

st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())
ship_modes = st.sidebar.multiselect("Ship Mode", df["Ship Mode"].unique(), default=df["Ship Mode"].unique())

filtered = df[(df["Region"].isin(regions)) & (df["Ship Mode"].isin(ship_modes))]

st.subheader("Route Efficiency Overview")
route_perf = filtered.groupby(["Factory", "State/Province"]).agg(
    Shipments=("Order ID", "count"),
    Avg_Lead_Time=("Lead Time", "mean")
).reset_index()

st.dataframe(route_perf.sort_values("Avg_Lead_Time"))

st.subheader("Ship Mode Comparison")
st.bar_chart(filtered.groupby("Ship Mode")["Lead Time"].mean())

st.subheader("Raw Data Preview")
st.dataframe(filtered.head())
