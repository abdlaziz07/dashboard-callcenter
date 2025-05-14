# call_center_dashboard.py
import pandas as pd
import streamlit as st
import plotly.express as px

# Load cleaned data
df = pd.read_csv('cleaned_call_center.csv')
df['Call_timestamp'] = pd.to_datetime(df['Call_timestamp'])
df['Day'] = df['Call_timestamp'].dt.day
df['Day_of_week'] = df['Call_timestamp'].dt.day_name()

# Streamlit Layout
st.set_page_config(page_title="Dashboard Call Center", layout="wide")
st.title("📞 Dashboard Analisis Call Center")
st.markdown("""
Dashboard ini menyajikan analisis interaktif terhadap data panggilan call center, termasuk distribusi skor CSAT,
channel layanan, alasan panggilan, serta durasi dan respon waktu.
""")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Data")
    selected_channel = st.selectbox("Pilih Channel:", options=df['Channel'].unique())
    selected_sentiment = st.multiselect("Pilih Sentimen:", options=df['Sentiment'].unique(), default=df['Sentiment'].unique())

# Filter data
filtered_df = df[(df['Channel'] == selected_channel) & (df['Sentiment'].isin(selected_sentiment))]

# 1. Jumlah Panggilan per Hari dalam Seminggu
st.subheader("📅 Jumlah Panggilan per Hari dalam Seminggu")
st.markdown("Melihat hari tersibuk agar tim bisa mengatur jadwal agen secara optimal.")
order_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_data = filtered_df['Day_of_week'].value_counts().reindex(order_days)
fig1 = px.bar(x=day_data.index, y=day_data.values, labels={'x':'Hari', 'y':'Jumlah Panggilan'}, color=day_data.index)
st.plotly_chart(fig1, use_container_width=True)

# 2. Alasan Panggilan Terbanyak
st.subheader("❓ Alasan Panggilan Terbanyak")
st.markdown("Mengetahui isu pelanggan paling sering muncul untuk perbaikan layanan.")
top_reasons = filtered_df['Reason'].value_counts().nlargest(10)
fig2 = px.bar(x=top_reasons.values, y=top_reasons.index, orientation='h', labels={'x':'Jumlah Panggilan', 'y':'Alasan'}, color=top_reasons.index)
st.plotly_chart(fig2, use_container_width=True)

# 3. Kota dengan Jumlah Panggilan Terbanyak
st.subheader("🏙️ Top 10 Kota dengan Jumlah Panggilan Terbanyak")
st.markdown("""Grafik ini menampilkan kota-kota dengan volume panggilan tertinggi Bisa dimanfaatkan untuk memprioritaskan layanan atau penguatan sumber daya berdasarkan wilayah.
""")
top_cities = df['City'].value_counts().nlargest(10)
fig7 = px.bar(x=top_cities.values, y=top_cities.index, orientation='h', labels={'x':'Jumlah Panggilan', 'y':'Kota'}, color=top_cities.index)
st.plotly_chart(fig7, use_container_width=True)

# 4. Distribusi Sentimen
st.subheader("💬 Distribusi Sentimen")
st.markdown("Mengevaluasi persepsi pelanggan terhadap layanan secara keseluruhan.")
fig3 = px.histogram(filtered_df, x='Sentiment', color='Sentiment', category_orders={'Sentiment': ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']})
st.plotly_chart(fig3, use_container_width=True)

# 5. Rata-rata CSAT Score per Channel
st.subheader("📊 Rata-rata CSAT Score per Channel")
st.markdown("Membandingkan performa layanan antar channel untuk evaluasi dan pengembangan.")
avg_csat = df.groupby('Channel')['Csat_score'].mean().reset_index()
fig4 = px.bar(avg_csat, x='Channel', y='Csat_score', color='Channel')
st.plotly_chart(fig4, use_container_width=True)

# 6. Durasi Panggilan vs CSAT Score
st.subheader("⏱️ Durasi Panggilan berdasarkan CSAT Score")
st.markdown("Melihat hubungan durasi dan kepuasan pelanggan sebagai evaluasi efisiensi.")
fig5 = px.box(filtered_df, x='Csat_score', y='Call duration in minutes', points='all', color='Csat_score')
st.plotly_chart(fig5, use_container_width=True)

# 7. Distribusi Response Time
st.subheader("⏱️ Distribusi Response Time")
st.markdown("Menilai kecepatan respon agen dalam menjawab panggilan pelanggan.")
fig6 = px.histogram(filtered_df, x='Response_time', color='Response_time')
st.plotly_chart(fig6, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Dibuat oleh Abdul 'Aziz | Analisis Data Call Center")
