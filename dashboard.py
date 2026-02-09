import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# =========================
# LOAD DATA
# =========================
data = pd.read_csv("main_data.csv")

# =========================
# PREPROCESSING
# =========================

# Mapping kondisi cuaca
if data["weathersit"].dtype != "object":
    data["weathersit"] = data["weathersit"].replace({
        1: "Clear",
        2: "Mist",
        3: "Light Snow",
        4: "Heavy Rain"
    })

# Mapping musim
if data["season"].dtype != "object":
    data["season"] = data["season"].replace({
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    })

# Mapping bulan (angka → nama)
bulan_map = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember"
}

data["bulan"] = data["mnth"].map(bulan_map)

# Hapus data kosong
data = data.dropna(subset=["weathersit", "bulan"])

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("Filter Data")

selected_weather = st.sidebar.selectbox(
    "Pilih Kondisi Cuaca",
    ["All", "Clear", "Mist", "Light Snow", "Heavy Rain"]
)

if selected_weather == "All":
    df_filtered = data.copy()
else:
    df_filtered = data[data["weathersit"] == selected_weather]

# =========================
# TITLE
# =========================
st.title("🚲 Dashboard Penyewaan Sepeda")
st.write("Dashboard ini menampilkan analisis sederhana penyewaan sepeda.")

# =========================
# METRICS
# =========================
total_rent = df_filtered["cnt"].sum()
avg_rent = df_filtered["cnt"].mean()

if pd.isna(avg_rent):
    avg_rent = 0

col1, col2 = st.columns(2)
col1.metric("Total Penyewaan", f"{int(total_rent):,}")
col2.metric("Rata-rata Penyewaan", f"{int(avg_rent):,}")

# =========================
# CHART 1 - BULAN (NAMA BULAN)
# =========================
st.subheader("Rata-rata Penyewaan Sepeda per Bulan")

monthly_avg = (
    df_filtered
    .groupby(["mnth", "bulan"])["cnt"]
    .mean()
    .reset_index()
    .sort_values("mnth")
)

if monthly_avg.empty:
    st.warning("Data bulanan kosong.")
else:
    fig1, ax1 = plt.subplots()
    ax1.plot(
        monthly_avg["bulan"],
        monthly_avg["cnt"],
        marker="o"
    )
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("Rata-rata Penyewaan")
    ax1.set_title("Rata-rata Penyewaan per Bulan")
    plt.xticks(rotation=45)
    st.pyplot(fig1)
    plt.close()

# =========================
# CHART 2 - CUACA
# =========================
st.subheader("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")

weather_avg = df_filtered.groupby("weathersit")["cnt"].mean()

if weather_avg.empty:
    st.warning("Data cuaca kosong.")
else:
    fig2, ax2 = plt.subplots()
    ax2.bar(weather_avg.index.astype(str), weather_
