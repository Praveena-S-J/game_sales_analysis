
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Game Sales Dashboard", layout="wide")

df = pd.read_csv("vgsales.csv")

st.title("🎮 Advanced Game Sales Analytics Dashboard")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔎 Filters")

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

genre_filter = st.sidebar.multiselect(
    "Select Genre",
    df["Genre"].unique(),
    default=df["Genre"].unique()
)

platform_filter = st.sidebar.multiselect(
    "Select Platform",
    df["Platform"].unique(),
    default=df["Platform"].unique()
)

# Apply filters
filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1]) &
    (df["Genre"].isin(genre_filter)) &
    (df["Platform"].isin(platform_filter))
]

# =========================
# KPI METRICS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("🎮 Total Games", len(filtered_df))
col2.metric("🌍 Total Sales", round(filtered_df["Global_Sales"].sum(), 2))
col3.metric("📊 Avg Sales", round(filtered_df["Global_Sales"].mean(), 2))
col4.metric("🏆 Best Game", filtered_df.loc[filtered_df["Global_Sales"].idxmax(), "Name"] if len(filtered_df) > 0 else "N/A")

st.divider()

# =========================
# TOP 10 GAMES
# =========================
st.subheader("🏆 Top 10 Games")

top_games = filtered_df.sort_values(by="Global_Sales", ascending=False).head(10)

st.dataframe(top_games[["Name", "Platform", "Genre", "Year", "Global_Sales"]])

st.bar_chart(top_games.set_index("Name")["Global_Sales"])

st.divider()

# =========================
# GENRE ANALYSIS
# =========================
st.subheader("🎯 Genre Performance")

genre_data = filtered_df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)

st.bar_chart(genre_data)

st.divider()

# =========================
# PLATFORM ANALYSIS
# =========================
st.subheader("🎮 Platform Performance")

platform_data = filtered_df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).head(10)

st.bar_chart(platform_data)

st.divider()

# =========================
# YEARLY TREND
# =========================
st.subheader("📈 Yearly Sales Trend")

yearly_data = filtered_df.groupby("Year")["Global_Sales"].sum()

st.line_chart(yearly_data)

st.divider()

# =========================
# REGION ANALYSIS
# =========================
st.subheader("🌍 Regional Sales Comparison")

region_data = pd.DataFrame({
    "NA": [filtered_df["NA_Sales"].sum()],
    "EU": [filtered_df["EU_Sales"].sum()],
    "JP": [filtered_df["JP_Sales"].sum()],
    "Other": [filtered_df["Other_Sales"].sum()]
})

st.bar_chart(region_data.T)

st.divider()

# =========================
# RAW DATA VIEW
# =========================
st.subheader("📄 Filtered Dataset")
st.dataframe(filtered_df)
