import mysql.connector
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import logging
import time


# Initialize logging.
logging.basicConfig(filename='anomaly_detection.log', level=logging.DEBUG,
                   format='%(asctime)s:%(levelname)s:%(message)s')

# Database configuration.
config = {
   'user': 'root',
   'password': 'secretsquirrels',
   'host': 'localhost',
   'database': 'biometric_auth',
   'port': '3307'
}

# Mapping of individual metric tables to their corresponding training table columns.
metric_table_map = {
    'wpm': 'wpm',
    'mouse_speed': 'mouse_speed',
    'keys_per_sec': 'keys_per_sec',
    'avg_time_between_keystrokes': 'avg_time_between_keystrokes',
    'avg_dwell_time': 'avg_dwell_time',
    'avg_click_dwell_time': 'avg_click_dwell_time'
}

def handle_missing_values(df):
    """Handles missing values in the data, applying imputer only to numeric columns."""
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    imputer = SimpleImputer(strategy='mean')
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    return df

def fetch_user_data(config, table_name, user_id, limit=None):
    """Fetches data from a specified table for a given user."""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name} WHERE USER_ID = '{user_id}' ORDER BY created_at ASC"
        if limit:
            query += f" LIMIT {limit}"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(result)
    except Exception as e:
        logging.error(f"Error fetching data for user_id {user_id} from {table_name}: {str(e)}")
        return pd.DataFrame()

def fetch_training_data(config, user_id):
    """Fetches and merges training data for mouse and keyboard metrics."""
    try:
        mouse_data = fetch_user_data(config, 'mouse_training_data', user_id)
        keyboard_data = fetch_user_data(config, 'keystroke_training_data', user_id)

        combined_data = pd.merge(
            mouse_data[['USER_ID', 'mouse_speed', 'avg_click_dwell_time']],
            keyboard_data[['USER_ID', 'wpm', 'keys_per_sec', 'avg_time_between_keystrokes', 'avg_dwell_time']],
            on='USER_ID', how='inner'
        )

        return combined_data
    except Exception as e:
        logging.error(f"Error fetching and merging training data for user_id {user_id}: {str(e)}")
        return pd.DataFrame()

def normalize_data(df):
    """Normalizes data for anomaly detection."""
    required_columns = [
       'mouse_speed', 'avg_click_dwell_time', 'wpm',
       'keys_per_sec', 'avg_time_between_keystrokes', 'avg_dwell_time'
    ]
    for col in required_columns:
        if col not in df.columns:
            logging.error(f"Column '{col}' is missing in the DataFrame.")
            raise KeyError(f"Column '{col}' is missing in the DataFrame.")
    
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[required_columns] = scaler.fit_transform(df[required_columns])
    return df_scaled

def check_data(config, metric_table, user_id):
    try:
        # Check if the metric table has at least 10 rows for the user
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {metric_table} WHERE USER_ID = %s", (user_id,))
        row_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if row_count < 10:
            logging.info(f"{metric_table} for user_id {user_id} has less than 10 rows. Skipping anomaly detection.")
            return None

        # Fetch user data for the specified metric table
        df = fetch_user_data(config, metric_table, user_id, limit=10)
        if df.empty:
            logging.info(f"{metric_table} for user_id {user_id} is empty.")
            return None

        raw_df = df.copy()

        # Fetch training data for anomaly detection
        training_data = fetch_training_data(config, user_id)
        if training_data.empty:
            logging.error(f"Training data for user_id {user_id} is missing.")
            return None

        # Get the corresponding metric column
        metric_column = metric_table_map.get(metric_table)
        if not metric_column:
            logging.error(f"No mapping found for metric_table: {metric_table}")
            return None

        # Define relevant columns, ensuring 'created_at' is present
        relevant_columns = ['USER_ID', metric_column, 'created_at']
        training_data = training_data[[col for col in relevant_columns if col in training_data.columns]]
        df = df.rename(columns={'value': metric_column})
        raw_df = df.rename(columns={'value': metric_column})

        df = df[[col for col in relevant_columns if col in df.columns]]
        raw_df = df[[col for col in relevant_columns if col in df.columns]]

        # Normalize data using StandardScaler
        scaler = StandardScaler()
        training_data[[metric_column]] = scaler.fit_transform(training_data[[metric_column]])
        df[[metric_column]] = scaler.transform(df[[metric_column]])

        # Handle missing values in DataFrames
        df = handle_missing_values(df)
        raw_df = handle_missing_values(raw_df)
        training_data = handle_missing_values(training_data)

        # Train the IsolationForest model for anomaly detection
        iso_forest = IsolationForest(n_estimators=100, max_samples='auto', contamination=0.1, random_state=42)
        iso_forest.fit(training_data[[metric_column]])

        # Detect anomalies in the data
        df['anomaly'] = iso_forest.predict(df[[metric_column]])
        df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})

        anomalies_count = df['anomaly'].sum()
        anomaly_percentage = (anomalies_count / len(df)) * 100 if len(df) >= 10 else 0

        if len(df) >= 10:
            logging.info(f"{metric_table} for user_id {user_id} has anomaly percentage: {anomaly_percentage:.2f}%")

        # Insert anomaly percentage into the database
        insert_anomaly_percentages(config, user_id, metric_table, anomaly_percentage)

        # If anomaly percentage is below 30%, move data to the training set
        if anomaly_percentage <= 30:
            logging.info(f"Anomaly percentage below 30%, moving data to training set for {user_id}")
            move_data_to_training_set(config, metric_table, user_id, raw_df)
        else:
            logging.info(f"Anomaly percentage above 30%, storing percentage and wiping data for {user_id}")
            clear_data_from_testing(config, metric_table, user_id, raw_df)
        return anomaly_percentage

    except KeyError as ke:
        logging.error(f"Missing column in DataFrame: {ke}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")



def insert_anomaly_percentages(config, user_id, metric_table, anomaly_percentages):
    """Inserts or updates multiple anomaly percentages into the percentages table."""
    conn = None
    cursor = None
    try:
        column_map = {
            'wpm': 'wpm_perc',
            'mouse_speed': 'mouse_speed_perc',
            'keys_per_sec': 'keys_per_sec_perc',
            'avg_time_between_keystrokes': 'avg_time_between_keystrokes_perc',
            'avg_dwell_time': 'avg_dwell_time_perc',
            'avg_click_dwell_time': 'avg_click_dwell_time_perc'
        }

        if metric_table not in column_map:
            logging.error(f"Invalid metric_table: {metric_table}")
            return

        column_name = column_map[metric_table]

        # Convert any NumPy float64 values to Python native float
        anomaly_percentages = {metric_table: float(anomaly_percentages)}

        # Connect to the database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Prepare the insert query to update all anomaly percentages in a single transaction
        query = f"""
        INSERT INTO percentages (USER_ID, {column_name})
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE {column_name}=VALUES({column_name});
        """

        data_to_insert = [(user_id, percentage) for percentage in anomaly_percentages.values()]
        
        cursor.executemany(query, data_to_insert)
        conn.commit()

        logging.info(f"{column_name} anomalies for {user_id} successfully updated in a single transaction.")

    except mysql.connector.Error as db_err:
        logging.error(f"Database connection error: {str(db_err)}")
    except Exception as ex:
        logging.error(f"Unexpected error while inserting anomalies for {user_id} in {metric_table}: {str(ex)}")
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def move_data_to_training_set(config, metric_table, user_id, raw_df):
    try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            column_map = {
                'wpm': 'wpm',
                'mouse_speed': 'mouse_speed',
                'keys_per_sec': 'keys_per_sec',
                'avg_time_between_keystrokes': 'avg_time_between_keystrokes',
                'avg_dwell_time': 'avg_dwell_time',
                'avg_click_dwell_time': 'avg_click_dwell_time'
            }

            if metric_table not in column_map:
                logging.error(f"Unknown table name: {metric_table}")
                return

            target_table = 'keystroke_training_data' if metric_table in ['wpm', 'keys_per_sec', 'avg_dwell_time', 'avg_time_between_keystrokes'] else 'mouse_training_data'

            metric_column = column_map[metric_table]
            relevant_columns = ['USER_ID', metric_column, 'created_at']

            # Filter raw data to match the required columns
            raw_filtered = raw_df[relevant_columns]

            # Construct the SQL query for inserting raw data into the database
            column_placeholders = ', '.join(['%s'] * len(relevant_columns))
            columns_sql = ', '.join(relevant_columns)
            insert_query = f"INSERT INTO {target_table} ({columns_sql}) VALUES ({column_placeholders})"

            cursor.executemany(insert_query, raw_filtered.values.tolist())
            conn.commit()


            if 'created_at' in raw_df.columns:
                created_at_values = ', '.join([f"'{row}'" for row in raw_df['created_at']])
                delete_query = f"DELETE FROM {metric_table} WHERE USER_ID = %s AND created_at IN ({created_at_values})"
                cursor.execute(delete_query, (user_id,))

            conn.commit()

            logging.info(f"Moved data for user_id {user_id} to {target_table}. Removed from {metric_table}.")

    except mysql.connector.Error as e:
        logging.error(f"Database error for user_id {user_id} in {metric_table}: {str(e)} move data to training set")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def clear_data_from_testing(config, metric_table, user_id, raw_df):
    try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            column_map = {
                'wpm': 'wpm',
                'mouse_speed': 'mouse_speed',
                'keys_per_sec': 'keys_per_sec',
                'avg_time_between_keystrokes': 'avg_time_between_keystrokes',
                'avg_dwell_time': 'avg_dwell_time',
                'avg_click_dwell_time': 'avg_click_dwell_time'
            }

            if metric_table not in column_map:
                logging.error(f"Unknown table name: {metric_table}")
                return

            if 'created_at' in raw_df.columns:
                created_at_values = ', '.join([f"'{row}'" for row in raw_df['created_at']])
                delete_query = f"DELETE FROM {metric_table} WHERE USER_ID = %s AND created_at IN ({created_at_values})"
                cursor.execute(delete_query, (user_id,))

            conn.commit()

            logging.info(f"Cleared data for user_id {user_id}. Removed from {metric_table}.")

    except mysql.connector.Error as e:
        logging.error(f"Database error for user_id {user_id} in {metric_table}: {str(e)} move data to training set")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def main():
    table_names = list(metric_table_map.keys())

# Normalize data using StandardScaler
  
    while True:
        user_ids = fetch_all_user_ids(config, table_names)
      
        for user_id in user_ids:
            for metric_table in table_names:
                anomaly_percentage = check_data(config, metric_table, user_id)
                if anomaly_percentage is not None:
                    print(f"Anomaly percentage for user {user_id} in {metric_table}: {anomaly_percentage:.2f}%")
                    
        time.sleep(15)

def fetch_all_user_ids(config, table_names):
    """Fetches all distinct user IDs."""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        query = " UNION ".join([f"SELECT DISTINCT USER_ID FROM {table}" for table in table_names])

        # Wrap in parentheses to ensure proper syntax
        full_query = f"SELECT DISTINCT USER_ID FROM ({query}) AS combined_result"
        cursor.execute(full_query)
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return user_ids
    except Exception as e:
        logging.error(f"Error fetching user IDs: {str(e)}")
        return []
    
    
if __name__ == "__main__":
    main()
