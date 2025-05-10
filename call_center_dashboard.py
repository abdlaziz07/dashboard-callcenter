import streamlit as st
import pandas as pd
import plotly.express as px

# === Load Data ===
df = pd.read_csv('cleaned_call_center.csv')
df['Call_timestamp'] = pd.to_datetime(df['Call_timestamp'])

# Feature Engineering
df['Month'] = df['Call_timestamp'].dt.to_period('M').astype(str)
df['Day_of_week'] = df['Call_timestamp'].dt.day_name()

# === Streamlit App ===
st.set_page_config(page_title="Call Center Dashboard", layout="wide")
st.title("📞 Call Center Analysis Dashboard")
st.markdown("""
Dashboard ini menampilkan analisis performa layanan call center berdasarkan data panggilan, sentimen pelanggan, dan kanal layanan.
""")

# Sidebar filter
st.sidebar.header("Filter")
selected_channel = st.sidebar.selectbox("Pilih Channel", options=['All'] + sorted(df['Channel'].unique().tolist()))
selected_sentiment = st.sidebar.selectbox("Pilih Sentiment", options=['All'] + sorted(df['Sentiment'].unique().tolist()))

# Filter Data
filtered_df = df.copy()
if selected_channel != 'All':
    filtered_df = filtered_df[filtered_df['Channel'] == selected_channel]
if selected_sentiment != 'All':
    filtered_df = filtered_df[filtered_df['Sentiment'] == selected_sentiment]

# Layout 2 Kolom
col1, col2 = st.columns(2)

# Distribusi CSAT Score
with col1:
    st.subheader("📊 Distribusi CSAT Score")
    fig_csat = px.histogram(filtered_df, x='Csat_score', color='Csat_score', nbins=10)
    st.plotly_chart(fig_csat, use_container_width=True)

# Distribusi Sentimen
with col2:
    st.subheader("😊 Distribusi Sentimen")
    fig_sentiment = px.histogram(filtered_df, x='Sentiment', color='Sentiment')
    st.plotly_chart(fig_sentiment, use_container_width=True)

# Jumlah Panggilan per Bulan
st.subheader("🗓️ Jumlah Panggilan per Bulan")
monthly_calls = filtered_df.groupby('Month').size().reset_index(name='Jumlah')
fig_monthly = px.bar(monthly_calls, x='Month', y='Jumlah')
st.plotly_chart(fig_monthly, use_container_width=True)

# Jumlah Panggilan per Hari
st.subheader("📆 Jumlah Panggilan per Hari")
order_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_calls = filtered_df['Day_of_week'].value_counts().reindex(order_days).reset_index()
day_calls.columns = ['Hari', 'Jumlah']
fig_days = px.bar(day_calls, x='Hari', y='Jumlah')
st.plotly_chart(fig_days, use_container_width=True)

# Alasan Panggilan Terbanyak (Adaptif)
st.subheader("🔍 Alasan Panggilan Terbanyak")
top_reasons = filtered_df['Reason'].value_counts().nlargest(10)
if len(top_reasons) < 3:
    st.warning("Data terlalu sedikit untuk menampilkan 10 alasan terbanyak berdasarkan filter. Menampilkan data global.")
    top_reasons = df['Reason'].value_counts().nlargest(10)
fig_reason = px.bar(
    x=top_reasons.values,
    y=top_reasons.index,
    orientation='h',
    labels={'x': 'Jumlah Panggilan', 'y': 'Alasan'},
    title='10 Alasan Panggilan Terbanyak'
)
st.plotly_chart(fig_reason, use_container_width=True)

# Rata-rata CSAT per Channel
st.subheader("📺 Rata-rata CSAT per Channel")
csat_channel = filtered_df.groupby('Channel')['Csat_score'].mean().reset_index()
fig_csat_channel = px.bar(csat_channel, x='Channel', y='Csat_score', color='Channel')
st.plotly_chart(fig_csat_channel, use_container_width=True)

# Durasi Panggilan berdasarkan CSAT
st.subheader("⏱️ Durasi Panggilan vs CSAT")
fig_duration = px.box(filtered_df, x='Csat_score', y='Call duration in minutes', points='all')
st.plotly_chart(fig_duration, use_container_width=True)

st.caption("Dashboard dibuat oleh Abdul 'Aziz")
