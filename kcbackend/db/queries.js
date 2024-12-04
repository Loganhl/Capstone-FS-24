const connection = require('./connect')


function Maketables(){
    //create keys per second
    let q1 = 'CREATE TABLE IF NOT EXISTS avg_click_dwell_time (avg_click_dwell_time_id INT PRIMARY KEY AUTO_INCREMENT,value REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, USER_ID VARCHAR(36),FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));';
    connection.query(q1);
    // connection.query('CREATE TABLE IF NOT EXISTS keys_per_sec (keys_per_sec_id INT PRIMARY KEY AUTO_INCREMENT,value REAL,USER_ID VARCHAR(36)  FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));')

    // //dwell_time
    let q2 = 'CREATE TABLE IF NOT EXISTS avg_dwell_time (avg_dwell_time_id INT PRIMARY KEY AUTO_INCREMENT,value REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, USER_ID VARCHAR(36),FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));'
    connection.query(q2);
    let q3 = 'CREATE TABLE IF NOT EXISTS avg_time_between_keystrokes ( avg_time_between_keystrokes_id INT PRIMARY KEY AUTO_INCREMENT, value REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, USER_ID VARCHAR(36),  FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));'
    // //time between strokes
    connection.query(q3);
    // let q4 = 'CREATE TABLE IF NOT EXISTS avg_click_dwell_time ( vg_click_dwell_time_id INT PRIMARY KEY AUTO_INCREMENT,value REAL,USER_ID VARCHAR(36),  FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));'
    let q4 = 'CREATE TABLE IF NOT EXISTS keys_per_sec (keys_per_sec_id INT PRIMARY KEY AUTO_INCREMENT,value REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, USER_ID VARCHAR(36),  FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));'
    connection.query(q4);
    
    let q5 = 'CREATE TABLE IF NOT EXISTS mouse_speed (mouse_speed_id INT PRIMARY KEY AUTO_INCREMENT,value REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, USER_ID VARCHAR(36),  FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));'
    connection.query(q5);
    let q6 = 'CREATE TABLE IF NOT EXISTS wpm (wpm_id INT PRIMARY KEY AUTO_INCREMENT,value REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, USER_ID VARCHAR(36),  FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));'
    connection.query(q6);

    let q7 = 'CREATE TABLE IF NOT EXISTS percentages (perc_id INT PRIMARY KEY AUTO_INCREMENT, wpm_perc FLOAT, avg_click_dwell_perc FLOAT, avg_dwell_time_perc FLOAT, keys_per_sec_perc FLOAT, mouse_speed_perc FLOAT, avg_time_between_keystrokes_perc FLOAT,USER_ID varchar(36), FOREIGN KEY (USER_ID) REFERENCEs USER_ENTITY(ID));'
    connection.query(q7);

    let q8 = 'CREATE TABLE IF NOT EXISTS mouse_training_data (mouse_training_id INT PRIMARY KEY AUTO_INCREMENT, mouse_speed FLOAT, avg_click_dwell_time FLOAT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, USER_ID VARCHAR(36),  FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));'
    connection.query(q8);

    let q9 = 'CREATE TABLE IF NOT EXISTS keystroke_training_data (keystroke_training_id INT PRIMARY KEY AUTO_INCREMENT, wpm FLOAT, keys_per_sec FLOAT, avg_time_between_keystrokes FLOAT, avg_dwell_time FLOAT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, USER_ID VARCHAR(36),  FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));'
    connection.query(q9);
}

module.exports = Maketables;