import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import plotly.express as px
import time
import copy

# set the title
st.title("Contact Crime Analysis")
st.info('''Contact crime refers to those crimes in which the victims themselves are the targets of violence or property is targeted and the victims in the vicinity during the commission of the crime are subjected to threats of violence or the use of such violence. 
        
Contact crimes include; Murder, Attempted Murder, Assault with the intent to inflict Grievous Bodily Harm (Assault GBH), Common Assault, Aggravated Robbery, Common Robbery and Sexual Offences.

The South African Police Services reporting period runs from April to March.

Data was sourced from the South African Police Services''')

st.subheader("South Africa")


# import contact_crime_geo
contact_crime_geo = pd.read_csv('contact_crime_geo.csv')
# create deep copy of the contact_crime_geo dataframe
contact_crime_geo_copy = pd.DataFrame(columns = contact_crime_geo.columns, data = copy.deepcopy(contact_crime_geo.values))


# side bar - step1: Province filtering
provinces_list = list(contact_crime_geo_copy['Province_station'].unique())
provinces_list.sort()

# present province options
step_one = st.sidebar.write('# Database filtering \n ## Step 1: \n ### Select the province(s) of interest')
prov_choice = st.sidebar.multiselect('Leave it blank if you are interested in all provinces.', provinces_list)

# filter the df based on province selection
if len(prov_choice) > 0:
    prov_filter = contact_crime_geo_copy['Province_station'].isin(prov_choice)
    contact_crime_geo_copy = contact_crime_geo_copy[prov_filter]

    
# side bar - step2: Cluster filtering
cluster_list = list(contact_crime_geo_copy['cluster'].unique())
cluster_list.sort()

# present cluster options
step_two = st.sidebar.write('## Step 2: \n ### Select the cluster(s) of interest')
cluster_choice = st.sidebar.multiselect('Leave it blank if you are interested in all clusters.', cluster_list)

# filter the df based on cluster selection
if len(cluster_choice) > 0:
    cluster_filter = contact_crime_geo_copy['cluster'].isin(cluster_choice)
    contact_crime_geo_copy = contact_crime_geo_copy[cluster_filter]
  
     
# side bar - step3: Station filtering
station_list = list(contact_crime_geo_copy['station'].unique())
station_list.sort()

# present station options
step_three = st.sidebar.write('## Step 3: \n ### Select the station(s) of interest')
station_choice = st.sidebar.multiselect('Leave it blank if you are interested in all stations.', station_list)

# filter the df based on station selection
if len(station_choice) > 0 and 'All' not in station_choice:
    station_filter = contact_crime_geo_copy['station'].isin(station_choice)
    contact_crime_geo_copy = contact_crime_geo_copy[station_filter]


# side bar - step4: Crime filtering
crime_cat_list = list(contact_crime_geo_copy['Crime Category'].unique())
crime_cat_list.sort()

# present crime options
step_four = st.sidebar.write('## Step 4: \n ### Select the crime(s) of interest')
crime_choice = st.sidebar.multiselect('Leave it blank if you are interested in all crimes.', crime_cat_list)

# filter the df based on crime selection
if len(crime_choice) > 0 and 'All' not in crime_choice:
    crime_filter = contact_crime_geo_copy['Crime Category'].isin(crime_choice)
    contact_crime_geo_copy = contact_crime_geo_copy[crime_filter]


# side bar - step5: Period filtering
list_of_years = ['2008','2009', '2010','2011','2012','2013','2014',
                 '2015','2016','2017','2018','2019','2020']

# present crime options
step_five = st.sidebar.write('## Step 5: \n ### Select the period of interest')
year_choice = st.sidebar.multiselect('Leave it blank if you are interested in all crimes.', list_of_years)

# filter the df based on crime selection
if len(year_choice) > 0 and 'All' not in year_choice:
    year_choice.sort()
    contact_crime_geo_copy = contact_crime_geo_copy[['station','Province_station','cluster','Crime Category',
            'longitude','latitude']+ year_choice]

# visualize the map
st.info('Mapped data based on your filter options')
st.map(data=contact_crime_geo_copy, zoom=4, use_container_width=False)

# visualize the dataframe  
st.info('Database based on your filter options -- scrolling may be required')  
st.write(contact_crime_geo_copy.shape[0], 'rows and', contact_crime_geo_copy.shape[1], 'columns') 
st.dataframe(contact_crime_geo_copy)


# group the data by province
if len(year_choice) > 0:
    province_grouping = contact_crime_geo_copy.groupby('Province_station')[year_choice].sum()
else:
    province_grouping = contact_crime_geo_copy.groupby('Province_station')[list_of_years].sum()
province_grouping = province_grouping.reset_index()

# group the data by cluster
if len(year_choice) > 0:
    cluster_grouping = contact_crime_geo_copy.groupby('cluster')[year_choice].sum()
else:
    cluster_grouping = contact_crime_geo_copy.groupby('cluster')[list_of_years].sum()
cluster_grouping = cluster_grouping.reset_index()

# group the data by station
if len(year_choice) > 0:
    station_grouping = contact_crime_geo_copy.groupby('station')[year_choice].sum()
else:
    station_grouping = contact_crime_geo_copy.groupby('station')[list_of_years].sum()   
station_grouping = station_grouping.reset_index()

# group the data by crime category
if len(year_choice) > 0:
    crime_grouping = contact_crime_geo_copy.groupby('Crime Category')[year_choice].sum()
else:
    crime_grouping = contact_crime_geo_copy.groupby('Crime Category')[list_of_years].sum()
crime_grouping = crime_grouping.reset_index()

# group the data by year
year_grouping = contact_crime_geo_copy
# remove the lat and long from the aggregation
year_grouping.drop(['latitude', 'longitude'], axis=1, inplace=True)
year_grouping = contact_crime_geo_copy.pivot_table(columns='Crime Category')
year_grouping = year_grouping.reset_index()
year_grouping.rename(columns={'index':'year'}, inplace=True)
# convert floats to integers
for col in list(year_grouping.columns):
    year_grouping[col] = year_grouping[col].astype(int)
    
    
st.info('Filtered cases per period, by crime')
st.write(crime_grouping.shape[0], 'rows and', crime_grouping.shape[1], 'columns') 
st.dataframe(crime_grouping)

st.info('Filtered cases per period, by province')
st.write(province_grouping.shape[0], 'rows and', province_grouping.shape[1], 'columns') 
st.dataframe(province_grouping)

st.info('Filtered cases per period, by cluster')
st.write(cluster_grouping.shape[0], 'rows and', cluster_grouping.shape[1], 'columns') 
st.dataframe(cluster_grouping)

st.info('Filtered cases per period, by station')
st.write(station_grouping.shape[0], 'rows and', station_grouping.shape[1], 'columns') 
st.dataframe(station_grouping)

st.info('Filtered cases per period, by year')
st.write(year_grouping.shape[0], 'rows and', year_grouping.shape[1], 'columns') 
st.dataframe(year_grouping)

cols = list(year_grouping.columns) #
cols.remove('year')

def basic_chart():
    for col in cols:
        df =  year_grouping[['year',col]]

        bar_chart = px.bar(df,
                           x = 'year',
                           y = col,
                           text = col,
                           color_discrete_sequence = ['#F63366']* len(df),
                           template = 'plotly_white')
        st.plotly_chart(bar_chart)

if st.sidebar.button('Plot basic chart'):
    basic_chart()
    

    
    



















