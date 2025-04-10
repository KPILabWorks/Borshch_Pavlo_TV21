# Практична робота №5
# Варіант №5
# Обробка та злиття даних з різних джерел: 
# Реалізувати обробку даних з CSV, JSON та SQL, їх очищення та злиття в один датафрейм.

import pandas as pd
import json
import sqlite3
import os

def create_data(num_records=10):
    """Creates sample data."""
    data = {
        'ID': range(1, num_records + 1),
        'Name': [f'Name_{i}' for i in range(1, num_records + 1)],
        'Value': [i * 10 for i in range(1, num_records + 1)],
        'Category': [chr(ord('A') + (i % 3)) for i in range(1, num_records + 1)] # A, B, C
    }
    return pd.DataFrame(data)

def save_to_csv(df, filename="data.csv"):
    """Saves a DataFrame to a CSV file."""
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def save_to_json(df, filename="data.json"):
    """Saves a DataFrame to a JSON file."""
    # Use 'records' orientation for a list of objects [{col:val}, ...]
    df.to_json(filename, orient="records")
    print(f"Data saved to {filename}")

def save_to_sql(df, filename="data.db", table_name="my_table"):
    """Saves a DataFrame to an SQLite database."""
    # 'replace' overwrites table if it exists
    try:
        with sqlite3.connect(filename) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data saved to {filename} (table: {table_name})")
    except Exception as e:
        print(f"Error saving to SQL: {e}")


def create_and_save_data(num_records=10):
    """Creates data and saves it to CSV, JSON, and SQL."""
    df = create_data(num_records)
    save_to_csv(df)
    save_to_json(df)
    save_to_sql(df)

if __name__ == "__main__":
    num_records = 15
    create_and_save_data(num_records)
