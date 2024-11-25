import mysql.connector
import pandas as pd
from sklearn.ensemble import IsolationForest
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

def fetch_user_data(config, table_name, user_id):
    #Fetches data for a specific user from the specified table.
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT value FROM {table_name} WHERE USER_ID = '{user_id}' ORDER BY timestamp ASC"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(result)
    except Exception as e:
        logging.error(f"Error fetching data for user_id {user_id} from {table_name}: {str(e)}")
        return pd.DataFrame()

def fetch_all_user_ids(config):
    #Fetches all unique user IDs from the database.
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT USER_ID FROM user_data_table")  # Replace with actual table containing user IDs
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return user_ids
    except Exception as e:
        logging.error(f"Error fetching user IDs: {str(e)}")
        return []

def check_sql_table_and_analyze(config, table_name, user_id):
    df = fetch_user_data(config, table_name, user_id)
    
    # Empty Check.
    if df.empty:
        logging.info(f"{table_name} for user_id {user_id} is empty.")
        return None
    
    # Convert numeric and drop NaN values.
    df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    df = df.dropna()
    
    if df.empty:
        logging.info(f"After dropping NaN values, {table_name} for user_id {user_id} is empty.")
        return None
    
    row_count = len(df)
    logging.info(f"Checking {table_name} for user_id {user_id}, found {row_count} rows.")
    
    if row_count >= 75:
        df.columns = df.columns.astype(str)
        
        # Split data into training and testing sets.
        training_data = df.iloc[:50]
        testing_data = df.iloc[50:75]
        
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        
        # Fit the model on the training data.
        iso_forest.fit(training_data)
        
        # Predict anomalies on the testing data.
        testing_data['anomaly'] = iso_forest.predict(testing_data)
        
        # Set Predictions to Binary.
        testing_data['anomaly'] = testing_data['anomaly'].map({1: 0, -1: 1})
        
        anomalies_count = testing_data['anomaly'].sum()
        anomaly_percentage = (anomalies_count / len(testing_data)) * 100
        logging.info(f"{table_name} for user_id {user_id} has anomaly percentage: {anomaly_percentage:.2f}%")
        
        if anomalies_count > 0:
            logging.info(f"Warning: {anomalies_count} anomalies detected in {table_name} for user_id {user_id}.")
        
        return anomaly_percentage
    else:
        logging.info(f"{table_name} for user_id {user_id} does not have enough data (75 rows needed).")
    
    return None

def insert_percentage(config, table_name, anomaly_percentage, user_id):
    if anomaly_percentage is None:
        return
    
    try:
        # Connect to the database.
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Construct the column name.
        column_name = f'{table_name}_perc'
        
        # Insert the percentage into the constructed column.
        cursor.execute(f"""
            INSERT INTO percentages (USER_ID, {column_name}) VALUES (%s, %s)
        """, (user_id, anomaly_percentage))
        
        # Commit.
        conn.commit()
        
        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        logging.error(f"Error inserting percentage into {table_name} for user_id {user_id}: {e}")

def main():
    logging.info("MAIN")
    table_names = [
        'wpm',
        'mouse_speed',
        'keys_per_sec',
        'avg_time_between_keystrokes',
        'avg_dwell_time',
        'avg_click_dwell_time'
    ]
    
    while True:
        user_ids = fetch_all_user_ids(config)
        
        for user_id in user_ids:
            for table_name in table_names:
                logging.info('------------------------------------------------------------------------------------------------')
                anomaly_percentage = check_sql_table_and_analyze(config, table_name, user_id)
                insert_percentage(config, table_name, anomaly_percentage, user_id)
                if anomaly_percentage is not None:
                    logging.info(f"Processed {table_name} for user_id {user_id} with anomaly percentage: {anomaly_percentage:.2f}%")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
