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
    return df_scaled, scaler

def check_data(config, metric_table, user_id):
    """Checks for anomalies in data from individual metric tables."""
    df = fetch_user_data(config, metric_table, user_id, limit=10)
    
    if df.empty:
        logging.info(f"{metric_table} for user_id {user_id} is empty.")
        return None

    training_data = fetch_training_data(config, user_id)
    if training_data.empty:
        logging.error(f"Training data for user_id {user_id} is missing.")
        return None

    try:
        metric_column = metric_table_map.get(metric_table)
        if not metric_column:
            logging.error(f"No mapping found for metric_table: {metric_table}")
            return None

        relevant_columns = ['USER_ID', metric_column]
        training_data = training_data.loc[:, [col for col in relevant_columns if col in training_data.columns]]

        df = df.rename(columns={'value': metric_column})
        df = df.loc[:, [col for col in relevant_columns if col in df.columns]]

        if metric_column not in training_data.columns or metric_column not in df.columns:
            logging.warning(f"Missing column {metric_column} in either training data or metric data for {metric_table}.")
            return None

        # Normalize data for anomaly detection
        training_data_normalized, scaler = normalize_data(training_data)
        df_normalized = df.copy()
        df_normalized[[metric_column]] = scaler.transform(df[[metric_column]])

        df_normalized = handle_missing_values(df_normalized)
        training_data_normalized = handle_missing_values(training_data_normalized)

        iso_forest = IsolationForest(n_estimators=100, max_samples='auto', contamination=0.1, random_state=42)
        iso_forest.fit(training_data_normalized[[metric_column]])

        df_normalized['anomaly'] = iso_forest.predict(df_normalized[[metric_column]])
        df_normalized['anomaly'] = df_normalized['anomaly'].map({1: 0, -1: 1})

        anomalies_count = df_normalized['anomaly'].sum()
        anomaly_percentage = (anomalies_count / len(df_normalized)) * 100 if len(df_normalized) >= 10 else 0

        if len(df_normalized) >= 10:
            logging.info(f"{metric_table} for user_id {user_id} has anomaly percentage: {anomaly_percentage:.2f}%")
        
        # If anomaly percentage is under 30%, move data to training
        if anomaly_percentage <= 30:
            logging.info(f"Anomaly percentage below 30%, moving data to training set for {user_id}.")
            move_data_to_training_set(config, metric_table, user_id, df)

        return anomaly_percentage
    except Exception as e:
        logging.error(f"Error in anomaly detection for {metric_table}, user_id {user_id}: {str(e)}")
        return None

def move_data_to_training_set(config, metric_table, user_id, df):
    """Moves data to the training set if anomalies are detected below the threshold."""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Determine the target table based on metric
        if metric_table in ['wpm', 'keys_per_sec', 'avg_time_between_keystrokes', 'avg_dwell_time']:
            target_table = 'keystroke_training_data'
        elif metric_table in ['mouse_speed', 'avg_click_dwell_time']:
            target_table = 'mouse_training_data'
        else:
            logging.error(f"Unknown table name: {metric_table}")
            return
        
        relevant_columns = ['USER_ID'] + [metric_table_map[metric_table]]
        df_filtered = df[relevant_columns]

        column_placeholders = ', '.join(['%s'] * len(relevant_columns))
        columns_sql = ', '.join(relevant_columns)
        insert_query = f"INSERT INTO {target_table} ({columns_sql}) VALUES ({column_placeholders})"
        
        cursor.executemany(insert_query, df_filtered.values.tolist())

        # Delete the data from the original table
        created_at_values = ', '.join([f"'{row}'" for row in df['created_at']])
        cursor.execute(f"DELETE FROM {metric_table} WHERE USER_ID = %s AND created_at IN ({created_at_values})", (user_id,))

        conn.commit()
        cursor.close()
        conn.close()

        logging.info(f"Moved data for user_id {user_id} to {target_table}. Removed from {metric_table}.")

    except mysql.connector.Error as e:
        logging.error(f"Error moving data for user_id {user_id} to training set: {e}")

def main():
    table_names = list(metric_table_map.keys())

    while True:
        user_ids = fetch_all_user_ids(config, table_names)

        for user_id in user_ids:
            for metric_table in table_names:
                anomaly_percentage = check_data(config, metric_table, user_id)
                if anomaly_percentage is not None:
                    print(f"Anomaly percentage for user {user_id} in {metric_table}: {anomaly_percentage:.2f}%")

        time.sleep(60)  

def fetch_all_user_ids(config, table_names):
    """Fetches all distinct user IDs."""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        query = "SELECT DISTINCT USER_ID FROM " + " UNION ".join([f"SELECT DISTINCT USER_ID FROM {table}" for table in table_names])
        cursor.execute(query)
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return user_ids
    except Exception as e:
        logging.error(f"Error fetching user IDs: {str(e)}")
        return []

if __name__ == "__main__":
    main()
