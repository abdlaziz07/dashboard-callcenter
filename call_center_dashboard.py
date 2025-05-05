import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup
st.set_page_config(page_title="📞 Call Center Dashboard", layout="wide")
st.title("📞 Dashboard Analisis Call Center")

# Load Data
df = pd.read_csv("cleaned_call_center.csv", parse_dates=['Call_timestamp'])

# Feature Engineering
df['Month'] = df['Call_timestamp'].dt.to_period('M').astype(str)
df['Day_of_week'] = df['Call_timestamp'].dt.day_name()
df['Hour'] = df['Call_timestamp'].dt.hour

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
channel_options = st.sidebar.multiselect("Pilih Channel:", options=df['Channel'].unique(), default=df['Channel'].unique())
date_range = st.sidebar.date_input("Pilih Rentang Tanggal:", [df['Call_timestamp'].min(), df['Call_timestamp'].max()])
filtered_df = df[
    (df['Channel'].isin(channel_options)) &
    (df['Call_timestamp'].dt.date >= date_range[0]) &
    (df['Call_timestamp'].dt.date <= date_range[1])
]

# === RINGKASAN DATA ===
st.subheader("📊 Ringkasan Statistik")
st.dataframe(filtered_df.describe())

# === DISTRIBUSI CSAT SCORE ===
st.subheader("🎯 Distribusi CSAT Score")
fig1, ax1 = plt.subplots()
sns.countplot(data=filtered_df, x='Csat_score', palette='Set2', ax=ax1)
ax1.set_title('Distribusi CSAT Score')
st.pyplot(fig1)

# === JUMLAH PANGGILAN PER BULAN ===
st.subheader("📆 Jumlah Panggilan per Bulan")
monthly_calls = filtered_df.groupby('Month').size()
st.bar_chart(monthly_calls)

# === JUMLAH PANGGILAN PER HARI ===
st.subheader("🗓️ Jumlah Panggilan per Hari dalam Seminggu")
order_hari = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
fig2, ax2 = plt.subplots()
sns.countplot(data=filtered_df, x='Day_of_week', order=order_hari, palette='muted', ax=ax2)
ax2.set_title("Jumlah Panggilan per Hari")
st.pyplot(fig2)

# === DISTRIBUSI PANGGILAN BERDASARKAN JAM ===
st.subheader("⏰ Distribusi Panggilan per Jam")
fig3, ax3 = plt.subplots()
sns.histplot(data=filtered_df, x='Hour', bins=24, kde=True, color='orange', ax=ax3)
ax3.set_title("Distribusi Panggilan per Jam")
st.pyplot(fig3)

# === JUMLAH PANGGILAN BERDASARKAN CHANNEL ===
st.subheader("📡 Jumlah Panggilan per Channel")
fig4, ax4 = plt.subplots()
sns.countplot(data=filtered_df, x='Channel', palette='Set3', ax=ax4)
ax4.set_title("Panggilan per Channel")
st.pyplot(fig4)

# === RATA-RATA CSAT SCORE PER CHANNEL ===
st.subheader("⭐ Rata-rata CSAT Score per Channel")
fig5, ax5 = plt.subplots()
sns.barplot(data=filtered_df, x='Channel', y='Csat_score', ci=None, palette='viridis', ax=ax5)
ax5.set_title("Rata-rata CSAT per Channel")
st.pyplot(fig5)

# === DISTRIBUSI SENTIMEN ===
st.subheader("💬 Distribusi Sentimen")
fig6, ax6 = plt.subplots()
sns.countplot(data=filtered_df, x='Sentiment', palette='RdYlGn', ax=ax6)
ax6.set_title("Distribusi Sentimen Panggilan")
st.pyplot(fig6)

# === DURASI PANGGILAN vs CSAT ===
st.subheader("📞 Durasi Panggilan vs CSAT Score")
fig7, ax7 = plt.subplots()
sns.boxplot(data=filtered_df, x='Csat_score', y='Call duration in minutes', palette='pastel', ax=ax7)
ax7.set_title("Durasi vs CSAT")
st.pyplot(fig7)

# === ALASAN PANGGILAN TERBANYAK ===
st.subheader("📋 10 Alasan Panggilan Terbanyak")
top_reasons = filtered_df['Reason'].value_counts().nlargest(10)
fig8, ax8 = plt.subplots()
sns.barplot(x=top_reasons.values, y=top_reasons.index, palette='coolwarm', ax=ax8)
ax8.set_title("Top 10 Alasan Panggilan")
st.pyplot(fig8)

# === TOP 10 KOTA ===
st.subheader("📍 10 Kota dengan Jumlah Panggilan Terbanyak")
top_cities = filtered_df['City'].value_counts().nlargest(10)
fig9, ax9 = plt.subplots()
sns.barplot(x=top_cities.values, y=top_cities.index, palette='viridis', ax=ax9)
ax9.set_title("Top 10 Kota")
st.pyplot(fig9)

st.markdown("---")
st.markdown("📊 Dashboard ini dibangun menggunakan Streamlit, Matplotlib, dan Seaborn oleh ABDUL 'AZIZ]")
