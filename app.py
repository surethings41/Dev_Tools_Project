import streamlit as st
import pandas as pd 
import plotly.express as px

column_names= ["price", "model_year", "model", "condition", "cylinders", "fuel", "odometer", "transmission", "type", "paint_color", "is_4wd", "date_posted", "days_listed"]


df = pd.read_csv('/Users/jeffreyheller/Desktop/Dev_Tools_Project/vehicles_us.csv', sep =',', header=None, names=column_names)

df = df.iloc[2:]

df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

# the data set carries negligable amounts of mercedes-benz's, many of which have missing data in the other categories. 
# for my purposes here im going to exclude all rows that include 'mercedes-benz' in the manufacturer column 

df = df[df['manufacturer'] != 'mercedes-benz']


st.header('US Vehicles Data Sheet') 
st.dataframe(df)


st.header('Mileage Based on Vehicle Type')
# histogram figure
df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce')

# Group data by 'manufacturer' and calculate the average 'odometer' value
manufacturer_avg_odometer = df.groupby('manufacturer')['odometer'].mean().reset_index()

# Create a Plotly Express bar chart
fig = px.bar(manufacturer_avg_odometer, x='manufacturer', y='odometer', title='Average Odometer Reading by Manufacturer')

# Customize the chart layout if needed
fig.update_layout(xaxis_title='Manufacturer', yaxis_title='Average Odometer (Miles)')
fig.update_traces(marker_color='red')  # You can change the marker_color as desired


# Display the chart using st.plotly_chart
st.title('Average Odometer Reading by Manufacturer')
st.plotly_chart(fig)