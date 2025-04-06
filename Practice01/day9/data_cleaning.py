import pandas as pd
import numpy as np
import sqlite3

# Load the data with a raw string to handle the Windows path correctly
data = pd.read_csv(r'C:\Users\notir\resume-portfolio\Practice01\day7\investments_day7.csv')

# Step 1: Handle Missing Values
print("Initial Missing Values:")
print(data.isnull().sum())
data['Current Value'] = data['Current Value'].replace(r'[\$,]', '', regex=True).astype(float)
data['Dollars Invested'] = data['Dollars Invested'].replace(r'[\$,]', '', regex=True).astype(float)
data['Growth %'] = data['Growth %'].replace(r'[%]', '', regex=True).astype(float)
data = data.fillna({
    'Current Value': data['Current Value'].mean(),
    'Dollars Invested': data['Dollars Invested'].mean(),
    'Growth %': data['Growth %'].mean()
})
print("\nMissing Values After Imputation:")
print(data.isnull().sum())

# Step 2: Remove Duplicates
duplicates = data.duplicated().sum()
print(f"\nNumber of Duplicate Rows: {duplicates}")
data = data.drop_duplicates()
print(f"Number of Rows After Removing Duplicates: {len(data)}")

# Step 3: Handle Outliers (using IQR method for Current Value)
Q1 = data['Current Value'].quantile(0.25)
Q3 = data['Current Value'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = data[(data['Current Value'] < lower_bound) | (data['Current Value'] > upper_bound)]
print(f"\nOutliers in Current Value: {len(outliers)}")
data = data[(data['Current Value'] >= lower_bound) & (data['Current Value'] <= upper_bound)]

# Step 4: Transform Data
# Normalize Growth % to a 0-1 scale
data['Normalized Growth'] = (data['Growth %'] - data['Growth %'].min()) / (data['Growth %'].max() - data['Growth %'].min())
# Categorize Investments (e.g., High, Medium, Low based on Current Value)
data['Value Category'] = pd.qcut(data['Current Value'], q=3, labels=['Low', 'Medium', 'High'])
print("\nFirst Few Rows After Transformation:")
print(data.head())

# Step 5: Save Cleaned Data
cleaned_file = 'C:/Users/notir/resume-portfolio/Practice01/day9/investments_day9_cleaned.csv'
data.to_csv(cleaned_file, index=False)
print(f"\nCleaned data saved to {cleaned_file}")

# Step 6: Update SQL Database
conn = sqlite3.connect('C:/Users/notir/resume-portfolio/Practice01/day9/investments.db')
data.to_sql('investments_cleaned', conn, if_exists='replace', index=False)
conn.close()
print("Updated SQL database with cleaned data.")