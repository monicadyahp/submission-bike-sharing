import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set style
sns.set(style='dark')

# Load data (pastikan file day.csv satu folder dengan file ini saat dijalankan)
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Helper function
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    return daily_orders_df

# Convert datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Sidebar
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan (opsional)
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan input tanggal
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# Main Page
st.header('Bike Sharing Dashboard :sparkles:')

# Metric Total Penyewaan
total_orders = main_df.cnt.sum()
st.metric("Total Sharing Bike", value=total_orders)

# Plot Musim
st.subheader("Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="cnt", 
    x="season",
    data=main_df.sort_values(by="season", ascending=False),
    palette="viridis",
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

# Plot Cuaca
st.subheader("Penyewaan Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="cnt", 
    x="weathersit",
    data=main_df.sort_values(by="weathersit", ascending=False),
    palette="coolwarm",
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

st.caption('Copyright (c) Monica Dyah 2026')