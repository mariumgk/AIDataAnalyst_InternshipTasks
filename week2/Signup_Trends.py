import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("cleaned_data_final.csv")

# Parse signup datetime and drop invalid entries
df['Learner SignUp DateTime'] = pd.to_datetime(df['Learner SignUp DateTime'], errors='coerce')
df = df.dropna(subset=['Learner SignUp DateTime'])

# Prepare time series data
df['MonthYear'] = df['Learner SignUp DateTime'].dt.to_period('M').astype(str)
monthly_counts = df['MonthYear'].value_counts().sort_index()

# 1. Growth: bar chart of monthly signups
plt.figure(figsize=(12, 5))
plt.bar(monthly_counts.index, monthly_counts.values)
plt.title("Monthly Signup Growth")
plt.xlabel("Month-Year")
plt.ylabel("Number of Signups")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Seasonality: heatmap of signups by month and year
df['Year'] = df['Learner SignUp DateTime'].dt.year
df['MonthNum'] = df['Learner SignUp DateTime'].dt.month
season_pivot = df.groupby(['Year', 'MonthNum']).size().unstack(fill_value=0)
plt.figure(figsize=(10, 6))
plt.imshow(season_pivot, aspect='auto')
plt.colorbar(label='Number of Signups')
plt.title("Signup Seasonality Heatmap")
plt.xlabel("Month (1=Jan, 12=Dec)")
plt.ylabel("Year")
plt.xticks(ticks=range(12), labels=list(range(1, 13)))
plt.yticks(ticks=range(len(season_pivot.index)), labels=season_pivot.index)
plt.tight_layout()
plt.show()

# 3. Spikes/Drops: identify and plot
diff = monthly_counts.diff()
max_spike = diff.idxmax()
max_drop = diff.idxmin()
max_spike_val = int(diff[max_spike])
max_drop_val = int(diff[max_drop])

print(f"Largest increase (spike) in signups: {max_spike} (+{max_spike_val})")
print(f"Largest decrease (drop) in signups: {max_drop} ({max_drop_val})")

plt.figure(figsize=(12, 5))
plt.plot(monthly_counts.index, monthly_counts.values, marker='o')
plt.title("Monthly Signups with Spikes and Drops")
plt.xlabel("Month-Year")
plt.ylabel("Number of Signups")
plt.xticks(rotation=45)
# Annotate spike and drop points
plt.annotate('Spike', xy=(max_spike, monthly_counts[max_spike]), xytext=(0, 20), textcoords='offset points', arrowprops=dict(arrowstyle='->'))
plt.annotate('Drop', xy=(max_drop, monthly_counts[max_drop]), xytext=(0, -30), textcoords='offset points', arrowprops=dict(arrowstyle='->'))
plt.tight_layout()
plt.show()
