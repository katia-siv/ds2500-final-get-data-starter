#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
# Set the global font to be Times New Roman
plt.rcParams["font.family"] = "Times New Roman"

DIRECTORY = "/Users/ekaterinasivokon/Desktop/ds2500-final-get-data-starter/2023_0818_plcy_yearbook_lawful_permanent_residents_fy2022.xlsx_0.xlsx"


def excel_to_dataframe(directory):
    '''
    Takes the path to an Excel file as input, reads the data from the second 
    sheet (indexed at 1), skips the first 5 rows as header, converts into a 
    pandas DataFrame. Removes rows where all values are NaN & resets the index
    of DataFrame. 
    '''
    df = pd.read_excel(directory, sheet_name=1, header=5)
    df.columns = df.columns.get_level_values(0)
    # Remove rows with all NaN values
    df = df.dropna(how='all')
    # Reset index
    df = df.reset_index(drop=True)
    return df


def clean_dataframe(df):
    '''
    Takes DataFrame as input, combines all columns with 'Year' in their names
    into a single 'Year' column and all columns with 'Number' in their names
    into a single 'Number' column. Creates new DataFrame (df_clean) with the
    combined 'Year' & 'Number' data.
    '''
    # Convert all 'Year' columns to integer
    for col in df.columns:
        if 'Year' in col:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Combine all 'Year' and 'Number' columns into two columns
    year_cols = [col for col in df.columns if 'Year' in col]
    number_cols = [col for col in df.columns if 'Number' in col]

    df_year = pd.concat([df[col] for col in year_cols])
    df_number = pd.concat([df[col] for col in number_cols])

    # Create a new DataFrame with the combined data
    df_clean = pd.DataFrame({'Year': df_year, 'Number': df_number})

    # Drop rows with missing values
    df_clean = df_clean.dropna()

    return df_clean


def predict_number(df, year):
    X = df['Year'].values.reshape(-1, 1)
    y = df['Number'].values
    model = LinearRegression()
    model.fit(X, y)
    prediction = model.predict(np.array([[year]]))
    return prediction[0]


def plot_data_and_predictions(df, prediction_2023, prediction_user, user_year, title):
    X = df['Year'].values
    y = df['Number'].values

    plt.plot(X, y, color = 'black', label='Historical Data')
    plt.scatter(2023, prediction_2023, color='red', label='Prediction for 2023')
    plt.scatter(user_year, prediction_user, color='blue', label=f'Prediction for {user_year}')

    plt.xlabel('Year')
    plt.ylabel('Number of People')
    plt.title(title, fontsize=15)
    plt.legend()

    plt.show()
  
def filter_data(df, start_year, end_year):
    '''
    Filters the DataFrame for the given range of years.
    '''
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)] 

def predict_plot_covid(df, start_year, end_year, title):
    '''
    Trains a linear regression model on the input DataFrame, makes predictions
    for the specified range of years, plots the actual & predicted data.
    '''
    # Data range 2019 - 2022
    df_filtered = filter_data(df, 2019, 2022)

    # Train linear regression model
    model = LinearRegression()
    model.fit(df_filtered[['Year']], df_filtered['Number'])
    # Make predictions for given range
    years = np.arange(start_year, end_year+1).reshape(-1, 1)
    predictions = model.predict(years)

    # Plot actual data for 2019 - 2022
    plt.scatter(df_filtered['Year'], df_filtered['Number'], color='blue', label='Actual Data')
    # Plot predictions for 2019 - 2023
    plt.plot(years, predictions, color='red', label='Predicted Data')

    plt.title(title, fontsize=15)
    plt.xlabel('Year')
    plt.ylabel('Number')
    plt.legend()
    plt.show()
  
    
def main():
    
    
    df = excel_to_dataframe(DIRECTORY)
    df = clean_dataframe(df)
# =============================================================================
#     csv_data = df.to_csv(index=False, path_or_buf=None)
#     csv_file_path = "/Users/ekaterinasivokon/Desktop/ds_final_project.csv"
#     df.to_csv(csv_file_path, index=False)
# ===========================================================================
    prediction_2023 = predict_number(df, 2023)
    # prediction_2023 = predict_2023_number(df)
    user_year = 2100
    prediction_user = predict_number(df, user_year)
    # Plot Data with Prediction
    title = "Prediction: persons obtaining lawful permanent resident status"
    plot_data_and_predictions(df, prediction_2023, prediction_user, user_year, title)
   
    predict_plot_covid(df, 2019, 2023, "Does the model predict the changes in data during covid?")
    
if __name__ == "__main__":
    main()
    
