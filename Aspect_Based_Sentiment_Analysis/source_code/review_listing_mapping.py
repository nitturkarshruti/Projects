#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 00:07:50 2024

@author: lyl331
"""
import subprocess
subprocess.call(["pip","install","shapely"])
subprocess.call(["pip","install","geopandas"])
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

# Function to retrieve census tract
def retrieve_census_tract(lat, lon, nyc_census_tract_data):
    for i, row in nyc_census_tract_data.iterrows():
        if row['geometry'].contains(Point(lon, lat)):
            return "Census Tract " + str(row['COUNTYFP'])
    return ''

# Read the listings.csv file
listings_df = pd.read_csv("listings.csv")

# Read census tract data and filter for NYC counties
nyc_counties = ['005', '047', '061', '081', '085']  # County codes for Bronx, Brooklyn, Manhattan, Queens, Staten Island
census_tract_data = gpd.read_file("census_tracts_filtered.shp")
nyc_census_tract_data = census_tract_data[census_tract_data['COUNTYFP'].isin(nyc_counties)]

# Apply retrieve_census_tract function to each row in listings_df
listings_df['Census Tract'] = listings_df.apply(lambda row: retrieve_census_tract(row['latitude'], row['longitude'], nyc_census_tract_data), axis=1)

# Read the reviews.csv file
reviews_df = pd.read_csv("reviews_2023.csv")

# Merge reviews_df with listings_df on listing_id to map reviews to listings
merged_df = pd.merge(reviews_df, listings_df, how='inner', left_on='listing_id', right_on='id')

# Write the merged DataFrame to CSV
merged_df.to_csv("reviews_listings_mapping.csv", index=False)
