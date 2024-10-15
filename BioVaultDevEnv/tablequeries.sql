
CREATE TABLE KeyPairAverageTime (
    key_pair_avg_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    key_pair VARCHAR(50),
    average_time FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID) REFERENCES USER_ENTITY(ID)
);


CREATE TABLE KeyboardData (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    wpm FLOAT NOT NULL,
    keystrokes_per_10_sec FLOAT NOT NULL,
    keys_per_second FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID) REFERENCES USER_ENTITY(ID)
);


CREATE TABLE MouseData (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    avg_speed FLOAT NOT NULL,
    avg_click_dwell FLOAT NOT NULL,
    avg_double_click FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID) REFERENCES USER_ENTITY(ID)
);


CREATE TABLE AuthenticationLogs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    is_authenticated BOOLEAN NOT NULL,
    reason VARCHAR(255),
    comparison_metric VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID) REFERENCES USER_ENTITY(ID)
);


CREATE TABLE ClickHotspots (
    hotspot_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    x_coordinate FLOAT,
    y_coordinate FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    num_clicks INT,
    FOREIGN KEY (ID) REFERENCES USER_ENTITY(ID)
);
