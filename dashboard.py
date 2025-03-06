import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import HeatMap
sns.set_style("whitegrid")
 
df = pd.read_csv("E:\Laskar Ai\submission\dashboard\main_data.csv")

location_df = df[['year','PM2.5', 'PM10','TEMP','PRES','station']].copy()

locations = {
    "Aotizhongxin": (39.984, 116.407),
    "Changping": (40.218, 116.23),
    "Dingling": (40.292, 116.203),
    "Dongsi": (39.928, 116.417),
    "Guanyuan": (39.933, 116.333),
    "Gucheng": (39.914, 116.184),
    "Huairou": (40.316, 116.632),
    "Nongzhanguan": (39.941, 116.467),
    "Shunyi": (40.128, 116.654),
    "Tiantan": (39.883, 116.407),
    "Wanliu": (39.987, 116.287),
    "Wanshouxigong": (39.878, 116.353),
}

# Tambahkan kolom latitude dan longitude ke DataFrame
location_df["Latitude"] = location_df["station"].map({city: coords[0] for city, coords in locations.items()})
location_df["Longitude"] = location_df["station"].map({city: coords[1] for city, coords in locations.items()})
# Judul aplikasi
st.title("Analisis Kualitas Udara Berdasarkan Tahun")

# Pilih tahun
selected_year = st.selectbox("Pilih Tahun", location_df["year"].unique())

# Filter data berdasarkan tahun yang dipilih
filtered_df = location_df[location_df["year"] == selected_year]

# Hitung rata-rata kualitas udara per kota
avg_air_quality = filtered_df.groupby("station").mean().reset_index()

# Tambahkan koordinat ke hasil rata-rata
avg_air_quality["Latitude"] = avg_air_quality["station"].map({city: coords[0] for city, coords in locations.items()})
avg_air_quality["Longitude"] = avg_air_quality["station"].map({city: coords[1] for city, coords in locations.items()})

st.subheader(f"Grafik Kualitas Udara Tahun {selected_year}")

# Buat satu grafik untuk PM2.5 dan PM10
fig, ax = plt.subplots(figsize=(12, 8))

# Lebar bar
bar_width = 0.35

# Posisi bar
x = np.arange(len(avg_air_quality["station"]))

# Plot PM2.5
ax.bar(x - bar_width/2, avg_air_quality["PM2.5"], width=bar_width, label="PM2.5", color="blue")

# Plot PM10
ax.bar(x + bar_width/2, avg_air_quality["PM10"], width=bar_width, label="PM10", color="red")

# Atur label sumbu X dan Y
ax.set_xlabel("Kota", fontsize=14)
ax.set_ylabel("Konsentrasi (µg/m³)", fontsize=14)
ax.set_title("Tren Kualitas Udara (PM2.5 dan PM10)", fontsize=16)

# Atur label sumbu X (nama kota)
ax.set_xticks(x)
ax.set_xticklabels(avg_air_quality["station"], rotation=45, ha='right', fontsize=12)

# Tambahkan legenda
ax.legend(fontsize=12)

# Tampilkan grafik
st.pyplot(fig)

# Bagi layout menjadi 2 kolom
col1, col2 = st.columns(2)

# Tampilkan tabel rata-rata kualitas udara di kolom pertama
with col1:
    st.subheader(f"Rata-Rata Kualitas Udara Tahun {selected_year}")
    st.write(avg_air_quality)

# Buat peta dan tampilkan di kolom kedua
with col2:
    st.subheader(f"Peta Kualitas Udara Tahun {selected_year}")
    m = folium.Map(location=[39.984, 116.407], zoom_start=10)

    # Tambahkan marker untuk rata-rata kualitas udara
    for index, row in avg_air_quality.iterrows():
        popup_text = f"""
        City: {row['station']}<br>
        Avg PM2.5: {row['PM2.5']:.2f}<br>
        Avg PM10: {row['PM10']:.2f}
        """
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup_text,
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)

    # Tambahkan heatmap untuk PM2.5
    heat_data = [[row['Latitude'], row['Longitude'], row['PM2.5']] for index, row in filtered_df.iterrows()]
    HeatMap(heat_data, name="PM2.5 Heatmap").add_to(m)

    # Tampilkan peta di Streamlit
    folium_static(m, width=500, height=400)

st.subheader(f"Korelasi Kualitas Udara Tahun {selected_year} dengan Suhu dan Tekanan")
correlation_df=location_df[['PM2.5', 'PM10', 'TEMP', 'PRES']].copy()
result=correlation_df.corr(method = "pearson")

fig, ax = plt.subplots(figsize=(12, 8))
# Buat heatmap
sns.heatmap(result, annot=True, cmap='coolwarm', fmt=".3f", linewidths=.5, ax=ax)

# Tampilkan judul dengan ukuran font yang lebih kecil
st.markdown(
    '<h1 style="font-size: 24px;">Heatmap Korelasi antara PM2.5, PM10, TEMP, dan PRES</h1>',
    unsafe_allow_html=True
)
# Tampilkan grafik
st.pyplot(fig)

st.caption('Copyright (c) Leonardo Fajar Mardika 2025')