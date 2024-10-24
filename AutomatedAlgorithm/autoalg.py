import pandas as pd
from sklearn.ensemble import IsolationForest
import logging
from pathlib import Path
import time

# Initialize logging
logging.basicConfig(filename='anomaly_detection.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def check_csv_row_count_and_analyze(file_path):
    try:
        # Read the CSV
        df = pd.read_csv(file_path, header=None)

        # Check numeric.
        df[0] = pd.to_numeric(df[0], errors='coerce')

        # Dop NaN values.
        df = df.dropna()

        row_count = len(df)
        logging.info(f"Checking {file_path.name}, found {row_count} rows.")

        if row_count >= 5:
            # Initialize the Isolation Forest model
            iso_forest = IsolationForest(contamination=0.1, random_state=42)

            # Fit the model on the data
            iso_forest.fit(df)

            # Predict Anomaly
            df['anomaly'] = iso_forest.predict(df)

            # Set Predictions to Binary
            df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})

            anomalies_count = df['anomaly'].sum()

            anomaly_percentage = (anomalies_count / row_count) * 100
            logging.info(f"{file_path.name} has reached 5 rows. Anomaly percentage: {anomaly_percentage:.2f}%")

            if anomalies_count > 0:
                print(f"Warning: {anomalies_count} anomalies detected in {file_path.name}.")
            return anomaly_percentage
        else:
            logging.info(f"{file_path.name} has not reached 5 rows yet.")
        
        return None

    except Exception as e:
        logging.error(f"Error processing {file_path.name}: {str(e)}")

def main():
    data_dir = Path('StoredData')

    csv_files = [
        data_dir / 'avg_time_between_keystrokes.csv',
        data_dir / 'click_count.csv',
        data_dir / 'double_click_speed.csv',
        data_dir / 'error_count.csv',
        data_dir / 'keys_per_second.csv',
        data_dir / 'mouse_speed.csv',
        data_dir / 'total_keys.csv',
        data_dir / 'wpm.csv'
    ]

    while True:
        for csv_file in csv_files:
            logging.info('------------------------------------------------------------------------------------------------')
            anomaly_percentage = check_csv_row_count_and_analyze(csv_file)
            if anomaly_percentage is not None:
                logging.info(f"Processed {csv_file.name} with anomaly percentage: {anomaly_percentage:.2f}%")

        time.sleep(10)

if __name__ == "__main__":
    main()
