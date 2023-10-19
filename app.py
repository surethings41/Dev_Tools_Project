import streamlit as st
import pandas as pd 
import plotly.express as px


column_names= ["price", "model_year", "model", "condition", "cylinders", "fuel", "odometer", "transmission", "type", "paint_color", "is_4wd", "date_posted", "days_listed"]


df = pd.read_csv('notebooks/post_eda_us_vehicle.csv', sep =',', header=None, names=column_names)

df = df.iloc[2:]

df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

# the data set carries negligable amounts of mercedes-benz's, many of which have missing data in the other categories. 
# for my purposes here im going to exclude all rows that include 'mercedes-benz' in the manufacturer column 

df = df[df['manufacturer'] != 'mercedes-benz']



st.header('US Vehicles Data Sheet') 
st.dataframe(df)



st.header('Average Milage per Manufacturer')

df['odometer']=df['odometer'].astype(int)
df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce')

# grouping data by 'manufacturer' and calculating the average 'odometer' value
manufacturer_avg_odometer = df.groupby('manufacturer')['odometer'].mean().reset_index()



fig = px.bar(
    manufacturer_avg_odometer,
    x='manufacturer',
    y='odometer',
    labels={'odometer': 'Average Mileage (Miles)', 'manufacturer': 'Manufacturer'},
    title='Average Mileage per Manufacturer'
)

st.plotly_chart(fig, use_container_width=True)



st.header('Correlation between Mileage and Days on Market')

selected_condition = st.selectbox('Select Condition', df['condition'].unique())

# Filter rows with non-null and non-zero 'odometer' values
condition_df = df[(df['condition'] == selected_condition) & (df['odometer'].notna()) & (df['odometer'] != 0)]

# Scatter plot using Plotly Express
scatter_fig = px.scatter(
    condition_df, 
    x='odometer', 
    y='days_listed', 
    color='manufacturer', 
    opacity=.6,
    labels={'odometer': 'Odometer', 'days_listed': 'Days Listed', 'manufacturer': 'Manufacturer'}
)

scatter_fig.update_layout(
    xaxis=dict(
        range=[50000, int(condition_df['odometer'].max()) + 50000],
        tickvals=list(range(1, int(condition_df['odometer'].max())+ 50000, 50000)),  
    ),
    yaxis=dict(
        range=[5, 300],  
        tickvals=list(range(5, 300, 20)), 
    )
)

# Display the scatter plot using st.plotly_chart
st.plotly_chart(scatter_fig, use_container_width=True)







st.header('Compare Condition Distribution between Manufacturers')

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
    x='condition',
    color='manufacturer',
    title=f'Condition Comparison: {manufacturer1} vs. {manufacturer2}',
    labels={'condition': 'Condition'},
    barmode='overlay',
    opacity=.8,
)

fig.update_yaxes(title_text='Number of Vehicles')

st.plotly_chart(fig, use_container_width=True)






