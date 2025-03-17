import pandas as pd

# Define file paths
sentiment_file_path = 'sentiment_analysis_2023.csv'
aspect_frequency_file_path = 'aspect_frequency_filtered.csv'

# Read sentiment analysis data
sentiment_df = pd.read_csv(sentiment_file_path)

# Read aspect frequency data
aspect_frequency_df = pd.read_csv(aspect_frequency_file_path)

# Initialize dictionaries to store review counts for each aspect
total_reviews = {}
positive_reviews = {}
negative_reviews = {}

# Iterate over each row in sentiment analysis data
for index, row in sentiment_df.iterrows():
    sentiment_results = eval(row['SentimentResults'])
    #print(sentiment_results)
    for aspect, sentiment_values in sentiment_results.items():
        # Check if the aspect is present in aspect frequency data
        if aspect in aspect_frequency_df['Aspect'].values:
            # Update total reviews count for the aspect
            total_reviews[aspect] = total_reviews.get(aspect, 0) + 1
            # Update positive and negative reviews counts
            if sentiment_values[0] == 1:
                positive_reviews[aspect] = positive_reviews.get(aspect, 0) + 1
            elif sentiment_values[1] == 1:
                negative_reviews[aspect] = negative_reviews.get(aspect, 0) + 1

# Create DataFrame from the dictionaries
review_counts_df = pd.DataFrame({'Aspect': list(total_reviews.keys()),
                                 'Total Reviews': list(total_reviews.values()),
                                 'Positive Reviews': [positive_reviews.get(aspect, 0) for aspect in total_reviews.keys()],
                                 'Negative Reviews': [negative_reviews.get(aspect, 0) for aspect in total_reviews.keys()]})

# Save the DataFrame to a CSV file
output_file_path = 'aspect_review_counts.csv'
review_counts_df.to_csv(output_file_path, index=False)

print("Review counts saved successfully!")
