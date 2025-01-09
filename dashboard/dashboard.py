import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Dapatkan directory path dari file dashboard.py
current_dir = os.path.dirname(__file__)
# Buat full path ke file CSV
file_path = os.path.join(current_dir, "main_data.csv")
# Baca file CSV
all_df = pd.read_csv(file_path)

all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

st.header('Bike Rentals Dashboard :sparkles:')

st.subheader('Annual Rental')
 
col1, col2 = st.columns(2)
 
with col1:
    year_zero_data = all_df[all_df['yr'] == 0]
    total_rental1 = year_zero_data["cnt_x"].sum()
    st.metric("2011 total rental", value=total_rental1)

with col2:
    year_one_data = all_df[all_df['yr'] == 1]
    total_rental2 = year_one_data["cnt_x"].sum()
    st.metric("2012 total rental", value=total_rental2)
 
# Agregasi data per bulan untuk tahun 2011 dan 2012
data_2011 = all_df[all_df['yr'] == 0].groupby('mnth')['cnt_y'].sum().reset_index()
data_2012 = all_df[all_df['yr'] == 1].groupby('mnth')['cnt_y'].sum().reset_index()

tab1, tab2 = st.tabs(["2011 Rentals", "2012 Rentals"])

with tab1:
    st.subheader("Total Rentals (2011)")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        data_2011['mnth'],
        data_2011['cnt_y'],
        marker='o',
        linewidth=2,
        color="#90CAF9",
    )
    ax.set_title("Total Rentals by Month (2011)", fontsize=20)
    ax.set_xlabel("Month", fontsize=15)
    ax.set_ylabel("Total Rentals", fontsize=15)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)

with tab2:
    st.subheader("Total Rentals (2012)")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        data_2012['mnth'],
        data_2012['cnt_y'],
        marker='o',
        linewidth=2,
        color="#90CAF9",
    )
    ax.set_title("Total Rentals by Month (2012)", fontsize=20)
    ax.set_xlabel("Month", fontsize=15)
    ax.set_ylabel("Total Rentals", fontsize=15)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)

st.subheader("The Influence of Weather Conditions on Bicycle Rentals")

fig, ax = plt.subplots(figsize=(8, 5))
weather_counts = all_df.groupby('weathersit')['cnt_x'].sum().reset_index()
sns.barplot(data=weather_counts, x='weathersit', y='cnt_x', palette='cubehelix')
plt.xlabel('Weather Conditions (1=Clear, 4=Bad)')
plt.ylabel('Total bike rentals')

st.pyplot(fig)

st.subheader("The Influence of Seasons on Bicycle Rentals")

fig, ax = plt.subplots(figsize=(8, 5))
season_counts = all_df.groupby('season')['cnt_x'].sum().reset_index()
sns.barplot(data=season_counts, x='season', y='cnt_x', palette='cubehelix')
plt.xlabel('Seasons (1:spring, 2:summer, 3:autumn, 4:winter)')
plt.ylabel('Total Bicycle Rentals')

st.pyplot(fig)

st.subheader("Bicycle Usage Patterns Throughout the Week")

fig, ax = plt.subplots(figsize=(8, 5))
weekday_counts = all_df.groupby('weekday')['cnt_x'].sum().reset_index()
sns.barplot(data=weekday_counts, x='weekday', y='cnt_x', palette='cubehelix')
plt.xlabel('Day (0: Sunday, 1: Monday, 2: Tuesday, 3: Wednesday, 4: Thursday, 5: Friday, 6: Saturday)')
plt.ylabel('Total Bicycle Rentals')
plt.show()

st.pyplot(fig)
 
st.subheader("Bicycle Rental Patterns by Hour and Day")

fig, ax = plt.subplots(figsize=(8, 5))
hourly_counts = all_df.groupby(['hr', 'workingday'])['cnt_x'].mean().reset_index()
sns.lineplot(data=hourly_counts, x='hr', y='cnt_x', hue='workingday', palette='cubehelix')
plt.xlabel('Hour (0-23)')
plt.ylabel('Average Bike Rentals')
plt.legend(title='Workdays', labels=['Weekend/Holiday', 'Workday'])

st.pyplot(fig)

st.subheader("Rental Patterns: Casual vs Registered Users")

fig, ax = plt.subplots(figsize=(8, 5))
user_counts = all_df[['casual', 'registered']].sum().reset_index()
user_counts.columns = ['User Type', 'Total Rentals']
sns.barplot(data=user_counts, x='User Type', y='Total Rentals', palette='cubehelix')
plt.xlabel('User Type')
plt.ylabel('Total Bicycle Rentals')

st.pyplot(fig)

st.caption('Copyright (c) Ridhaka Gina Amalia @ginardka')