import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# =========================
# LOAD DATASET
# =========================

DATA_FILE = "vgsales.csv"

if not os.path.exists(DATA_FILE):
    messagebox.showerror("Error", f"{DATA_FILE} not found in folder!")
    exit()

df = pd.read_csv(DATA_FILE)
df.dropna(inplace=True)

# =========================
# ANALYSIS FUNCTIONS
# =========================

def show_top_games():
    top = df.sort_values(by="Global_Sales", ascending=False).head(10)

    plt.figure(figsize=(10, 5))
    plt.bar(top["Name"], top["Global_Sales"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 Games by Global Sales")
    plt.xlabel("Game Name")
    plt.ylabel("Sales (Millions)")
    plt.tight_layout()
    plt.show()


def genre_analysis():
    data = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)

    plt.figure(figsize=(8, 5))
    data.plot(kind="bar", color="skyblue")
    plt.title("Sales by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Global Sales")
    plt.tight_layout()
    plt.show()


def platform_analysis():
    data = df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).head(10)

    plt.figure(figsize=(8, 5))
    data.plot(kind="bar", color="orange")
    plt.title("Top Platforms by Sales")
    plt.xlabel("Platform")
    plt.ylabel("Global Sales")
    plt.tight_layout()
    plt.show()


def stats_summary():
    total_sales = np.sum(df["Global_Sales"])
    avg_sales = np.mean(df["Global_Sales"])
    best_game = df.loc[df["Global_Sales"].idxmax(), "Name"]

    messagebox.showinfo(
        "Stats Summary",
        f"Total Sales: {total_sales:.2f}M\n"
        f"Average Sales: {avg_sales:.2f}M\n"
        f"Best Game: {best_game}"
    )


# =========================
# STREAMLIT LAUNCHER
# =========================

def open_streamlit():
    messagebox.showinfo("Launching", "Opening Streamlit Dashboard...")

    with open("dashboard.py", "w", encoding="utf-8") as f:
        f.write("""
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
""")

    import sys
    
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "dashboard.py"])

# =========================
# TKINTER UI
# =========================

root = tk.Tk()
root.title("Game Sales Analytics System")
root.geometry("1200x700")
root.resizable(False, False)

title = tk.Label(root, text="🎮 Game Sales Analytics Dashboard", font=("Arial", 14, "bold"))
title.pack(pady=15)

btn1 = tk.Button(root, text="Top 10 Games", width=30, command=show_top_games)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Genre Analysis", width=30, command=genre_analysis)
btn2.pack(pady=5)

btn3 = tk.Button(root, text="Platform Analysis", width=30, command=platform_analysis)
btn3.pack(pady=5)

btn4 = tk.Button(root, text="Stats Summary", width=30, command=stats_summary)
btn4.pack(pady=5)

btn5 = tk.Button(root, text="Open Streamlit Dashboard", width=30, command=open_streamlit)
btn5.pack(pady=10)

btn6 = tk.Button(root, text="Exit", width=30, command=root.quit)
btn6.pack(pady=5)

root.mainloop()