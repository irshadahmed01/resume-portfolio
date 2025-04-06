import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load and clean data
data = pd.read_csv('C:/Users/notir/resume-portfolio/Practice01/day7/investments_day7.csv')
data['Dollars Invested'] = data['Dollars Invested'].replace(r'[\$,]', '', regex=True).astype(float)
data['Current Value'] = data['Current Value'].replace(r'[\$,]', '', regex=True).astype(float)

# Prepare features and target
X = data[['Dollars Invested', 'Row Number']]
y = data['Current Value']

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X, y)
linear_predictions = linear_model.predict(X)

# Polynomial Regression (Degree 2)
poly_features = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly_features.fit_transform(X)
poly_model = LinearRegression()
poly_model.fit(X_poly, y)
poly_predictions = poly_model.predict(X_poly)

# New predictions for next 10 investments
new_X = pd.DataFrame({
    'Dollars Invested': np.full(10, 1000),
    'Row Number': range(101, 111)
})
new_X_poly = poly_features.transform(new_X)
new_linear_predictions = linear_model.predict(new_X)
new_poly_predictions = poly_model.predict(new_X_poly)

# Evaluate models
linear_mse = mean_squared_error(y, linear_predictions)
poly_mse = mean_squared_error(y, poly_predictions)
print(f"Linear Regression MSE: {linear_mse:.2f}")
print(f"Polynomial Regression MSE: {poly_mse:.2f}")

# Print new predictions
print("\nPredicted Current Values for next 10 investments:")
print("Linear Regression:")
for i, pred in enumerate(new_linear_predictions, 101):
    print(f"Investment {i}: ${pred:.2f}")
print("Polynomial Regression:")
for i, pred in enumerate(new_poly_predictions, 101):
    print(f"Investment {i}: ${pred:.2f}")

# Visualize and save plot
plt.figure(figsize=(12, 6))
plt.scatter(data['Row Number'], y, color='blue', label='Actual Data')
plt.plot(data['Row Number'], linear_predictions, color='red', label='Linear Prediction')
plt.plot(data['Row Number'], poly_predictions, color='green', label='Polynomial Prediction')
plt.plot(new_X['Row Number'], new_linear_predictions, '--r', label='Linear Future Prediction')
plt.plot(new_X['Row Number'], new_poly_predictions, '--g', label='Polynomial Future Prediction')
plt.xlabel('Row Number')
plt.ylabel('Current Value ($)')
plt.title('Linear vs. Polynomial Regression')
plt.legend()
plt.grid(True)
plt.savefig('C:/Users/notir/resume-portfolio/Practice01/day8/linear_vs_poly.png')
plt.show()

# Save predictions to CSV
predictions_df = pd.DataFrame({
    'Row Number': range(101, 111),
    'Linear Prediction': new_linear_predictions,
    'Polynomial Prediction': new_poly_predictions
})
predictions_df.to_csv('C:/Users/notir/resume-portfolio/Practice01/day8/ml_advanced_predictions.csv', index=False)
print("Predictions saved to ml_advanced_predictions.csv")