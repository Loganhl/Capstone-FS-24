import mysql.connector
import pandas as pd
import os

# Database configuration
config = {
    'user': 'root',
    'password': 'secretsquirrels',
    'host': 'localhost',
    'database': 'biometric_auth',
    'port': '3307'
}

def insert_data_to_db(table_name, columns, data, config):
    """
    Inserts data into the database table in one batch.

    Args:
    - table_name: Name of the table where data will be inserted.
    - columns: List of column names in the table.
    - data: List of tuples containing data for each row to be inserted.
    - config: Database connection configuration.
    """
    # Step 3: Connect to the database
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print(f"Connected to the database.")
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return
    
    # Step 4: Prepare the SQL query for inserting data
    placeholders = ', '.join(['%s'] * len(columns))  # Prepare placeholders for the columns
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    
    # Step 5: Insert data into the database
    try:
        # Insert data into the database
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{len(data)} rows inserted successfully into {table_name}.")
    except mysql.connector.Error as e:
        print(f"Error inserting data into {table_name}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def read_csv_and_extract_value_column(file_path):
    """
    Reads the CSV file and extracts the 'value' column.
    
    Args:
    - file_path: Path to the CSV file.
    
    Returns:
    - List of 'value' column entries from the CSV file.
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        if 'value' not in df.columns:
            print(f"Error: 'value' column not found in {file_path}.")
            return None
        return df['value'].tolist()
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return None

# File paths for the mouse-related CSVs
mouse_speed_file = r'BioVaultDataCollection\mouse_speed.csv'  # Specify your mouse_speed.csv file path
avg_click_dwell_time_file = r'BioVaultDataCollection\avg_click_dwell_time.csv'  # Specify your avg_click_dwell_time.csv file path

# File paths for the keystroke-related CSVs
avg_dwell_time_file = r'BioVaultDataCollection\avg_dwell_time.csv'  # Specify your avg_dwell_time.csv file path
wpm_file = r'BioVaultDataCollection\wpm.csv'  # Specify your wpm.csv file path
keys_per_sec_file = r'BioVaultDataCollection\keys_per_sec.csv'  # Specify your keys_per_sec.csv file path
avg_time_between_keystrokes_file = r'BioVaultDataCollection\avg_time_between_keystrokes.csv'  # Specify your avg_time_between_keystrokes.csv file path

# Read data from CSVs
mouse_speed_values = read_csv_and_extract_value_column(mouse_speed_file)
avg_click_dwell_time_values = read_csv_and_extract_value_column(avg_click_dwell_time_file)

avg_dwell_time_values = read_csv_and_extract_value_column(avg_dwell_time_file)
wpm_values = read_csv_and_extract_value_column(wpm_file)
keys_per_sec_values = read_csv_and_extract_value_column(keys_per_sec_file)
avg_time_between_keystrokes_values = read_csv_and_extract_value_column(avg_time_between_keystrokes_file)

# Check if any CSV reading failed
if None in [mouse_speed_values, avg_click_dwell_time_values, avg_dwell_time_values, wpm_values, keys_per_sec_values, avg_time_between_keystrokes_values]:
    print("One or more CSV files failed to load.")
else:
    # Prepare data for mouse_training_data table
    mouse_data = list(zip(mouse_speed_values, avg_click_dwell_time_values))

    # Prepare data for keystroke_training_data table
    keystroke_data = list(zip(avg_dwell_time_values, wpm_values, keys_per_sec_values, avg_time_between_keystrokes_values))

    # Table and column names for mouse-related data
    mouse_training_table = 'mouse_training_data'
    mouse_columns = ['mouse_speed', 'avg_click_dwell_time']

    # Table and column names for keystroke-related data
    keystroke_training_table = 'keystroke_training_data'
    keystroke_columns = ['avg_dwell_time', 'wpm', 'keys_per_sec', 'avg_time_between_keystrokes']

    # Insert data into mouse_training_data table
    insert_data_to_db(mouse_training_table, mouse_columns, mouse_data, config)

    # Insert data into keystroke_training_data table
    insert_data_to_db(keystroke_training_table, keystroke_columns, keystroke_data, config)
