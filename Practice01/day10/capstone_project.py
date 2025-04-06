import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

# Load cleaned data
data = pd.read_csv(r'C:\Users\notir\resume-portfolio\Practice01\day9\investments_day9_cleaned.csv')

# Data Cleaning Recap (already done in Day 9, just verifying)
print("Verifying Cleaned Data - Missing Values:")
print(data.isnull().sum())

# Predictive Modeling (Linear and Polynomial Regression)
X = data[['Dollars Invested', 'Row Number']]
y = data['Current Value']

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X, y)
linear_predictions = linear_model.predict(X)
linear_mse = mean_squared_error(y, linear_predictions)

# Polynomial Regression
poly_features = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly_features.fit_transform(X)
poly_model = LinearRegression()
poly_model.fit(X_poly, y)
poly_predictions = poly_model.predict(X_poly)
poly_mse = mean_squared_error(y, poly_predictions)

# Predict next 5 investments (assuming $1,000 invested each)
new_X = pd.DataFrame({'Dollars Invested': np.full(5, 1000), 'Row Number': range(101, 106)})
new_X_poly = poly_features.transform(new_X)
new_linear_predictions = linear_model.predict(new_X)
new_poly_predictions = poly_model.predict(new_X_poly)

print(f"\nLinear Regression MSE: {linear_mse:.2f}")
print(f"Polynomial Regression MSE: {poly_mse:.2f}")
print("\nPredicted Values for Next 5 Investments:")
print("Linear Regression:")
for i, pred in enumerate(new_linear_predictions, 101):
    print(f"Investment {i}: ${pred:.2f}")
print("Polynomial Regression:")
for i, pred in enumerate(new_poly_predictions, 101):
    print(f"Investment {i}: ${pred:.2f}")

# Visualization 1: Total Current Value by Investment Name
type_summary = data.groupby('Investment Name')['Current Value'].sum()
plt.figure(figsize=(10, 6))
type_summary.plot(kind='bar', color='skyblue')
plt.title('Total Current Value by Investment Name')
plt.xlabel('Investment Name')
plt.ylabel('Total Current Value ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('C:/Users/notir/resume-portfolio/Practice01/day10/total_value_by_name.png')
plt.close()

# Visualization 2: Value Category Distribution
category_counts = data['Value Category'].value_counts()
plt.figure(figsize=(8, 5))
category_counts.plot(kind='bar', color='lightgreen')
plt.title('Distribution of Value Categories')
plt.xlabel('Value Category')
plt.ylabel('Count')
plt.savefig('C:/Users/notir/resume-portfolio/Practice01/day10/value_category_distribution.png')
plt.close()

# SQL Query for Insights (using case-insensitive column names)
conn = sqlite3.connect('C:/Users/notir/resume-portfolio/Practice01/day9/investments.db')
query = """
    SELECT "Investment Name", AVG("Current Value") as Avg_Value, AVG("Normalized Growth") as Avg_Growth
    FROM investments_cleaned
    GROUP BY "Investment Name"
    ORDER BY Avg_Value DESC
    LIMIT 10
"""
sql_data = pd.read_sql_query(query, conn)
print("\nSQL Insights - Average Value and Growth by Investment Name:")
print(sql_data)
conn.close()

# Save combined results
results = pd.DataFrame({
    'Investment_Name': sql_data['Investment Name'],
    'Avg_Value': sql_data['Avg_Value'],
    'Avg_Growth': sql_data['Avg_Growth'],
    'Linear_Prediction_101': new_linear_predictions[0],
    'Poly_Prediction_101': new_poly_predictions[0]
})
results.to_csv('C:/Users/notir/resume-portfolio/Practice01/day10/capstone_results.csv', index=False)
print(f"\nResults saved to capstone_results.csv")