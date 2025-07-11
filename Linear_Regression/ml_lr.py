# -*- coding: utf-8 -*-
"""ml LR.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I-thUKYJV506eNZo4t03Jq_NdgBicoRb
"""

# Loading the libraries and functions
from pandas import read_csv, DataFrame
from plotly import figure_factory
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV

data=read_csv('/content/House_Rent_Dataset.csv')

data.shape

data.head()

data.info()

data['Posted On'].unique()

import pandas as pd
data['Posted On'] = pd.to_datetime(data['Posted On'], errors='coerce')
data['Posted On'] = data['Posted On'].dt.strftime('%Y%m%d').astype(int)

data['BHK'].unique()

data['Size'].unique()

data['Floor'].unique()

data['Floor'].value_counts()

import pandas as pd
# Extract the numeric part from each value in the 'Floor' column
data['Floor'] = data['Floor'].str.split().str[0]
data['Floor'] = pd.to_numeric(data['Floor'], errors='coerce')
data['Floor'].fillna(0, inplace=True)

data['Floor'].unique()

data['Area Type'].unique()

data['Area Type'] = data['Area Type'].map({'Super Area':1,'Carpet Area':2,'Built Area':3})

data['Area Locality'].unique()

data['Area Locality'] = data['Area Locality'].str.split().str[0]
data['Area Locality'] = pd.to_numeric(data['Area Locality'], errors='coerce')
data['Area Locality'].fillna(0, inplace=True)

data['City'].unique()

data['City']=data['City'].map({'Mumbai':1,'Bangalore':2,'Chennai':3,'Hyderabad':4,'Delhi':5,'Kolkata':6})

data['Furnishing Status'].unique()

data['Furnishing Status']=data['Furnishing Status'].map({'Unfurnished':1,'Semi-Furnished':2,'Furnished':3})

data['Tenant Preferred'].unique()

data['Tenant Preferred']=data['Tenant Preferred'].map({'Bachelors/Family':1,'Bachelors':2,'Family':3})

data['Bathroom'].unique()

data['Point of Contact'].unique()

data['Point of Contact']=data['Point of Contact'].map({'Contact Owner':1,'Contact Agent':2,'Contact Builder':3})

data['Unnamed: 11'].unique()

data['Rent'].unique()

data1 = data.drop(['Unnamed: 11'], axis=1)

data1.info()

cor=data1.corr()
f=figure_factory.create_annotated_heatmap(cor.values,list(cor.columns),list(cor.columns),cor.round(2).values,showscale=True)
f.show()

# import numpy as np
# cor=data1.corr().abs()
# upper=cor.where(np.triu(np.ones(cor.shape),k=1).astype(bool))
# to_drop=[column for column in upper.columns if any(upper[column]>0.7)]
# data_reduced=data1.drop(columns=to_drop)
# print(to_drop)

data1= data1.drop(['Size','Bathroom'],axis=1)
data1.info()

X = data1.drop(['Rent'],axis=1)
Y = data1['Rent']

X_st=StandardScaler().fit_transform(X)

# Linear Regression
LR=linear_model.SGDRegressor(random_state=1,penalty=None) # Linear regression without the regularisation
hyper_param={'eta0':[0.001,0.01,0.1,1],'max_iter':[1000,2000,3000,4000]}
grid_search=GridSearchCV(estimator=LR,param_grid=hyper_param,scoring='r2',cv=5) # R^2 tells how the good the linear model has fitted the dataset.
grid_search.fit(X_st,Y) # Fitting the linear model

print("Best Hyperparameters:", grid_search.best_params_)
print("Best R² Score:", grid_search.best_score_)

# Optimal parameters
best_params= grid_search.best_params_
print(best_params)
best_result=grid_search.best_score_
print(best_result)
best_model=grid_search.best_estimator_
print('Beta_0:',best_model.intercept_)
#best_model.coef_
print(DataFrame(zip(X.columns,best_model.coef_),columns=['Columns/features','Beta coefficients']))

"""regularisation

"""

# Adding the penalty in the model
LR1=linear_model.SGDRegressor(random_state=1,penalty='elasticnet') # Linear regression without the regularisation
hyper_param={'eta0':[0.001,0.01,0.1,1],'max_iter':[1000,2000,3000,4000],'alpha':[0.001,0.01,0.1,1],'l1_ratio':[0.2,0.25,0.4,0.5,0.75,1]}
grid_search=GridSearchCV(estimator=LR1,param_grid=hyper_param,scoring='r2',cv=5) # R^2 tells how the good the linear model has fitted the dataset.
grid_search.fit(X_st,Y) # Fitting the linear model

# Optimal parameters
best_params= grid_search.best_params_
print(best_params)
best_result=grid_search.best_score_
print(best_result)
best_model=grid_search.best_estimator_
print('Beta_0:',best_model.intercept_)
#best_model.coef_
print(DataFrame(zip(X.columns,best_model.coef_),columns=['Columns/features','Beta coefficients']))

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pandas as pd

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, Y_train, Y_test = train_test_split(X_st, Y, test_size=0.2, random_state=1)

# Train the best model on the training data
best_model.fit(X_train, Y_train)

# Predict on the test set
Y_pred = best_model.predict(X_test)

# Calculate and print regression evaluation metrics
mae = mean_absolute_error(Y_test, Y_pred)
mse = mean_squared_error(Y_test, Y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(Y_test, Y_pred)

print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("R-squared (R²):", r2)

# Optional: Compare predictions vs true values visually
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(Y_test, Y_pred, color='blue', alpha=0.6, label="Predicted vs True")
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2, label="Perfect Fit")
plt.xlabel("True Values (Y_test)")
plt.ylabel("Predicted Values (Y_pred)")
plt.title("Regression Model Predictions vs. True Values")
plt.legend()
plt.show()

"""Prediction/Forecasting"""

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDRegressor

# Define the model
LR2 = SGDRegressor(penalty='elasticnet', random_state=42, max_iter=1000)

# Define the parameter grid to search
param_grid = {
    'alpha': [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0],
    'eta0': [0.00001, 0.0001, 0.001, 0.01, 0.1],
    'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9]
}

# Use GridSearchCV to find the best combination of parameters
grid_search = GridSearchCV(LR2, param_grid, scoring='r2', cv=5)
grid_search.fit(X_st, Y)

# Best parameters and score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best parameters:", best_params)
print("Best cross-validated R^2 score:", best_score)

LR2=linear_model.SGDRegressor(random_state=42,penalty='elasticnet',alpha=1.0, eta0=1e-05, l1_ratio= 0.1, max_iter=1000) # Fitting the Linear model with boptimised parameters

LR22=linear_model.SGDRegressor(random_state=42,penalty='l2',alpha=1.0, eta0=0.0001, max_iter=3000) # Fitting the Linear model with boptimised parameters

LR22=linear_model.SGDRegressor(random_state=42,penalty='l1',alpha=1.0, eta0=0.0001, max_iter=3000) # Fitting the Linear model with boptimised parameters

LR22=linear_model.SGDRegressor(random_state=42,penalty=None,alpha=1.0, eta0=0.0001, max_iter=3000) # Fitting the Linear model with boptimised parameters



# LR22.fit(X_st,Y)# Fitting the Linear model with penalty elasticnet and using the bestparameters from GridsearchCV
# LR22.score(X_st,Y) # R^2 score tells how much variation in the dependent variable is explained by independent variable, i.e., 76% of variation in Price is explained by independent variables in the dataset.

LR2.fit(X_st,Y)# Fitting the Linear model with penalty elasticnet and using the bestparameters from GridsearchCV
LR2.score(X_st,Y) # R^2 score tells how much variation in the dependent variable is explained by independent variable, i.e., 76% of variation in Price is explained by independent variables in the dataset.

LR2.predict(X[:10]) # Prediction of first 10 rows in the dataset

X[:10]