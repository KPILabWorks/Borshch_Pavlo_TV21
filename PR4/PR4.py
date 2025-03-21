# Практична робота №4
# Варіант №4
# Реалізуйте байєсівську регресію для моделювання залежностей між погодними умовами та енергоспоживанням. 
# Порівняйте отримані висновки з результатами, отриманими за допомогою класичної лінійної регресії.

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# --- Data Preparation (Simplified Synthetic Data) ---
np.random.seed(42)
n_samples = 200
temperature = np.random.normal(20, 5, n_samples)
energy_consumption = 50 - 2 * temperature + np.random.normal(0, 15, n_samples)  # Simplified: only temperature

data = pd.DataFrame({'temperature': temperature, 'energy_consumption': energy_consumption})
X = data[['temperature']]  # Only temperature as feature
y = data['energy_consumption']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Classical Linear Regression ---
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
y_pred_linear = linear_model.predict(X_test)
mse_linear = mean_squared_error(y_test, y_pred_linear)
r2_linear = r2_score(y_test, y_pred_linear)

print("--- Linear Regression ---")
print(f"Coeff: {linear_model.coef_[0]:.2f}, MSE: {mse_linear:.2f}, R2: {r2_linear:.2f}")

# --- Bayesian Regression ---
bayesian_model = BayesianRidge()
bayesian_model.fit(X_train, y_train)
y_pred_bayesian, y_std_bayesian = bayesian_model.predict(X_test, return_std=True)
mse_bayesian = mean_squared_error(y_test, y_pred_bayesian)
r2_bayesian = r2_score(y_test, y_pred_bayesian)

print("\n--- Bayesian Regression ---")
print(f"Coeff: {bayesian_model.coef_[0]:.2f}, MSE: {mse_bayesian:.2f}, R2: {r2_bayesian:.2f}")

# --- Basic Visualization ---
plt.figure(figsize=(8, 5))
plt.scatter(y_test, y_pred_linear, label='Linear', alpha=0.7)
plt.scatter(y_test, y_pred_bayesian, label='Bayesian', alpha=0.7)
plt.errorbar(y_test, y_pred_bayesian, yerr=y_std_bayesian, fmt='o', color='orange', alpha=0.3, label='Bayesian Uncertainty')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs. Predicted')
plt.legend()
plt.show()

# --- Basic Comparison ---
print("\n--- Comparison ---")
print(f"MSE: Linear={mse_linear:.2f}, Bayesian={mse_bayesian:.2f}")
print(f"R2:  Linear={r2_linear:.2f}, Bayesian={r2_bayesian:.2f}")
print("Bayesian regression also provides uncertainty estimates (see error bars).")