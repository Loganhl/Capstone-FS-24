CREATE TABLE IF NOT EXISTS TypingMetrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    average_wpm REAL,
    average_time_between_keystrokes REAL
);

-- Create table for key pair times
CREATE TABLE IF NOT EXISTS KeyPairTimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_pair TEXT,
    average_time REAL,
    count INTEGER
);

-- Select existing averages from TypingMetrics
SELECT COUNT(*), AVG(average_wpm), AVG(average_time_between_keystrokes)
FROM TypingMetrics;

-- Insert new averages into TypingMetrics
INSERT INTO TypingMetrics (average_wpm, average_time_between_keystrokes)
VALUES (?, ?);

-- Update existing averages in TypingMetrics
UPDATE TypingMetrics
SET average_wpm = ?, average_time_between_keystrokes = ?;

-- Select existing key pair data
SELECT average_time, count
FROM KeyPairTimes
WHERE key_pair = ?;

-- Insert new key pair data
INSERT INTO KeyPairTimes (key_pair, average_time, count)
VALUES (?, ?, ?);

-- Update existing key pair data
UPDATE KeyPairTimes
SET average_time = ?, count = ?
WHERE key_pair = ?;
