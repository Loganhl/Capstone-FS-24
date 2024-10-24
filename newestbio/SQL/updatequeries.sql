UPDATE BiometricData b
JOIN MetricCount m ON b.biometric_id = m.biometric_id
SET 
    b.total_keys = (b.total_keys * m.update_count + %s) / (m.update_count + 1),
    b.total_errors = (b.total_errors * m.update_count + %s) / (m.update_count + 1),
    b.wpm = (b.wpm * m.update_count + %s) / (m.update_count + 1),
    b.keys_per_second = (b.keys_per_second * m.update_count + %s) / (m.update_count + 1),
    b.time_between_keystrokes = (b.time_between_keystrokes * m.update_count + %s) / (m.update_count + 1),
    b.total_clicks = (b.total_clicks * m.update_count + %s) / (m.update_count + 1),
    b.mouse_speed = (b.mouse_speed * m.update_count + %s) / (m.update_count + 1),
    b.double_click_speed = (b.double_click_speed * m.update_count + %s) / (m.update_count + 1),
    m.update_count = m.update_count + 1
WHERE b.user_id = %s AND m.metric_name IN ('total_keys', 'total_errors', 'wpm', 'keys_per_second', 'time_between_keystrokes', 'total_clicks', 'mouse_speed', 'double_click_speed');



UPDATE MetricCount 
SET update_count = update_count + 1
WHERE ID = %s AND metric_name = %s
