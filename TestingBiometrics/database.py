import sqlite3
import os

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.init_db()  # Initialize the database on creation

    def init_db(self):
        if not os.path.exists(self.db_name):
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Create table for typing metrics
                cursor.execute('''
                    CREATE TABLE TypingMetrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        average_wpm REAL,
                        average_time_between_keystrokes REAL
                    )
                ''')
                # Create table for key pair times
                cursor.execute('''
                    CREATE TABLE KeyPairTimes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key_pair TEXT,
                        average_time REAL,
                        count INTEGER
                    )
                ''')
                conn.commit()

    def save_to_db(self, wpm, avg_interval, key_pair_averages):
        """Save averaged typing metrics and key pair times to the SQLite database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Calculate new average WPM and interval
            cursor.execute('SELECT COUNT(*), AVG(average_wpm), AVG(average_time_between_keystrokes) FROM TypingMetrics')
            result = cursor.fetchone()
            if result[0] > 0:
                count, old_wpm_avg, old_interval_avg = result
                new_wpm_avg = (old_wpm_avg * count + wpm) / (count + 1)
                new_interval_avg = (old_interval_avg * count + avg_interval) / (count + 1)
                cursor.execute('''
                    UPDATE TypingMetrics
                    SET average_wpm = ?, average_time_between_keystrokes = ?
                ''', (new_wpm_avg, new_interval_avg))
                
            else:
                cursor.execute('''
                    INSERT INTO TypingMetrics (average_wpm, average_time_between_keystrokes)
                    VALUES (?, ?)
                ''', (wpm, avg_interval))

            # Update key pair times
            for pair, avg_time in key_pair_averages.items():
                pair_str = f"{pair[0]}-{pair[1]}"
                cursor.execute('SELECT average_time, count FROM KeyPairTimes WHERE key_pair = ?', (pair_str,))
                result = cursor.fetchone()
                if result:
                    old_avg_time, count = result
                    new_count = count + 1
                    new_avg_time = (old_avg_time * count + avg_time) / new_count
                    cursor.execute('''
                        UPDATE KeyPairTimes
                        SET average_time = ?, count = ?
                        WHERE key_pair = ?
                    ''', (new_avg_time, new_count, pair_str))
                    print(f"Updated KeyPairTimes: Pair={pair_str}, AvgTime={new_avg_time}, Count={new_count}")
                else:
                    cursor.execute('''
                        INSERT INTO KeyPairTimes (key_pair, average_time, count)
                        VALUES (?, ?, ?)
                    ''', (pair_str, avg_time, 1))
                    print(f"Inserted KeyPairTimes: Pair={pair_str}, AvgTime={avg_time}, Count=1")

            conn.commit()