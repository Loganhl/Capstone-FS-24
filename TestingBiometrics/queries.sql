-- CREATE_TYPING_METRICS_TABLE
CREATE TABLE IF NOT EXISTS TypingMetrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    average_wpm REAL,
    average_time_between_keystrokes REAL
);

-- CREATE_KEY_PAIR_TIMES_TABLE
CREATE TABLE IF NOT EXISTS KeyPairTimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_pair TEXT,
    average_time REAL,
    count INTEGER
);

-- SELECT_EXISTING_AVERAGES
SELECT COUNT(*), AVG(average_wpm), AVG(average_time_between_keystrokes)
FROM TypingMetrics;

-- INSERT_NEW_AVERAGES
INSERT INTO TypingMetrics (average_wpm, average_time_between_keystrokes)
VALUES (?, ?);

-- UPDATE_EXISTING_AVERAGES
UPDATE TypingMetrics
SET average_wpm = ?, average_time_between_keystrokes = ?;

-- SELECT_EXISTING_KEY_PAIR_DATA
SELECT average_time, count
FROM KeyPairTimes
WHERE key_pair = ?;

-- INSERT_NEW_KEY_PAIR_DATA
INSERT INTO KeyPairTimes (key_pair, average_time, count)
VALUES (?, ?, ?);

-- UPDATE_EXISTING_KEY_PAIR_DATA
UPDATE KeyPairTimes
SET average_time = ?, count = ?
WHERE key_pair = ?;
