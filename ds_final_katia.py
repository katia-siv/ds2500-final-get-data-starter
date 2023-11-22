#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 16:29:07 2023

@author: ekaterinasivokon
"""

import pandas as pd
import os
import re
import fnmatch

# Substitute for the filepath to a folder with all Immigration Enforcement Actions folders
# (from 2000 - 2022 yearbooks)
DIRECTORY = "/Users/ekaterinasivokon/Desktop/ds_final_project/Immigration Enforcement Actions"

def list_subfolders(directory):
    """
    Given a directory, returns a list of subfolder names.
    Parameters:
    - directory (str): The path to the directory to be analyzed.
    Returns:
    - List of strings: Names of subfolders in the specified directory.
    """
    try:
        # Get the list of subfolders in the specified directory
        subfolders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        return subfolders
    except OSError as e:
        print(f"Error: {e}")
        return []
        
def concatenate_filepath(strings):
    paths = [os.path.join(DIRECTORY, s) for s in strings]
    return paths

def get_year(path):
    '''Inputs: path (string): a file path to a CSV file.
       Takes a file path as input and extracts
       the year from the file name by using regular expressions
       to find the first numeric sequence.
       Returns the first numeric sequence found in the file name,
       or 0 if none is found.
    '''
    file_name_str = os.path.split(path)[1]
    numeric_matches = re.findall(r'\b\d+\b', file_name_str)
    
    if numeric_matches:
        return int(numeric_matches[0])
    else:
        return 0
    
def get_specific_tables(filepaths):
    ''' Takes a list of filepaths, searches for Excel
        files in each directory, and checks if the files
        contain the phrases "deportable aliens" and "country
        of nationality" or if the filename contains "table34".
        The function returns a dictionary where keys are filepaths
        and values are lists of the corresponding Excel filenames
        that meet the criteria.
    '''
    
    result = {}
    for path in filepaths:
        for root, dirs, files in os.walk(path):
            for filename in files:
                if fnmatch.fnmatch(filename.lower(), '*.xls*'):  # Check if file is an Excel file
                    if 'table34' in filename.lower():  # Check if filename contains 'table34'
                        result.setdefault(root, []).append(filename)
                    else:
                        file_path = os.path.join(root, filename)
                        try:
                            df = pd.read_excel(file_path)
                            if 'deportable aliens' in df.to_string().lower() and 'country of nationality' in df.to_string().lower():
                                result.setdefault(root, []).append(filename)
                        except Exception as e:
                            print(f"Error reading file {file_path}: {e}")
    return result

def format_dictionary(dictionary):
    ''' takes a dictionarty
        {'key1': ['value1'], 'key2': ['value2'], 'key3': ['value3']}
        and turns it into a list
        ['key1/value1', 'key2/value2', 'key3/value3']
    '''
    formatted_list = [f"{key}/{value[0]}" for key, value in dictionary.items()]
    return formatted_list

def read_excel_files(filepaths):
    ''' Reads multiple Excel files and prints information
        about each file.
    '''
    dataframes = []

    for filepath in filepaths:
        try:
            df = pd.read_excel(filepath)

            # Print information about the Excel file
            print(f"Filepath: {filepath}")
            print("Header:")
            print(df.columns)
            print("DataFrame:")
            print(df)
            print("\n")

            # Append the DataFrame to the list
            dataframes.append(df)

        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            dataframes.append(None)

    return dataframes


def main():
    
    subfolder_list = list_subfolders(DIRECTORY)
    paths = concatenate_filepath(subfolder_list)
    
    # sorting the path names from earliest to latest year
    # sorted_byyear_list = sorted(subfolder_list, key=get_year)
    
    # Get data that interests us:
    # NONCITIZEN APPREHENSIONS BY REGION AND COUNTRY OF
    # NATIONALITY for 22 years
    deportable_by_nationality_dict = get_specific_tables(paths)
    paths_to_deportable_by_nationality = format_dictionary(deportable_by_nationality_dict)    
    excel_dataframes = read_excel_files(paths_to_deportable_by_nationality)
    
    
    
if __name__ == "__main__":
    main()