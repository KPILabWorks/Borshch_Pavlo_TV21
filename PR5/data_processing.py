# Практична робота №5
# Варіант №5
# Обробка та злиття даних з різних джерел: 
# Реалізувати обробку даних з CSV, JSON та SQL, їх очищення та злиття в один датафрейм.

import pandas as pd
import sqlite3
import json
import os

def load_from_csv(filename="data.csv"):
    """Loads data from a CSV file."""
    if not os.path.exists(filename):
        print(f"Error: CSV file '{filename}' not found.")
        return None
    try:
        df = pd.read_csv(filename)
        print(f"Data loaded from {filename}")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def load_from_json(filename="data.json"):
    """Loads data from a JSON file."""
    if not os.path.exists(filename):
        print(f"Error: JSON file '{filename}' not found.")
        return None
    try:
        # Assumes 'records' orientation from save_to_json
        df = pd.read_json(filename, orient="records")
        print(f"Data loaded from {filename}")
        return df
    except ValueError as e: # More specific error for JSON format issues
        print(f"Error decoding JSON (check format/orientation): {e}")
        return None
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

def load_from_sql(filename="data.db", table_name="my_table"):
    """Loads data from an SQLite database."""
    if not os.path.exists(filename):
        print(f"Error: SQL database file '{filename}' not found.")
        return None
    try:
        with sqlite3.connect(filename) as conn:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        print(f"Data loaded from {filename} (table: {table_name})")
        return df
    except (sqlite3.OperationalError, pd.io.sql.DatabaseError) as e: # Catch common SQL errors
        print(f"Error: Table '{table_name}' not found or SQL error: {e}")
        return None
    except Exception as e:
        print(f"Error loading from SQL: {e}")
        return None

def clean_data(df):
    """Performs basic data cleaning."""
    if df is None:
        return None
    
    cleaned_df = df.copy() # Avoid SettingWithCopyWarning
    
    # Remove rows with missing values
    cleaned_df.dropna(inplace=True)

    # Convert 'Value' column to integer
    try:
        cleaned_df['Value'] = cleaned_df['Value'].astype(int)
    except ValueError as e:
        print(f"Warning: Could not convert 'Value' to int: {e}. Leaving as is.")

    # Remove duplicate rows
    cleaned_df.drop_duplicates(inplace=True)
    return cleaned_df

def merge_dataframes(df1, df2, df3):
    """
    Merges three DataFrames based on 'ID'.
    Uses outer joins to include all data.
    """
    dfs = [df for df in [df1, df2, df3] if df is not None]
    if len(dfs) < 2:
       print("Error: Need at least two non-None DataFrames to merge.")
       return dfs[0] if dfs else None # Return the single df or None

    merged_df = dfs[0]
    suffixes = [f'_src{i+1}' for i in range(len(dfs))] # Generic suffixes

    for i, df_next in enumerate(dfs[1:], 1):
         # Define suffixes dynamically based on which merge step we are on
         current_suffixes = (suffixes[i-1] if i==1 else '', suffixes[i])
         merged_df = pd.merge(merged_df, df_next, on='ID', how='outer', suffixes=current_suffixes)

    return merged_df

def process_and_merge():
    """Loads, cleans, and merges data from CSV, JSON, and SQL."""
    df_csv = clean_data(load_from_csv())
    df_json = clean_data(load_from_json())
    df_sql = clean_data(load_from_sql())

    merged_df = merge_dataframes(df_csv, df_json, df_sql)

    if merged_df is not None:
        print("\nMerged DataFrame Head:")
        print(merged_df.head())
        print("\nMerged DataFrame Info:")
        merged_df.info()
        # print("\nMerged DataFrame Description:")
        # print(merged_df.describe(include='all')) # include='all' gives info on non-numeric too

if __name__ == "__main__":
    process_and_merge()
