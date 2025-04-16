import pandas as pd

# Load the datasets
primary_df = pd.read_csv('Primary_CallReports_v1.6.csv')
opioid_df = pd.read_csv('OpiodEMSResponsesAlberta.csv')

# Select only relevant columns and rename for clarity
opioid_df = opioid_df[['Year_Quarter', 'Value']].rename(columns={'Year_Quarter': 'Quarter', 'Value': 'OpiodEMSResponsesAB'})

# Merge on 'Quarter' with a left join
merged_df = pd.merge(primary_df, opioid_df, on='Quarter', how='left')

# Save the output as version 1.7
merged_df.to_csv('Primary_CallReports_v1.7.csv', index=False)

# Preview a few rows
print(merged_df.head())
