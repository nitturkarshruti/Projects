#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

# Define file paths
sentiment_file_path = 'sentiment_analysis_2023.csv'
aspect_frequency_file_path = 'aspect_frequency_filtered.csv'
avg_listing_census_mapping_file_path = 'reviews_listings_mapping.csv'

# Read sentiment analysis data
sentiment_df = pd.read_csv(sentiment_file_path)

# Read aspect frequency data
aspect_frequency_df = pd.read_csv(aspect_frequency_file_path)

# Read avg listing census mapping data
avg_listing_census_mapping_df = pd.read_csv(avg_listing_census_mapping_file_path)

# Initialize dictionary to store number of listings per census tract
listings_per_tract = {}

# Count number of listings per census tract
for tract in avg_listing_census_mapping_df['Census Tract'].unique():
    listings_per_tract[tract] = avg_listing_census_mapping_df[avg_listing_census_mapping_df['Census Tract'] == tract].shape[0]

# Create a new DataFrame with the count of listings per census tract
listings_count_df = pd.DataFrame({'Census Tract': list(listings_per_tract.keys()), 'Number of Listings': list(listings_per_tract.values())})

# Merge sentiment data with listing count data based on Census Tract
merged_df = pd.merge(avg_listing_census_mapping_df, listings_count_df, on='Census Tract')

# Rearrange columns to have 'Number of Listings' at the beginning
cols = merged_df.columns.tolist()
cols = cols[-1:] + cols[:-1]
merged_df = merged_df[cols]

# Save the merged DataFrame to a CSV file with listings count
output_file_path = 'avg_sentiment_aspect_listing_count.csv'
merged_df.to_csv(output_file_path, index=False)

print("Data with listings count saved successfully!")

