# -*- coding: utf-8 -*-
"""Avg_sentiment_aspect_listing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RO6Xc0PeUMNiMbXKFJlpeCNks26WqkvV
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

#working-code to run on utsa portal

# Load listing data
listing_df = pd.read_csv("/content/drive/My Drive/listings.csv")[:50]
# Load sentiment analysis data
sentiment_df = pd.read_csv("/content/drive/My Drive/sentiment_analysis_2023.csv")

# Function to calculate average sentiment for each aspect
def calculate_average_sentiment(row):
    listing_id = row['id']
    # Filter sentiment data for the current listing
    listing_sentiment = sentiment_df[sentiment_df['listing_id'] == listing_id][['listing_id', 'SentimentResults']]

    # Count the number of reviews for the current listing
    num_reviews = len(listing_sentiment)

    # Initialize a dictionary to store total sentiment values for each aspect
    total_sentiment = {}

    # Iterate over each review's sentiment results
    for index, review in listing_sentiment.iterrows():
        sentiment_results = eval(review['SentimentResults'])
        for aspect, sentiment_values in sentiment_results.items():
            if aspect not in total_sentiment:
                total_sentiment[aspect] = [0, 0, 0]  # Initialize [positive, negative, neutral]
            total_sentiment[aspect] = [x + y for x, y in zip(total_sentiment[aspect], sentiment_values)]

    # Calculate the average sentiment for each aspect
    average_sentiment = {}
    for aspect, sentiment_values in total_sentiment.items():
        if num_reviews != 0:
            average_sentiment[aspect] = [x / num_reviews for x in sentiment_values]
        else:
            average_sentiment[aspect] = [0, 0, 0]

    # Return the number of reviews and average sentiment values
    return pd.Series({'listing_id': listing_id, 'Number of Reviews': num_reviews, **average_sentiment})

# Apply the function to calculate average sentiment for each listing
average_sentiment_df = listing_df.apply(calculate_average_sentiment, axis=1)

# Reorder the columns so that 'listing_id' is the first column
columns = average_sentiment_df.columns.tolist()
columns = ['listing_id'] + [col for col in columns if col != 'listing_id']
average_sentiment_df = average_sentiment_df[columns]

# Write the results to a new CSV file
print("saving to file")
output_file = "/content/drive/My Drive/avg_sentiment_aspect_listing.csv"
average_sentiment_df.to_csv(output_file, index=False)
print("saved to file")

#working with entire listings data in output file

import pandas as pd

# Load listing data
listing_df = pd.read_csv("/content/drive/My Drive/listings.csv")[:50]

# Load sentiment analysis data
sentiment_df = pd.read_csv("/content/drive/My Drive/sentiment_analysis_2023.csv")

# Function to calculate average sentiment for each aspect
def calculate_average_sentiment(row):
    listing_id = row['id']
    # Filter sentiment data for the current listing
    listing_sentiment = sentiment_df[sentiment_df['listing_id'] == listing_id]
    print(listing_sentiment)
    # Count the number of reviews for the current listing
    num_reviews = len(listing_sentiment)

    # Initialize a dictionary to store total sentiment values for each aspect
    total_sentiment = {}
    # Iterate over each review's sentiment results
    for index, review in listing_sentiment.iterrows():
        sentiment_results = eval(review['SentimentResults'])
        for aspect, sentiment_values in sentiment_results.items():
            if aspect not in total_sentiment:
                total_sentiment[aspect] = [0, 0, 0]  # Initialize [positive, neutral, negative]
            total_sentiment[aspect] = [x + y for x, y in zip(total_sentiment[aspect], sentiment_values)]

    # Calculate the average sentiment for each aspect
    average_sentiment = {}
    for aspect, sentiment_values in total_sentiment.items():
        if num_reviews != 0:
            average_sentiment[aspect] = [x / num_reviews for x in sentiment_values]
        else:
            average_sentiment[aspect] = [0, 0, 0]

    # Return the number of reviews and average sentiment values
    return pd.Series({'Number of Reviews': num_reviews, **average_sentiment})

# Apply the function to calculate average sentiment for each listing
average_sentiment_df = listing_df.apply(calculate_average_sentiment, axis=1)

# Concatenate the result with the original DataFrame
output_df = pd.concat([listing_df, average_sentiment_df], axis=1)

# Write the results to a new CSV file
output_df.to_csv("/content/drive/My Drive/average_sentiment_per_aspect.csv", index=False)

