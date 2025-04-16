import pandas as pd

# Read the CSV file
df = pd.read_csv('Primary_CallReports_v1.5.csv')

# Convert 'Year&Month' to datetime
df['Year&Month'] = pd.to_datetime(df['Year&Month'], format='%y-%b')

# Create new column with 'YYYY Q#' format
df['Quarter'] = df['Year&Month'].dt.year.astype(str) + ' Q' + df['Year&Month'].dt.quarter.astype(str)

# Save the result to a new CSV
df.to_csv('test.csv', index=False)


