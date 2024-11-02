import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
import logging
import time

# Initialize logging
logging.basicConfig(filename='anomaly_detection.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def check_sql_table_and_analyze(db_path, table_name):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        query = f"SELECT * FROM {table_name}"
        
        df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        # Empty Check
        if df.empty:
            logging.info(f"{table_name} is empty.")
            return None
        
        # Convert numeric and drop NaN values
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        df = df.dropna()
        
        if df.empty:
            logging.info(f"After dropping NaN values, {table_name} is empty.")
            return None
        
        row_count = len(df)
        logging.info(f"Checking {table_name}, found {row_count} rows.")
        
        if row_count >= 5:
            df.columns = df.columns.astype(str)
            
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            
            # Fit the model on the data
            iso_forest.fit(df)
            
            # Predict Anomaly
            df['anomaly'] = iso_forest.predict(df)
            
            # Set Predictions to Binary
            df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})
            
            anomalies_count = df['anomaly'].sum()
            
            anomaly_percentage = (anomalies_count / row_count) * 100
            logging.info(f"{table_name} has reached 5 rows. Anomaly percentage: {anomaly_percentage:.2f}%")
            
            if anomalies_count > 0:
                print(f"Warning: {anomalies_count} anomalies detected in {table_name}.")
            return anomaly_percentage
        else:
            logging.info(f"{table_name} has not reached 5 rows yet.")
        
        return None

    except Exception as e:
        logging.error(f"Error processing {table_name}: {str(e)}")

def main():
    db_path = 'BioVaultDataCollection/data/biometric_data.db'
    
    table_names = [
        'wpm',
        'mouse_speed',
        'keys_per_sec',
        'avg_time_between_keystrokes',
        'avg_dwell_time',
        'avg_click_dwell_time'
    ]
    
    while True:
        for table_name in table_names:
            logging.info('------------------------------------------------------------------------------------------------')
            anomaly_percentage = check_sql_table_and_analyze(db_path, table_name)
            if anomaly_percentage is not None:
                logging.info(f"Processed {table_name} with anomaly percentage: {anomaly_percentage:.2f}%")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
