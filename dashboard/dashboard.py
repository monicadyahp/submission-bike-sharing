import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set(style='dark')

script_dir = os.path.dirname(os.path.abspath(__file__))
day_csv_path = os.path.join(script_dir, 'day.csv')
hour_csv_path = os.path.join(script_dir, 'hour.csv')

day_df = pd.read_csv(day_csv_path)
hour_df = pd.read_csv(hour_csv_path)

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_label'] = day_df['season'].map(season_map)

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

st.header('Bike Sharing Dashboard :sparkles:')

total_orders = main_df.cnt.sum()
st.metric("Total Sharing Bike", value=f"{total_orders:,}")

st.subheader("Rata-rata Penyewaan per Musim")

season_avg = main_df.groupby('season_label')['cnt'].mean().reset_index().sort_values("cnt", ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='season_label',
    y='cnt',
    data=season_avg,
    palette='viridis',
    ax=ax
)
ax.set_title("Rata-rata Penyewaan Sepeda per Musim", fontsize=15)
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xlabel("Musim")

for i in ax.containers:
    ax.bar_label(i, fmt='%.0f', padding=5, fontsize=10)

st.pyplot(fig)

st.subheader("Pola Penyewaan per Jam")

hour_avg = hour_df.groupby('hr')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x='hr',
    y='cnt',
    data=hour_avg,
    marker='o',
    color='blue',
    ax=ax2
)
ax2.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=15)
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.set_xlabel("Jam (00:00 - 23:00)")
ax2.set_xticks(range(0, 24))
ax2.grid(True)

st.pyplot(fig2)

st.caption('Copyright (c) Monica Dyah 2026')