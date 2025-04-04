# -*- coding: utf-8 -*-
"""eviciton_census_tract.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hyRoGqSg-qddpaYrr9aqGIHGkvy_zYrm
"""

import subprocess
subprocess.call(["pip","install","shapely"])
subprocess.call(["pip","install","geopandas"])
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

census_tract_data = gpd.read_file("cb_2022_36_tract_500k.shp")
#print(census_tract_data.columns)
nyc_counties = ['005', '047', '061', '081', '085']
nyc_gdf = census_tract_data[census_tract_data['COUNTYFP'].isin(nyc_counties)]
output_shapefile_path = "census_tracts_filtered.shp"
nyc_gdf.to_file(output_shapefile_path)
nyc_gdf.plot()

from shapely.geometry import Point

# Function to retrieve census tract
def retrieve_census_tract(lat, lon):
    # Read census tract data and filter for NYC counties
    nyc_counties = ['005', '047', '061', '081', '085']  # County codes for Bronx, Brooklyn, Manhattan, Queens, Staten Island
    census_tract_data = gpd.read_file("census_tracts_filtered.shp")
    nyc_census_tract_data = census_tract_data[census_tract_data['COUNTYFP'].isin(nyc_counties)]

    for i, row in nyc_census_tract_data.iterrows():
        if row['geometry'].contains(Point(lon, lat)):
            return "Census Tract " + str(row['COUNTYFP'])
    return ''

# Read the CSV file
evictions_df = pd.read_csv("Evictions_data.csv")

# Create an empty DataFrame to store the counts of evictions per census tract
eviction_counts_df = pd.DataFrame(columns=['Census Tract', 'Eviction Count'])

# Create an empty DataFrame to store the new census tract information
evictions_df['New Census Tract'] = ''

# Iterate through each row
for index, row in evictions_df.iterrows():
    # Extract latitude and longitude
    lat = row['Latitude']
    lon = row['Longitude']
    # Call retrieve_census_tract function
    census_tract = retrieve_census_tract(lat, lon)
     # Update the value in the new column regardless of whether a census tract is found or not
    evictions_df.at[index, 'New Census Tract'] = census_tract
    if census_tract:
        if census_tract in eviction_counts_df['Census Tract'].tolist():
            eviction_counts_df.loc[eviction_counts_df['Census Tract'] == census_tract, 'Eviction Count'] += 1
        else:
            new_row = pd.DataFrame({'Census Tract': [census_tract], 'Eviction Count': [1]})
            eviction_counts_df = pd.concat([eviction_counts_df, new_row], ignore_index=True)

# Write the updated DataFrame back to CSV
evictions_df.to_csv("Evictions_with_new_census_tract_200.csv", index=False)

# Save the counts of evictions per census tract to a CSV file
eviction_counts_df.to_csv("Evictions_Counts_Per_Census_Tract_200.csv", index=False)