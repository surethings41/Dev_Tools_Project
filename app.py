import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_option('deprecation.showfileUploaderEncoding', False)

column_names= ["price", "model_year", "model", "condition", "cylinders", "fuel", "odometer", "transmission", "type", "paint_color", "is_4wd", "date_posted", "days_listed"]


df = pd.read_csv('https://raw.githubusercontent.com/surethings41/Dev_Tools_Project/main/us_vehicle_3.1.csv', sep =',', header=None, names=column_names, encoding='utf-8', index_col=False)

df = df[column_names].shift(axis=0)

df = df.iloc[2:]
df['manufacturer'] = df['model'].astype(str).apply(lambda x: x.split()[0])




st.header('US Vehicles Data Sheet (2018-2019)') 
st.subheader('This application seeks to analyze data of car sales in the US between 2018 and 2019.')
st.write('More Specifically, it will attempt to illustrate the following:')
st.write('-The average miles on the odometer per vehicle based on the manufacturer')
st.write('-The correlation between Odometer reading and Days on Market')
st.write('-The condition distribution between Manufacturers with the option to filter for both 4wd and non-4wd vehicles')
st.write('-The predominate car colors on the market are "White", "Black", and "Silver"')

st.subheader('Below is a display of the raw data from the csv file.')
st.write('***Duplicates and missing values have all been removed/metigated in order to not disrupt certain conclusions and observations')
st.dataframe(df)




st.header('Average Milage per Manufacturer')
st.write('-Acura, Toyota, GMC, and Honda all have the highest average (in order) milage-per-vehicle.') 
st.write('-We might be able to make an inferrence that cars from these manufacturers have a tendency to last longer and be more reliable.')
st.write('-Further analysis would be required to confirm this. ')

df['odometer']=df['odometer'].astype(float)
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
st.write('There is a positive correlation between the miles on the odometer of a vehicle and the days that is spends on-market.')

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
st.write('Further analysis of the "condition" distribution between manufacturers reveals a lot more details concerning the inference made on the first conclusion.')
st.write('One revelation in particular is that when the condition distribution between Honda and Toyota is illustrated, even though Honda has a higher average mileage per vehicle, Toyota has roughly 40% to 50% more units in better condition either on the road or in the market. ')

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


st.header('Pie Chart of Car Colors based on # of Total cars on Market')


data = pd.DataFrame({'paint_color': ['white', 'black', 'silver', 'grey', 'blue', 'red', 'green', 'brown', 'custom', 'yellow', 'orange', 'purple'],
                     'Count': [9960, 7606, 6193, 4995, 4444, 4386, 1377, 1206, 1142, 253, 225, 101]})

color_map = {
    'white': 'white',
    'black': 'black',
    'silver': 'silver',
    'grey': 'grey',
    'blue': 'blue',
    'red': 'red',
    'green': 'green',
    'brown': 'brown',
    'custom': 'rgb(255, 0, 255)',
    'yellow': 'yellow',
    'orange': 'orange',
    'purple': 'purple',
}

data['color'] = data['paint_color'].map(color_map)

fig = px.pie(data, names='paint_color', values='Count',
             title='Pie Chart of Paint Colors in DF',
             color='color', 
             color_discrete_map=color_map)

st.plotly_chart(fig, use_container_width=True)





