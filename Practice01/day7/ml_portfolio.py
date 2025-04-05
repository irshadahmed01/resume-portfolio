import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load and clean data
data = pd.read_csv('C:/Users/notir/resume-portfolio/da/investments_day7.csv')

# Clean the 'Dollars Invested' and 'Current Value' columns
data['Dollars Invested'] = data['Dollars Invested'].replace(r'[\$,]', '', regex=True).astype(float)
data['Current Value'] = data['Current Value'].replace(r'[\$,]', '', regex=True).astype(float)

# Prepare features and target
X = data[['Dollars Invested', 'Row Number']]
y = data['Current Value']

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict for new data (e.g., next 10 investments with increasing Row Number)
new_investments_df = pd.DataFrame({
    'Dollars Invested': np.full(10, 1000),
    'Row Number': range(101, 111)
})
predictions = model.predict(new_investments_df)

# Print predictions
print("Predicted Current Values for next 10 investments:")
for i, pred in enumerate(predictions, 101):
    print(f"Investment {i}: ${pred:.2f}")

# Visualize
plt.scatter(X['Row Number'], y, color='blue', label='Actual')
plt.plot(new_investments_df['Row Number'], predictions, color='red', label='Predicted')
plt.xlabel('Row Number')
plt.ylabel('Current Value ($)')
plt.title('Linear Regression Prediction')
plt.legend()
plt.show()

# Save predictions to CSV
predictions_df = pd.DataFrame({'Row Number': range(101, 111), 'Predicted Value': predictions})
predictions_df.to_csv('C:/Users/notir/resume-portfolio/da/ml_predictions.csv', index=False)