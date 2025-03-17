# -*- coding: utf-8 -*-
"""count_aspect_frequency.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gNtIZ-RvuRQQl3pfaLfHcUFvVbyO6TGw
"""

import pandas as pd
import ast
import csv
from collections import Counter

from google.colab import drive
drive.mount('/content/drive')

# Load the CSV file and extract sentiment results from the 8th column
def load_sentiment_results(csv_file_path):
    df = pd.read_csv(csv_file_path, encoding="utf-8")
    sentiment_results = df.iloc[:, 8].apply(lambda x: ast.literal_eval(x)).tolist()
    return sentiment_results

# Count the frequency of each aspect
def count_aspect_frequency(sentiment_results):
    aspect_counter = Counter()
    for result in sentiment_results:
        aspect_counter.update(result.keys())
    return aspect_counter

# Load SentimentResults from the CSV file
csv_file_path = '/content/drive/My Drive/sentiment_analysis_2023.csv'  # Update with your CSV file path
sentiment_results = load_sentiment_results(csv_file_path)

# Count aspect frequencies
aspect_frequency = count_aspect_frequency(sentiment_results)

# Write the output to a new CSV file
output_csv_path = '/content/drive/My Drive/aspect_frequency_output.csv'  # Update with your desired output file path
with open(output_csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Aspect', 'Frequency'])
    for aspect, frequency in aspect_frequency.items():
        writer.writerow([aspect, frequency])

print("Aspect frequencies saved to:", output_csv_path)

# Define the path to your CSV file
csv_file_path = '/content/drive/My Drive/aspect_frequency_output.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Define the column to filter by
filter_column = 'Frequency'

# Apply the filter to get rows where frequency is greater than or equal to 1000
filtered_df = df[df[filter_column] >= 1000]

# Specify the columns to keep in the new CSV file
columns_to_keep = ['Aspect', 'Frequency']

# Save the filtered data to a new CSV file
filtered_csv_path = '/content/drive/My Drive/aspect_frequency_filtered.csv'
filtered_df[columns_to_keep].to_csv(filtered_csv_path, index=False)

print("Filtered data saved successfully!")