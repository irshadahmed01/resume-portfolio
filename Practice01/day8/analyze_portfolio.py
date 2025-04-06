import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file with the correct path
data = pd.read_csv('C:/Users/notir/resume-portfolio/Practice01/day7/investments_day7.csv')

# Clean the 'Current Value' column by removing $ and , and converting to float
data['Current Value'] = data['Current Value'].replace(r'[\$,]', '', regex=True).astype(float)

# Display basic summary statistics
print("Summary Statistics:")
print(data.describe())

# Group by Investment Type and calculate total Current Value
type_summary = data.groupby('Investment Type')['Current Value'].sum()
print("\nTotal Current Value by Investment Type:")
print(type_summary)

# Create a bar chart
plt.figure(figsize=(10, 6))
type_summary.plot(kind='bar', color='skyblue')
plt.title('Total Current Value by Investment Type')
plt.xlabel('Investment Type')
plt.ylabel('Total Current Value ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Save the grouped data to a new CSV file
type_summary.to_csv('C:/Users/notir/resume-portfolio/Practice01/day8/investment_type_summary.csv')