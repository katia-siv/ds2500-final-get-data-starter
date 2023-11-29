#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def predict_2023_number(df):
    '''
    Extracts the "Year" and "Number" columns from the
    input DataFrame. Creates a LinearRegression model,
    fits the model to the data, and uses it to predict
    the Number for 2023. 
    '''
    X = df['Year'].values.reshape(-1, 1)
    y = df['Number'].values
    model = LinearRegression()
    model.fit(X, y)
    prediction_2023 = model.predict(np.array([[2023]]))
    return prediction_2023[0]

def plot_data_and_prediction(df, prediction_2023, title):
    '''
    Creates a plot with the historical data and the
    prediction for 2023. Plots title, axis labels, and a
    legend.
    '''
    X = df['Year'].values
    y = df['Number'].values

    plt.plot(X, y, label='Historical Data')
    plt.scatter(2023, prediction_2023, color='red', label='Prediction for 2023')

    plt.xlabel('Year')
    plt.ylabel('Number of People')
    plt.title(title)
    plt.legend()

    plt.show()
    
def main():
    
    prediction_2023 = predict_2023_number(df)
    # Plot Data with Prediction
    title = "Prediction: persons obtaining lawful permanent resident status"
    plot_data_and_prediction(df, prediction_2023, title)
    
if __name__ == "__main__":
    main()
    
