import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("main_data.csv")

# =========================
# PREPROCESSING
# =========================

# Mapping weathersit jika masih numerik
if df["weathersit"].dtype != "object":
    df["weathersit"] = df["weathersit"].map({
        1: "Clear",
        2: "Mist",
        3: "Light Snow",
        4: "Heavy Rain"
    })

# Mapping season jika masih numerik
if df["season"].dtype != "object":
    df["season"] = df["season"].map({
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    })

# Mapping bulan jika masih numerik
if df["month"].dtype != "object":
    df["month"] = df["season"].map({
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
    })
    
# Hapus data kosong
df = df.dropna(subset=["weathersit", "mnth", "cnt"])

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("Filter Data")

# Filter cuaca
weather_option = st.sidebar.selectbox(
    "Pilih Kondisi Cuaca",
    ["All", "Clear", "Mist", "Light Snow", "Heavy Rain"]
)

# Filter bulan (default 6 bulan)
month_range = st.sidebar.slider(
    "Pilih Rentang Bulan",
    min_value=1,
    max_value=12,
    value=(1, 12)
)

# Terapkan filter bulan
filtered_df = df[
    (df["mnth"] >= month_range[0]) &
    (df["mnth"] <= month_range[1])
]

# Terapkan filter cuaca
if weather_option != "All":
    filtered_df = filtered_df[filtered_df["weathersit"] == weather_option]

# =========================
# TITLE
# =========================
st.title("🚲 Dashboard Penyewaan Sepeda")
st.write("Dashboard ini menampilkan analisis sederhana penyewaan sepeda.")

# =========================
# METRICS
# =========================
total_rent = filtered_df["cnt"].sum()
avg_rent = filtered_df["cnt"].mean()

if pd.isna(avg_rent):
    avg_rent = 0

col1, col2 = st.columns(2)
col1.metric("Total Penyewaan", f"{int(total_rent):,}")
col2.metric("Rata-rata Penyewaan", f"{int(avg_rent):,}")

# =========================
# CHART 1 - BULAN
# =========================
st.subheader("Rata-rata Penyewaan Sepeda per Bulan")

monthly_avg = filtered_df.groupby("mnth")["cnt"].mean()

if monthly_avg.empty:
    st.warning("Data bulanan kosong.")
else:
    fig1, ax1 = plt.subplots()
    ax1.plot(monthly_avg.index, monthly_avg.values, marker="o")
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("Rata-rata Penyewaan")
    ax1.set_title("Rata-rata Penyewaan per Bulan")
    st.pyplot(fig1)
    plt.close()

# =========================
# CHART 2 - CUACA
# =========================
st.subheader("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")

weather_avg = filtered_df.groupby("weathersit")["cnt"].mean()

if weather_avg.empty:
    st.warning("Data cuaca kosong.")
else:
    fig2, ax2 = plt.subplots()
    ax2.bar(weather_avg.index.astype(str), weather_avg.values)
    ax2.set_xlabel("Kondisi Cuaca")
    ax2.set_ylabel("Rata-rata Penyewaan")
    ax2.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
    st.pyplot(fig2)
    plt.close()

# =========================
# DATA SAMPLE
# =========================
st.subheader("Contoh Data")
st.dataframe(filtered_df.head())
