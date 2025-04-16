import pandas as pd

# Load the merged dataset
df = pd.read_csv('Primary_CallReports_v1.7.csv')

# Group by Year&Month and Quarter to count calls per month
monthly_calls = df.groupby(['Year&Month', 'Quarter'])['CallReportNum'].count().reset_index()
monthly_calls.rename(columns={'CallReportNum': 'TotalCalls'}, inplace=True)

# Keep only unique Quarter-to-OpiodEMSResponsesAB mapping
opioid_by_quarter = df[['Quarter', 'QuarterlyOpioidEMSResponsesAB']].drop_duplicates()

# Merge the call counts with opioid data
monthly_data = pd.merge(monthly_calls, opioid_by_quarter, on='Quarter', how='left')

# Check correlation
correlation = monthly_data['TotalCalls'].corr(monthly_data['QuarterlyOpioidEMSResponsesAB'])

# Print results
print(monthly_data)
print(f"\nCorrelation between monthly total calls and quarterly opioid EMS responses: {correlation:.4f}")

import matplotlib.pyplot as plt
import seaborn as sns

sns.scatterplot(x='QuarterlyOpioidEMSResponsesAB', y='TotalCalls', data=monthly_data)
plt.title('Monthly Call Volume vs Quarterly Opioid EMS Responses')
plt.xlabel('Quarterly Opioid EMS Responses (AB)')
plt.ylabel('Monthly Total Calls')
plt.grid(True)
plt.tight_layout()
plt.show()
