import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style = 'dark')

def create_monthly_df(df):
    monthly_df= day_hour_df.groupby(by='Month').agg({
    'season_x': 'nunique',
    'temp_x': 'mean'
}).reset_index()
    monthly_df.rename(columns ={
        'season_x' : 'SEASON',
        'temp_x' : 'AVG_TEMP'
    }, inplace = True)

    return monthly_df


def create_BY_COUNT(df):
    BY_COUNT = day_hour_df.groupby('season_x')['hr'].count().reset_index()

    return BY_COUNT

def create_BY_SUM(df):
    BY_SUM =  day_hour_df.groupby('season_x')['hr'].sum().reset_index()

    return BY_SUM

day_hour_df =pd.read_csv('C:/Users/Asus/OneDrive/PYTHON/Tugas_akhir/dataset.csv')

datetime_columns= ['dteday_x']
day_hour_df.sort_values(by='dteday_x', inplace=True)
day_hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_hour_df[column] = pd.to_datetime(day_hour_df[column])


min_date = day_hour_df['dteday_x'].min()
max_date = day_hour_df['dteday_x'].max()

with st.sidebar:
    

    
    start_date,end_date = st.date_input(
        label = 'RENTANG WAKTU', min_value=min_date,
        max_value=max_date,
        value= [min_date,max_date]
        )

main_df = day_hour_df[(day_hour_df["dteday_x"] >= str(start_date)) & 
                (day_hour_df["dteday_x"] <= str(end_date))]

monthly_df = create_monthly_df(main_df)
BY_COUNT = create_BY_COUNT(main_df)
BY_SUM = create_BY_SUM(main_df)

st.header('BIKE RENTAL VISUALIZATION')

st.subheader('TEMP AVG BY MONTH')
colors1 = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

fig, ax = plt.subplots(figsize=(20, 10))
    
sns.barplot(
    y="temp_x", 
    x="Month",
    data=day_hour_df.sort_values(by="temp_x", ascending=False),
    palette=colors1,
    ax=ax
    )
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35, rotation = 45)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)



st.subheader('TOTAL RENTAL BY NUMBER OF RENTALS :sparkles:')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    BY_COUNT["season_x"],
    BY_COUNT["hr"],
    marker='o', 
    linewidth=2,
    color="#3357FF"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


st.subheader('TOTAL RENTAL number of hours rental :sparkles:')
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






