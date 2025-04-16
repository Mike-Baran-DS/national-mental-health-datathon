import pandas as pd

# Load both CSVs
calls_df = pd.read_csv("Primary_CallReports_v1.3.csv")
unemp_df = pd.read_csv("Unemployment_Rate_Alberta_Cleaned.csv")

# Create a new column for join key in calls_df
calls_df["Year&Month"] = calls_df["CallDateAndTimeStart"].astype(str).str[:7].str.strip()

# Rename columns in the unemployment DataFrame
unemp_df.rename(columns={"Date": "Year&Month", "Value": "AlbertaUnemploymentRate"}, inplace=True)

# Perform left join
merged_df = pd.merge(calls_df, unemp_df, on="Year&Month", how="left")

# Save to new version
merged_df.to_csv("Primary_CallReports_v1.4.csv", index=False)

print("✅ Merged file saved as 'Primary_CallReports_v1.4.csv'")
