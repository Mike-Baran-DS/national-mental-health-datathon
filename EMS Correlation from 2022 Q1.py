import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the merged dataset
df = pd.read_csv('Primary_CallReports_v1.7.csv')

# Filter to include only data from 2022 Q1 onwards
df = df[df['Quarter'] >= '2022 Q1']

# Group by Year&Month and Quarter to count calls per month
monthly_calls = df.groupby(['Year&Month', 'Quarter'])['CallReportNum'].count().reset_index()
monthly_calls.rename(columns={'CallReportNum': 'TotalCalls'}, inplace=True)

# Get unique values for opioid responses per quarter
opioid_by_quarter = df[['Quarter', 'QuarterlyOpioidEMSResponsesAB']].drop_duplicates()

# Merge the grouped calls with the opioid EMS responses
monthly_data = pd.merge(monthly_calls, opioid_by_quarter, on='Quarter', how='left')

# Calculate correlation
correlation = monthly_data['TotalCalls'].corr(monthly_data['QuarterlyOpioidEMSResponsesAB'])

# Print results
print(monthly_data)
print(f"\nCorrelation between monthly total calls and quarterly opioid EMS responses (2022 Q1+): {correlation:.4f}")

# Optional: plot the relationship
sns.scatterplot(x='QuarterlyOpioidEMSResponsesAB', y='TotalCalls', data=monthly_data)
plt.title('Monthly Call Volume vs Quarterly Opioid EMS Responses (2022 Q1+)')
plt.xlabel('Quarterly Opioid EMS Responses (AB)')
plt.ylabel('Monthly Total Calls')
plt.grid(True)
plt.tight_layout()
plt.show()
