import pandas as pd

# Load the datasets
calls_df = pd.read_csv('Primary_CallReports_v1.4.csv')
weather_df = pd.read_csv('edmonton_daily_weather.csv')

# Convert date columns to string and extract the first 10 characters (assumed to be YYYY-MM-DD)
calls_df['date_key'] = calls_df['CallDateAndTimeStart'].astype(str).str[:10]
weather_df['date_key'] = weather_df['date'].astype(str).str[:10]

# Merge datasets, retaining all rows from calls_df (left join)
merged_df = pd.merge(calls_df, weather_df, on='date_key', how='left')

# Drop the join key if not needed
merged_df.drop(columns=['date_key'], inplace=True)

# Export the result to CSV
merged_df.to_csv('test.csv', index=False)
