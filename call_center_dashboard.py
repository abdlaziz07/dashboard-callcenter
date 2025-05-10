import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Setup
st.set_page_config(page_title="📞 Call Center Dashboard", layout="wide")
st.title("📞 Dashboard Analisis Call Center")

# === 2. LOAD DATA ===
@st.cache
def load_data():
    df = pd.read_csv('cleaned_call_center.csv')
    df['Call_timestamp'] = pd.to_datetime(df['Call_timestamp'])
    df['Month'] = df['Call_timestamp'].dt.to_period('M').astype(str)
    df['Day_of_week'] = df['Call_timestamp'].dt.day_name()
    return df

df = load_data()

# === 3. SIDEBAR FILTER ===
st.sidebar.header("Filter Data")
selected_channel = st.sidebar.multiselect(
    "Pilih Channel:", options=df['Channel'].unique(), default=df['Channel'].unique()
)
selected_month = st.sidebar.multiselect(
    "Pilih Bulan:", options=df['Month'].unique(), default=df['Month'].unique()
)

filtered_data = df[
    (df['Channel'].isin(selected_channel)) & (df['Month'].isin(selected_month))
]

# === 4. GRAFIK INTERAKTIF ===

# 1. Distribusi CSAT Score
st.subheader("Distribusi CSAT Score")
fig_csat = px.histogram(
    filtered_data,
    x='Csat_score',
    color='Sentiment',
    title='Distribusi CSAT Score Berdasarkan Sentimen',
    labels={'Csat_score': 'CSAT Score', 'count': 'Jumlah'},
    template='plotly_white',
    color_discrete_sequence=px.colors.qualitative.Viridis
)
st.plotly_chart(fig_csat, use_container_width=True)

# 2. Jumlah Panggilan per Bulan
st.subheader("Jumlah Panggilan per Bulan")
monthly_calls = filtered_data['Month'].value_counts().sort_index()
fig_monthly_calls = px.bar(
    x=monthly_calls.index,
    y=monthly_calls.values,
    title='Jumlah Panggilan per Bulan',
    labels={'x': 'Bulan', 'y': 'Jumlah Panggilan'},
    template='plotly_white',
    color=monthly_calls.values,
    color_continuous_scale='Blues'
)
st.plotly_chart(fig_monthly_calls, use_container_width=True)

# 3. Jumlah Panggilan per Hari
st.subheader("Jumlah Panggilan per Hari")
order_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_calls = filtered_data['Day_of_week'].value_counts().reindex(order_days)
fig_daily_calls = px.bar(
    x=daily_calls.index,
    y=daily_calls.values,
    title='Jumlah Panggilan per Hari',
    labels={'x': 'Hari', 'y': 'Jumlah Panggilan'},
    template='plotly_white',
    color=daily_calls.values,
    color_continuous_scale='Sunset'
)
st.plotly_chart(fig_daily_calls, use_container_width=True)

# 4. Alasan Panggilan (Top 10)
st.subheader("Top 10 Alasan Panggilan")
top_reasons = filtered_data['Reason'].value_counts().nlargest(10).reset_index()
top_reasons.columns = ['Reason', 'Call Count']
fig_top_reasons = px.bar(
    top_reasons,
    x='Call Count',
    y='Reason',
    orientation='h',
    title='10 Alasan Panggilan Terbanyak',
    labels={'Call Count': 'Jumlah Panggilan', 'Reason': 'Alasan'},
    template='plotly_white',
    color='Call Count',
    color_continuous_scale='Cool'
)
st.plotly_chart(fig_top_reasons, use_container_width=True)

# 5. Top 10 Kota Berdasarkan Panggilan
st.subheader("Top 10 Kota dengan Panggilan Terbanyak")
top_cities = filtered_data['City'].value_counts().nlargest(10).reset_index()
top_cities.columns = ['City', 'Call Count']
fig_top_cities = px.bar(
    top_cities,
    x='Call Count',
    y='City',
    orientation='h',
    title='Top 10 Kota dengan Panggilan Terbanyak',
    labels={'Call Count': 'Jumlah Panggilan', 'City': 'Kota'},
    template='plotly_white',
    color='Call Count',
    color_continuous_scale='Plasma'
)
st.plotly_chart(fig_top_cities, use_container_width=True)

# 6. Rata-rata CSAT per Channel
st.subheader("Rata-rata CSAT Score per Channel")
fig_csat_channel = px.bar(
    filtered_data.groupby('Channel')['Csat_score'].mean().reset_index(),
    x='Channel',
    y='Csat_score',
    title='Rata-rata CSAT Score per Channel',
    labels={'Csat_score': 'Rata-rata CSAT Score', 'Channel': 'Channel'},
    template='plotly_white',
    color='Csat_score',
    color_continuous_scale='Viridis'
)
st.plotly_chart(fig_csat_channel, use_container_width=True)

# 7. Distribusi Response Time
st.subheader("Distribusi Response Time")
fig_response_time = px.histogram(
    filtered_data,
    x='Response_time',
    title='Distribusi Response Time',
    labels={'Response_time': 'Response Time', 'count': 'Jumlah'},
    template='plotly_white',
    color_discrete_sequence=['#636EFA']
)
st.plotly_chart(fig_response_time, use_container_width=True)

# 8. Durasi Panggilan vs CSAT Score
st.subheader("Durasi Panggilan Berdasarkan CSAT Score")
fig_call_duration = px.box(
    filtered_data,
    x='Csat_score',
    y='Call duration in minutes',
    title='Durasi Panggilan vs CSAT Score',
    labels={'Csat_score': 'CSAT Score', 'Call duration in minutes': 'Durasi Panggilan (menit)'},
    template='plotly_white',
    color='Csat_score'
)
st.plotly_chart(fig_call_duration, use_container_width=True)
# Footer
st.markdown("---")
st.markdown("📊 Dashboard ini dibangun menggunakan **Streamlit**, **Matplotlib**, dan **Seaborn** oleh **Abdul 'Aziz**")
