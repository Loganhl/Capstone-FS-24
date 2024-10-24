import time
from collections import defaultdict

mouse_movements = []
click_times = []
click_hotspots = defaultdict(int)

screen_width = 1920  
screen_height = 1080  

def on_click(x, y, button, pressed):
    current_time = time.time()
    if pressed:
        click_times.append(current_time)
        box_x = int(x / (screen_width / 10))
        box_y = int(y / (screen_height / 10))
        click_hotspots[(box_x, box_y)] += 1

def on_move(x, y):
    mouse_movements.append((x, y))

def calculate_mouse_metrics():
    global mouse_movements, click_times

    avg_mouse_speed = 0
    if len(mouse_movements) > 1:
        distances = []
        for i in range(1, len(mouse_movements)):
            prev_x, prev_y = mouse_movements[i - 1]
            curr_x, curr_y = mouse_movements[i]
            distance = ((curr_x - prev_x) ** 2 + (curr_y - prev_y) ** 2) ** 0.5
            distances.append(distance)
        avg_mouse_speed = sum(distances) / len(distances)

    click_count = len(click_times)

    mouse_movements = []
    click_times = []

    return avg_mouse_speed, click_count

def calculate_double_click_speed():
    global click_times

    double_click_speed = 0
    if len(click_times) >= 2:
        double_click_intervals = [click_times[i] - click_times[i - 1] for i in range(1, len(click_times))]
        double_click_speed = sum(double_click_intervals) / len(double_click_intervals)

    return double_click_speed

def print_click_hotspots():
    print("Click hotspots:")
    for (box_x, box_y), count in click_hotspots.items():
        print(f"Box ({box_x}, {box_y}): {count} clicks")


    click_hotspots.clear()
