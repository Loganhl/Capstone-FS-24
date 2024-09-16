import sqlite3
import os

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.queries = self.load_queries()  # Load queries from the SQL file
        self.init_db()  # Initialize the database on creation

    def load_queries(self):
        queries = {}
        # Open the SQL file and read its content
        with open('queries.sql', 'r') as file:
            content = file.read().strip()
            # Split on '-- ' to get each query block
            parts = content.split('-- ')
            for part in parts:
                if part.strip():
                    # Split each part into query name and query text
                    lines = part.split('\n', 1)
                    if len(lines) == 2:
                        query_name, query = lines
                        queries[query_name.strip()] = query.strip()
        return queries

    def init_db(self):
        # Initialize the database only if it does not exist
        if not os.path.exists(self.db_name):
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Execute SQL queries to create tables
                cursor.execute(self.queries['Create table for TypingMetrics'])
                cursor.execute(self.queries['Create table for KeyPairTimes'])
                conn.commit()

    def save_to_db(self, wpm, avg_interval, key_pair_averages):
        """Save averaged typing metrics and key pair times to the SQLite database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Calculate new average WPM and interval
            cursor.execute(self.queries['SELECT_EXISTING_AVERAGES'])
            result = cursor.fetchone()
            if result[0] > 0:
                # If records exist, calculate new averages
                count, old_wpm_avg, old_interval_avg = result
                new_wpm_avg = (old_wpm_avg * count + wpm) / (count + 1)
                new_interval_avg = (old_interval_avg * count + avg_interval) / (count + 1)
                cursor.execute(self.queries['UPDATE_EXISTING_AVERAGES'], (new_wpm_avg, new_interval_avg))
            else:
                # If no records exist, insert new averages
                cursor.execute(self.queries['INSERT_NEW_AVERAGES'], (wpm, avg_interval))
            
            # Update key pair times
            for pair, avg_time in key_pair_averages.items():
                pair_str = f"{pair[0]}-{pair[1]}"
                cursor.execute(self.queries['SELECT_EXISTING_KEY_PAIR_DATA'], (pair_str,))
                result = cursor.fetchone()
                if result:
                    # If key pair data exists, update it
                    old_avg_time, count = result
                    new_count = count + 1
                    new_avg_time = (old_avg_time * count + avg_time) / new_count
                    cursor.execute(self.queries['UPDATE_EXISTING_KEY_PAIR_DATA'], (new_avg_time, new_count, pair_str))
                    print(f"Updated KeyPairTimes: Pair={pair_str}, AvgTime={new_avg_time}, Count={new_count}")
                else:
                    # If key pair data does not exist, insert it
                    cursor.execute(self.queries['INSERT_NEW_KEY_PAIR_DATA'], (pair_str, avg_time, 1))
                    print(f"Inserted KeyPairTimes: Pair={pair_str}, AvgTime={avg_time}, Count=1")
            
            # Commit the transaction
            conn.commit()
