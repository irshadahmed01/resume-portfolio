import pandas as pd
import sqlite3

# Load and clean CSV
data = pd.read_csv('C:/investments_day7.csv')
data['Dollars Invested'] = data['Dollars Invested'].replace(r'[\$,]', '', regex=True).astype(float)
data['Current Value'] = data['Current Value'].replace(r'[\$,]', '', regex=True).astype(float)

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('C:/Users/notir/resume-portfolio/da/investments.db')

# Write the data to a table named 'investments'
data.to_sql('investments', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("Database 'investments.db' created successfully!")
