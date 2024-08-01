import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style = 'dark')

def create_monthly_df(df):
    monthly_df= day_hour_df.resample(rule = 'M', on = 'dteday_x').agg({
    'hr': 'mean',
    'season_x' : lambda x: x.iloc[0]
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

day_hour_df =pd.read_csv("dataset.csv")

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

st.subheader('Hour avg by season')


fig, ax = plt.subplots(figsize=(20, 10))
    
sns.barplot(
    y="hr", 
    x="season_x",
    data=day_hour_df.sort_values(by="hr", ascending=False),
    palette='viridis',
    ax=ax
    )
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35, rotation = 45)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)



st.subheader('percentage of usage each season')
fig, ax =plt.subplots(figsize=(10, 5))
ax.pie(
    BY_COUNT['hr'],
    labels = BY_COUNT['season_x'],
    autopct='%1.1f%%',
    startangle=140,
    colors=["#72BCD4", "#FFC0CB", "#FFB6C1", "#FF677D"]
)
 
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






