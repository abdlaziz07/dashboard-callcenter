import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setup halaman
st.set_page_config(page_title="Call Center Dashboard", layout="wide")
st.title("📞 Call Center Dashboard")

# Load data
df = pd.read_csv("cleaned_call_center.csv", parse_dates=['Call_timestamp'])

# Sidebar filter
st.sidebar.header("🔍 Filter Data")
channel = st.sidebar.multiselect("Pilih Channel:", options=df['Channel'].unique(), default=df['Channel'].unique())
filtered_df = df[df['Channel'].isin(channel)]

# Ringkasan Data
st.subheader("📋 Ringkasan Statistik Data")
st.write(filtered_df.describe())

# Jumlah Panggilan per Bulan
st.subheader("📈 Jumlah Panggilan per Bulan")
monthly_calls = filtered_df.resample('M', on='Call_timestamp').size()
st.line_chart(monthly_calls)

# Durasi vs CSAT
st.subheader("🎯 Durasi Panggilan vs CSAT Score")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=filtered_df, x='Call duration in minutes', y='Csat_score', hue='Channel', ax=ax1)
ax1.set_xlabel("Durasi Panggilan (menit)")
ax1.set_ylabel("CSAT Score")
st.pyplot(fig1)

# Distribusi Sentimen
st.subheader("💬 Distribusi Sentimen Pelanggan")
sentiment_count = filtered_df['Sentiment'].value_counts()
st.bar_chart(sentiment_count)

# Boxplot Durasi per Channel
st.subheader("📦 Boxplot Durasi Panggilan per Channel")
fig2, ax2 = plt.subplots()
sns.boxplot(data=filtered_df, x='Channel', y='Call duration in minutes', ax=ax2)
ax2.set_ylabel("Durasi (menit)")
ax2.set_xlabel("Channel")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Pie Chart Sentimen
st.subheader("🥧 Proporsi Sentimen")
fig3, ax3 = plt.subplots()
sentiment_prop = sentiment_count
ax3.pie(sentiment_prop, labels=sentiment_prop.index, autopct='%1.1f%%', startangle=90)
ax3.axis('equal')
st.pyplot(fig3)

# Korelasi antar fitur numerik
st.subheader("🔥 Korelasi Antar Fitur Numerik")
numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64'])
fig4, ax4 = plt.subplots()
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', ax=ax4)
st.pyplot(fig4)

# Jumlah Panggilan per Channel
st.subheader("📶 Jumlah Panggilan per Channel")
channel_count = filtered_df['Channel'].value_counts()
st.bar_chart(channel_count)

# Footer
st.markdown("---")
st.markdown("📊 Dibuat oleh Abdul 'Aziz menggunakan Streamlit")
