import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("Primary_CallReports_v1.4.csv")

# Group by Year&Month and calculate total calls per month
monthly_calls = df.groupby("Year&Month").size().reset_index(name="TotalCalls")

# Merge with unemployment rate (assuming it’s constant per month in the dataset)
monthly_rates = df[["Year&Month", "AlbertaUnemploymentRate"]].drop_duplicates()
combined = pd.merge(monthly_calls, monthly_rates, on="Year&Month")

# Plot
plt.figure(figsize=(10, 6))
sns.regplot(data=combined, x="AlbertaUnemploymentRate", y="TotalCalls", ci=None, scatter_kws={"s": 50})
plt.title("Unemployment Rate vs Total Distress Line Calls per Month")
plt.xlabel("Alberta Unemployment Rate (%)")
plt.ylabel("Total Calls per Month")
plt.grid(True)
plt.tight_layout()

# Save the figure as PNG
plt.savefig("unemployment_vs_calls.png", dpi=300)

# Show the plot
plt.show()
