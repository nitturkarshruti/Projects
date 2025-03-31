# -*- coding: utf-8 -*-
#!/bin/env python3
import pandas as pd

# # Define file paths
# aspect_frequency_file_path = 'aspect_frequency_filtered.csv'
# avg_listing_census_mapping_file_path = 'avg_sentiment_aspect_listing.csv'

# # Read aspect_frequency_filtered.csv
# aspect_frequency_df = pd.read_csv(aspect_frequency_file_path)

# # Extract aspects from aspect_frequency_df
# aspects = aspect_frequency_df['Aspect'].unique()

# # Read avg_listing_census_mapping.csv with Census Tract and selected columns only
# columns_to_read = ['listing_id','%','Number of Reviews'] + list(aspects)

# # Check if columns from aspects exist in avg_sentiment_aspect_listing.csv
# existing_columns = []
# for col in columns_to_read:
#     if col in pd.read_csv(avg_listing_census_mapping_file_path, nrows=1).columns:
#         existing_columns.append(col)

# # Read only existing columns
# avg_listing_census_mapping_df = pd.read_csv(avg_listing_census_mapping_file_path, usecols=existing_columns)

# # Save the filtered columns to a new CSV file
# filtered_columns_csv_path = 'avg_sentiment_aspect_listing_filtered.csv'
# avg_listing_census_mapping_df.to_csv(filtered_columns_csv_path, index=False)

# print("Filtered columns saved successfully!")

# Define the path to your CSV file
csv_file_path = 'avg_sentiment_aspect_listing_filtered.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Define a function to process each cell
def process_cell(cell):
     # Check if the cell is not empty
    if pd.notna(cell):
        # Convert the cell contents to a string
        cell_str = str(cell)
        # Parse the string representation of the list of values
        values = eval(cell_str)
        # Keep only the first two values and convert back to string
        processed_values = str(values[:2])
    else:
        processed_values = cell  # Return the empty cell as is
    return processed_values

# Apply the function to all cells in the DataFrame except for the first column (Census Tract)
for column in df.columns[3:]:
    df[column] = df[column].apply(process_cell)

# Save the modified DataFrame back to CSV
modified_csv_path = 'avg_sentiment_aspect_listing_modified.csv'
df.to_csv(modified_csv_path, index=False)

print("CSV file modified and saved successfully!")

