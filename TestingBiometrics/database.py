import sqlite3
import os

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.queries = self.load_queries()  # Load queries from the SQL file
        self.init_db()  # Initialize the database on creation

    def load_queries(self):
        with open('queries.sql', 'r') as file:
            queries = file.read().split(';')  # Split queries by semicolon
        return [query.strip() for query in queries if query.strip()]

    def init_db(self):
        if not os.path.exists(self.db_name):
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                for query in self.queries:
                    if query:
                        cursor.execute(query)
                conn.commit()

    def save_to_db(self, wpm, avg_interval, key_pair_averages):
        
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Calculate new average WPM and interval
            cursor.execute(self.queries[2])
            result = cursor.fetchone()
            if result[0] > 0:

                count, old_wpm_avg, old_interval_avg = result

                new_wpm_avg = (old_wpm_avg * count + wpm) / (count + 1)

                new_interval_avg = (old_interval_avg * count + avg_interval) / (count + 1)

                cursor.execute(self.queries[3], (new_wpm_avg, new_interval_avg))
                
            else:
                cursor.execute(self.queries[4], (wpm, avg_interval))

            # Update key pair times
            for pair, avg_time in key_pair_averages.items():

                pair_str = f"{pair[0]}-{pair[1]}"

                cursor.execute(self.queries[5], (pair_str,))

                result = cursor.fetchone()

                if result:

                    old_avg_time, count = result

                    new_count = count + 1

                    new_avg_time = (old_avg_time * count + avg_time) / new_count

                    cursor.execute(self.queries[6], (new_avg_time, new_count, pair_str))

                    print(f"Updated KeyPairTimes: Pair={pair_str}, AvgTime={new_avg_time}, Count={new_count}")

                else:

                    cursor.execute(self.queries[7], (pair_str, avg_time, 1))
                    print(f"Inserted KeyPairTimes: Pair={pair_str}, AvgTime={avg_time}, Count=1")

            conn.commit()
