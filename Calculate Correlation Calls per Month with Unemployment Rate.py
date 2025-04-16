import pandas as pd
from scipy.stats import pearsonr  # or spearmanr if data isn't normally distributed

# Load your CSV file
df = pd.read_csv("Primary_CallReports_v1.4.csv")

# Step 1: Group by 'Year&Month' and count number of calls
monthly_calls = df.groupby("Year&Month").size().reset_index(name='TotalCalls')

# Step 2: Get the unique unemployment rate per month
unemployment_rate = df.groupby("Year&Month")["AlbertaUnemploymentRate"].first().reset_index()

# Step 3: Merge the two dataframes
merged = pd.merge(monthly_calls, unemployment_rate, on="Year&Month")

# Step 4: Correlation between TotalCalls and AlbertaUnemploymentRate
corr, p_value = pearsonr(merged['TotalCalls'], merged['AlbertaUnemploymentRate'])

# Output the results
print("Monthly Call Volumes with Unemployment Rate:\n", merged)
print(f"\nCorrelation Coefficient: {corr:.4f}")
print(f"P-value: {p_value:.4f}")
