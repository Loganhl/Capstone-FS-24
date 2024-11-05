const connection = require('./connect')


function Maketables(){
    //create keys per second
    let q1 = 'CREATE TABLE IF NOT EXISTS avg_click_dwell_time (    avg_click_dwell_time_id INT PRIMARY KEY AUTO_INCREMENT,value REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, USER_ID VARCHAR(36),FOREIGN KEY (USER_ID) REFERENCES USER_ENTITY(ID));';
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
}

module.exports = Maketables;