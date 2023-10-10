import streamlit as st
import pandas as pd 
import plotly.express as px


column_names= ["price", "model_year", "model", "condition", "cylinders", "fuel", "odometer", "transmission", "type", "paint_color", "is_4wd", "date_posted", "days_listed"]


df = pd.read_csv('https://raw.githubusercontent.com/surethings41/Dev_Tools_Project/main/vehicles_us.csv', sep =',', header=None, names=column_names)

df = df.iloc[2:]

df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

# the data set carries negligable amounts of mercedes-benz's, many of which have missing data in the other categories. 
# for my purposes here im going to exclude all rows that include 'mercedes-benz' in the manufacturer column 

df = df[df['manufacturer'] != 'mercedes-benz']

df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce')
df.dropna(subset=['odometer'], inplace=True)

st.header('US Vehicles Data Sheet') 
st.dataframe(df)

df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce')
df.dropna(subset=['odometer'], inplace=True)

st.header('Average Milage per Manufacturer')

# grouping data by 'manufacturer' and calculating the average 'odometer' value
manufacturer_avg_odometer = df.groupby('manufacturer')['odometer'].mean().reset_index()

st.write(px.histogram(manufacturer_avg_odometer, x='manufacturer', y='odometer',
                   labels={'odometer': 'Average Mileage (Miles)', 'manufacturer': 'Manufacturer'},
                   orientation='v'))


st.header('Correlation between Mileage and Days on Market')



# scatter plot using Plotly Express 
st.write(px.scatter(df, x='odometer', y='days_listed', color='manufacturer', opacity=.6,
                    labels = {'odometer': 'Odometer', 'days_listed': 'Days Listed', 'manufacturer' : 'Manufacturer'}))


st.header('Compare Condition Distribution between Manufacturers')
st.subheader('Compare Condition Distribution between Manufacturers')

manufact_list = sorted(df['manufacturer'].unique())

manufacturer1 = st.selectbox('Select Manufacturer 1', 
                             options=manufact_list,
                             index=manufact_list.index('toyota')
                             )
manufacturer2 = st.selectbox('Select Manufacturer 2',
                             options=manufact_list,
                             index=manufact_list.index('jeep')
                             )

# checkbox to select 'is_4wd' values
show_4wd = st.checkbox('Show 4WD Vehicles', value=True)

# filtered the df based on manufacturer and 'is_4wd'
manufacturer_filtered_df = df[(df['manufacturer'] == manufacturer1) | (df['manufacturer'] == manufacturer2)]

# filtered the df based on 'is_4wd' checkbox
if not show_4wd:
    filtered_df = manufacturer_filtered_df[manufacturer_filtered_df['is_4wd'].isna()]
else:
    filtered_df = manufacturer_filtered_df

# bar chart to compare 'condition' distribution between manufacturers
fig = px.histogram(
    filtered_df,
    x='Condition',
    y='Number of Vehicles',
    color='manufacturer',
    title=f'Condition Comparison: {manufacturer1} vs. {manufacturer2}',
    labels={'condition': 'Condition'},
    barmode='overlay',
    opacity=.8,
)
st.plotly_chart(fig, use_container_width=True)






