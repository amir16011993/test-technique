import pandas as pd
from datetime import datetime

df = pd.read_csv("C:\Users\MSI GP 66\Downloads\bq-results-20231220-134345-1703079855754.csv")

# Filter engagements that occurred in 2023
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'].dt.year == 2023]

# Group by user and topic, then calculate the engagement count for each type
grouped_df = df.groupby(['scv_id', 'topic', 'source_system']).size().reset_index(name='engagement_count')

# Pivot the DataFrame to have source_systems as columns
pivoted_df = grouped_df.pivot_table(index=['scv_id', 'topic'], columns='source_system', values='engagement_count', fill_value=0).reset_index()

# Calculate the total engagement for each user-topic combination
pivoted_df['total_engagement'] = pivoted_df['Activecampaign'] + pivoted_df['Catalogue'] + pivoted_df['PX']

# Calculate the topic affinity score
pivoted_df['topic_affinity_score'] = 10 * (pivoted_df['total_engagement'] / pivoted_df['total_engagement'].max())

# Drop unnecessary columns
result_df = pivoted_df[['scv_id', 'topic', 'topic_affinity_score']]

# Save the result to a CSV file
result_df.to_csv('topic_affinity_scores.csv', index=False)
