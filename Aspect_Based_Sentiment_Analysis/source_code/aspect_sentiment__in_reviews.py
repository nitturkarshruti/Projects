# -*- coding: utf-8 -*-
#!/bin/env python3
#import pdb
import pandas as pd
import ast

# Load aspect frequencies from aspect_frequency_output.csv
aspect_frequency_df = pd.read_csv('aspect_frequency_output.csv')

# Filter aspects with frequency greater than 5
selected_aspects = aspect_frequency_df[aspect_frequency_df['Frequency'] > 1000]['Aspect'].tolist()

# Load sentiment analysis results
sentiment_analysis_df = pd.read_csv('sentiment_analysis_2023.csv')

# Function to determine sentiment of an aspect in a review
def get_aspect_sentiment(aspect, review):
    try:
        sentiment_scores = ast.literal_eval(review)
        if aspect in sentiment_scores:
            sentiment = sentiment_scores[aspect]
            if sentiment[0] > 0:  # Positive sentiment
                return 1
            elif sentiment[1] > 0:  # Negative sentiment
                return -1
            else:
                return 0  # Neutral sentiment
        else:
            return "Unused"
    except Exception as e:
        print('Error:', e)
        return "Unused"

# Create list to store DataFrames for each aspect
aspect_sentiments_dfs = []

# Iterate over each selected aspect and determine its sentiment for each review
for aspect in selected_aspects:
    aspect_sentiments_df = sentiment_analysis_df.iloc[:, 8].map(lambda review: get_aspect_sentiment(aspect, review))
    aspect_sentiments_dfs.append(pd.DataFrame({aspect: aspect_sentiments_df}))

# Concatenate all DataFrames along axis=1
aspect_sentiments_df = aspect_sentiments_dfs[0]
for df in aspect_sentiments_dfs[1:]:
    aspect_sentiments_df = aspect_sentiments_df.join(df)

# Add the 7th column from sentiment_analysis_2023.csv as the first column
aspect_sentiments_df.insert(0, 'comments', sentiment_analysis_df.iloc[:, 6])
print("saving to csv")
# Save the output to a new CSV file
output_csv_path = 'aspect_sentiments_output.csv'
aspect_sentiments_df.to_csv(output_csv_path, index=False)

print("Aspect sentiments saved to:", output_csv_path)