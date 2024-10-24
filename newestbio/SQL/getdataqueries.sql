
-- Get existing biometric data
SELECT 
    BD.ID,
    BD.total_keys,
    BD.total_errors,
    BD.wpm,
    BD.keys_per_second,
    BD.time_between_keystrokes,
    BD.total_clicks,
    BD.mouse_speed,
    BD.double_click_speed,
    MC.update_count AS biometric_update_count
FROM 
    BiometricData BD
LEFT JOIN 
    MetricCount MC ON BD.ID = MC.ID
WHERE 
    BD.ID = ?;

-- Get existing key pair times
SELECT
    CH.ID,
    CH.coordinate
    CH.click_count
FROM ClickHotspots CH

WHERE
    CH.ID = ?;

-- Get existing metric counts
SELECT 
    KPT.user_id,
    KPT.key_pair,
    KPT.avg_time,
    KPT.count
FROM 
    KeyPairTimes KPT
WHERE 
    KPT.user_id = ?; 

SELECT 
    MC.ID,
    MC.metric_name,
    MC.update_count
FROM 
    MetricCount MC
WHERE 
    MC.ID = ?;  




