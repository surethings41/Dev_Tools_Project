import streamlit as st
import pandas as pd 
import plotly.express as px

column_names= ["price", "model_year", "model", "condition", "cylinders", "fuel", "odometer", "transmission", "type", "paint_color", "is_4wd", "date_posted", "days_listed"]


df = pd.read_csv('/Users/jeffreyheller/Desktop/Dev_Tools_Project/vehicles_us.csv', sep =',', header=None, names=column_names)

df = df.iloc[2:]

df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

st.header('US Vehicles Data Sheet') 
st.dataframe(df)


st.header('Mileage Based on Vehicle Type')
# histogram figure
fig = px.histogram(df, x='odometer', color='type')
st.write(fig)