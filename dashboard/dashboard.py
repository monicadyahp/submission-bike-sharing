import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set(style='dark')

# --- LOAD DATA ---
script_dir = os.path.dirname(os.path.abspath(__file__))
day_csv_path = os.path.join(script_dir, 'day.csv')
hour_csv_path = os.path.join(script_dir, 'hour.csv')

day_df = pd.read_csv(day_csv_path)
hour_df = pd.read_csv(hour_csv_path)

# --- CLEANING DATA ---
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_label'] = day_df['season'].map(season_map)

# --- SIDEBAR FILTER ---
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png")
    
    # Input rentang waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date, 
        max_value=max_date, 
        value=[min_date, max_date]
    )

# --- FILTER DATA UTAMA (FIX: Filter KEDUANYA) ---
# 1. Filter data harian
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# 2. Filter data jam (INI YANG DIMINTA REVIEWER)
main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                       (hour_df["dteday"] <= str(end_date))]

# --- DASHBOARD PAGE ---
st.header('Bike Sharing Dashboard :sparkles:')

# Metric
total_orders = main_df.cnt.sum()
st.metric("Total Sharing Bike", value=f"{total_orders:,}")

# --- VISUALISASI 1: MUSIM (Dengan Highlight Warna) ---
st.subheader("Rata-rata Penyewaan per Musim")

# Hitung rata-rata
season_avg = main_df.groupby('season_label')['cnt'].mean().reset_index().sort_values("cnt", ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))

# FIX: Membuat palet warna custom (Bar pertama Biru, sisanya Abu-abu)
# Ini menjawab "Prinsip Desain Visualisasi"
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x='season_label', 
    y='cnt', 
    data=season_avg, 
    palette=colors,  # Pakai warna custom tadi
    ax=ax
)

ax.set_title("Musim Gugur (Fall) Memiliki Rata-rata Penyewaan Tertinggi", fontsize=15)
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)

# Tambah label angka
for i in ax.containers:
    ax.bar_label(i, fmt='%.0f', padding=5, fontsize=10)

st.pyplot(fig)

# --- VISUALISASI 2: JAM SIBUK (Menggunakan Data Terfilter) ---
st.subheader("Pola Penyewaan per Jam")

# FIX: Gunakan main_hour_df (yang sudah difilter tanggalnya)
hour_avg = main_hour_df.groupby('hr')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x='hr', 
    y='cnt', 
    data=hour_avg, 
    marker='o', 
    color='#72BCD4', # Pakai warna biru yang sama dengan grafik atas
    ax=ax2
)

ax2.set_title("Pola Jam Sibuk: Puncak pada Pagi dan Sore Hari", fontsize=15)
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.set_xlabel("Jam (00:00 - 23:00)")
ax2.set_xticks(range(0, 24))
ax2.grid(True)

st.pyplot(fig2)

st.caption('Copyright (c) Monica Dyah 2026')