import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Fungsi untuk membuat DataFrame berdasarkan agregasi bulanan
def create_count_df(df):
    count = df.groupby('Month').agg({
        'weekday_avg': 'sum',
        'holiday_x': 'sum'
    }).reset_index()
    return count

# Fungsi untuk membuat DataFrame berdasarkan hitungan (count)
def create_BY_COUNT(df):
    BY_COUNT = df.groupby('season_x')['hr'].count().reset_index()
    return BY_COUNT

# Fungsi untuk membuat DataFrame berdasarkan penjumlahan (sum)
def create_BY_SUM(df):
    BY_SUM = df.groupby('season_x')['hr'].sum().reset_index()
    return BY_SUM

# Memuat dataset
day_hour_df = pd.read_csv("dataset.csv")

# Konversi kolom tanggal
day_hour_df['dteday_x'] = pd.to_datetime(day_hour_df['dteday_x'], errors='coerce')
day_hour_df['Month'] = day_hour_df['dteday_x'].dt.strftime('%b')  # Menambahkan nama bulan

# Mendapatkan rentang tanggal minimum dan maksimum
min_date = day_hour_df['dteday_x'].min()
max_date = day_hour_df['dteday_x'].max()

# Input rentang waktu pada sidebar di Streamlit
with st.sidebar:
    start_date, end_date = st.date_input(
        label='RENTANG WAKTU', 
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    # Konversi tanggal dari Streamlit menjadi datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

# Filter data berdasarkan rentang tanggal
main_df = day_hour_df[
    (day_hour_df['dteday_x'] >= start_date) &
    (day_hour_df['dteday_x'] <= end_date)
]

# Membuat DataFrame bulanan
count = create_count_df(main_df)
BY_COUNT = create_BY_COUNT(main_df)
BY_SUM = create_BY_SUM(main_df)

# Visualisasi: Sum of Weekday Avg and Holiday by Month
st.header('Sum of Weekday Avg and Holiday by Month')
fig, ax = plt.subplots(figsize=(10, 6))

x = range(len(count))  # Posisi x untuk setiap bulan
width = 0.35  # Lebar bar

# Bar untuk weekday_avg
ax.bar(
    [p - width / 2 for p in x],
    count['weekday_avg'],
    width,
    label='Weekday Avg',
    color='skyblue'
)

# Bar untuk holiday_x
ax.bar(
    [p + width / 2 for p in x],
    count['holiday_x'],
    width,
    label='Holiday',
    color='orange'
)

# Menambahkan label dan keterangan
ax.set_xticks(x)
ax.set_xticklabels(count['Month'])
ax.set_xlabel('Month')
ax.set_ylabel('Sum of Values')
ax.set_title('Sum of Weekday Avg and Holiday by Month')
ax.legend()

st.pyplot(fig)

# Subheader dan plot persentase penggunaan setiap musim
st.subheader('Percentage of usage each season')
fig, ax = plt.subplots(figsize=(10, 5))
ax.pie(
    BY_COUNT['hr'],
    labels=BY_COUNT['season_x'],
    autopct='%1.1f%%',
    startangle=140,
    colors=["#72BCD4", "#FFC0CB", "#FFB6C1", "#FF677D"]
)
st.pyplot(fig)

# Subheader dan plot jumlah jam rental
st.subheader('Total rental number of hours')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    BY_SUM["season_x"],
    BY_SUM["hr"],
    marker='o', 
    linewidth=2,
    color="#33FF57"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)