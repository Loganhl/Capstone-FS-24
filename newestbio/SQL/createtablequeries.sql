CREATE TABLE BiometricData(
    biometric_id INT PRIMARY KEY AUTO_INCREMENT
    ID INT,
    total_keys INT,
    total_errors INT,
    wpm FLOAT,
    keys_per_second FLOAT,
    time_between_keystrokes FLOAT,
    total_clicks INT,
    mouse_speed FLOAT,
    double_click_speed FLOAT,
    FOREIGN KEY (ID) REFERENCES USER_ENTITY(ID)
);

CREATE TABLE ClickHotspots (
    hotspot_id INT PRIMARY KEY AUTO_INCREMENT,
    ID INT,
    coordinate VARCHAR(255),
    click_count,
    FOREIGN KEY (ID) REFERENCES USER_ENTITY(ID)
);

CREATE TABLE KeyPairTimes (
    pair_id INT PRIMARY KEY AUTO_INCREMENT,
    ID INT,
    key_pair VARCHAR(2),
    avg_time FLOAT,
    count INT,
    FOREIGN KEY (ID) REFERENCES USER_ENTITY(ID)
);

CREATE TABLE MetricCount(
    count_id INT PRIMARY KEY AUTO_INCREMENT,
    ID INT,
    metric_name VARCHAR(30),
    update_count INT,
    FOREIGN KEY (biometric_id) REFERENCES BiometricData(biometric_id)
);