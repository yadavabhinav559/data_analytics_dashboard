import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("business_kpi.csv")

# Convert 'Date' column to datetime format for plotting
df["Date"] = pd.to_datetime(df["Date"])

# Set style for Seaborn plots
sns.set_theme(style="darkgrid")

# Create a revenue vs expenses trend plot
plt.figure(figsize=(10, 5))
sns.lineplot(x=df["Date"], y=df["Revenue"], label="Revenue", marker="o")
sns.lineplot(x=df["Date"], y=df["Expenses"], label="Expenses", marker="o")

# Format the chart
plt.xticks(rotation=45)
plt.title("Revenue vs Expenses Over Time")
plt.xlabel("Date")
plt.ylabel("Amount ($)")
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
 
