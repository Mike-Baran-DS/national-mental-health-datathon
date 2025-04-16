# This script modifies the input dataset by deleting the 'labels' column,
	# and # Truncating the 'Date' column to YYYY-MM

import pandas as pd

# Load the CSV
df = pd.read_csv("Unemployment Rate Alberta.csv", dtype={"Date": str})

# Drop the 'labels' column
df.drop(columns=["labels"], inplace=True)

# Truncate the 'Date' column to YYYY-MM
df["Date"] = df["Date"].str[:7]

# Save to new CSV
df.to_csv("Unemployment_Rate_Alberta_Cleaned.csv", index=False)

print("Cleaned file saved as 'Unemployment_Rate_Alberta_Cleaned.csv'")
