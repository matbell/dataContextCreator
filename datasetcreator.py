import argparse
import csv

import numpy as np
from tqdm import tqdm
from datetime import datetime
import os
from collections import Counter

from model import Example
from play_store import GooglePlayStore


def parse_arguments():

    parser = argparse.ArgumentParser(description='Creates the dataset for the ContextLabeler experiment.')

    parser.add_argument('-in', dest='inputDir', required=True,
                        help='Path of the directory which contains raw sensors data.')

    parser.add_argument('-out', dest='outputDir', required=True,
                        help='The path of the directory that will be used to store the dataset.')

    return parser.parse_args()


'''=====================================================================================================================
ACTIVITES (LABELS)
====================================================================================================================='''


def read_activities(main_dir):

    file_name = main_dir + '/activities.csv'

    activities = []

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            activities.append((int(row[0]), int(row[1]), row[2]))

    return activities


'''=====================================================================================================================
ACTIVITY RECOGNITION FEATURES
====================================================================================================================='''


def get_activity_recognition_data(main_dir, start, end):
    file_name = main_dir + '/activity.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data[time] = (int(row[1]), int(row[2]), row[3], row[4], row[5], row[6], row[7], row[8])

    return data


'''=====================================================================================================================
INSTALLED APPS
====================================================================================================================='''


def get_installed_apps_frequency(google, main_dir, start, end):
    file_name = main_dir + '/installed_apps.csv'

    frequencies = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                elements = []
                for element in row:
                    if element != time:
                        category = google.get_package_category(element)
                        if category is not None:
                            elements.append(category)

                d = Counter(elements)
                f = {}

                for key in d.keys():
                    f[key] = d.get(key)

                frequencies[time] = f

    return frequencies


'''=====================================================================================================================
RUNNING APPS
====================================================================================================================='''


def get_running_apps_frequency(google, main_dir, start, end):
    file_name = main_dir + '/running_apps.csv'

    categories = GooglePlayStore.get_apps_categories()

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        data = {}

        for row in rows:
            time = int(row[0])

            if start <= time <= end:

                apps = []

                for element in row:
                    if element != row[0]:
                        category = google.get_package_category(element)
                        if category is not None:
                            apps.append(category)

                c = dict(categories)

                if len(apps) > 0:
                    d = Counter(apps)

                    for key in d.keys():
                        c[key] = d.get(key)

                data[time] = c

    return data


'''=====================================================================================================================
WEATHER
====================================================================================================================='''


def get_weather_info(main_dir, start, end):
    file_name = main_dir + '/weather.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data[time] = (int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]),
                              float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]))
    return data


'''=====================================================================================================================
READS USED APPLICATIONS
====================================================================================================================='''


def reading_apps(google, main_dir, sub_dirs):

    apps = set()

    for dir in sub_dirs:

        file_name = main_dir + "/" + dir + '/installed_apps.csv'

        print("Reading apps in "+file_name)

        with open(file_name) as csvfile:
            rows = csv.reader(csvfile, delimiter='\t')

            for row in rows:
                try:
                    time = int(row[0])
                    for element in row:
                        if element != row[0]:
                            apps.add(element)
                except ValueError:
                    continue

    for app in tqdm(apps, desc="Downloading apps categories"):
        google.get_package_category(app)

    return


def bool_val(val):
    if val == "false":
        return -1
    return 1


'''=====================================================================================================================
AUDIO
====================================================================================================================='''


def get_audio_features(main_dir, start, end):
    file_name = main_dir + '/audio.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data[time] = (int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), bool_val(row[6]),
                              bool_val(row[7]), bool_val(row[8]), bool_val(row[9]), bool_val(row[10]))
                #data.append((time, int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]),
                #             bool_val(row[6]), bool_val(row[7]), bool_val(row[8]), bool_val(row[9]), bool_val(row[10])))
    return data


'''=====================================================================================================================
BATTERY
====================================================================================================================='''


def get_battery_features(main_dir, start, end):
    file_name = main_dir + '/battery.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data[time] = (float(row[1]), int(row[2]))
    return data


'''=====================================================================================================================
BLUETOOTH CONNECTIONS
====================================================================================================================='''


def get_bt_conn(main_dir, start, end):
    file_name = main_dir + '/bt_conn.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                devices = []
                if len(row) > 1 and len(row[1]) > 0:
                    for element in row:
                        if element != row[0]:
                            devices.append(element.split(",")[1])

                data[time] = devices
    return data


'''=====================================================================================================================
BLUETOOTH SCANS
====================================================================================================================='''


def get_bt_scans(main_dir, start, end):
    file_name = main_dir + '/bt_scan.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                devices = []
                if len(row) > 1 and len(row[1]) > 0:
                    for element in row:
                        if element != row[0]:
                            devices.append(element.split(",")[1])

                data[time] = devices
    return data


'''=====================================================================================================================
CALENDAR CURRENT EVENTS
====================================================================================================================='''


def get_calendar_current_events(main_dir, start, end):
    file_name = main_dir + '/calendar_current_events.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                if "compleanno" not in row[5]:
                    data[time] = (row[5], row[6])
    return data


'''=====================================================================================================================
DISPLAY
====================================================================================================================='''


def get_display_data(main_dir, start, end):
    file_name = main_dir + '/display.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data[time] = (int(row[1]), int(row[2]))
    return data


'''=====================================================================================================================
LOCATION
====================================================================================================================='''


def get_location_data(main_dir, start, end):
    file_name = main_dir + '/location.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data[time] = (float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]))
    return data


'''=====================================================================================================================
WIFI-P2P
====================================================================================================================='''


def get_wifi_p2p_data(main_dir, start, end):
    file_name = main_dir + '/wifi_p2p_scans.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:

                devices = []

                for device in row:
                    if device != row[0]:
                        devices.append(device)

                data[time] = devices
    return data


'''=====================================================================================================================
ENVIRONMENT SENSORS
====================================================================================================================='''


def get_environment_data(main_dir, start, end):
    file_name = main_dir + '/environment_sensors.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:

                light_raw_data = row[15:29]

                light_data = []
                if light_raw_data[0] != "NaN":
                    for raw_data in light_raw_data:
                        light_data.append(float(raw_data))

                    data[time] = light_data
    return data


'''=====================================================================================================================
MOTION SENSORS
====================================================================================================================='''


def get_motion_data(main_dir, start, end):
    file_name = main_dir + '/motion_sensors.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                raw_sensor_data = row[1:]
                sensor_data = []
                if raw_sensor_data[0] != "NaN":
                    for raw_data in raw_sensor_data:
                        sensor_data.append(float(raw_data))

                    data[time] = sensor_data
    return data


'''=====================================================================================================================
POSITION SENSORS
====================================================================================================================='''


def get_position_sensor_data(main_dir, start, end):
    file_name = main_dir + '/position_sensors.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                raw_sensor_data = row[1:]
                sensor_data = []
                if raw_sensor_data[0] != "NaN":
                    for raw_data in raw_sensor_data:
                        sensor_data.append(float(raw_data))

                    data[time] = sensor_data
    return data


'''=====================================================================================================================
WIFI
====================================================================================================================='''


def get_wifi_data(main_dir, start, end):
    file_name = main_dir + '/wifi_scans.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:

                devices = []

                for device in row:
                    if device != row[0]:
                        mac = device.split(",")[1]
                        signal = device.split(",")[2]
                        dbm = device.split(",")[3]
                        connected = 0
                        if device.split(",")[5] == "true":
                            connected = 1
                        configured = 0
                        if device.split(",")[6] == "true":
                            configured = 1
                        devices.append((mac, signal, dbm, connected, configured))

                data[time] = devices
    return data


'''=====================================================================================================================
VISIBLE CELLS
====================================================================================================================='''


def get_visible_cells(main_dir, start, end):
    file_name = main_dir + '/cells.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                cells = []
                if row[1] != "":
                    for element in row:
                        if element != row[0]:
                            cells.append((element.split(",")[0], element.split(",")[1], element.split(",")[2]))

                data[time] = cells
    return data


'''=====================================================================================================================
TIME
====================================================================================================================='''


def get_time_info(timestamp):

    weekno = datetime.fromtimestamp(timestamp).weekday()
    day_type = 0

    if weekno >= 5:
        day_type = 1

'''=====================================================================================================================
MAIN
====================================================================================================================='''


def get_nearest_example(time, data, max_diff):

    diffs = []

    for key in data.keys():
        diffs.append(abs(time-key))

    example = None

    if len(diffs) != 0:

        if max_diff is not None and min(diffs) <= max_diff:
            key = list(data.keys())[diffs.index(min(diffs))]
            example = data[key]

        elif max_diff is None:
            key = list(data.keys())[diffs.index(min(diffs))]
            example = data[key]

    return example


if __name__ == '__main__':

    args = parse_arguments()
    google = GooglePlayStore()

    main_dir = args.inputDir
    users_dirs = [dI for dI in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, dI))]

    reading_apps(google, main_dir, users_dirs)

    for user in users_dirs:

        user_dir = main_dir + "/" + user

        activities = read_activities(user_dir)

        act_examples = {}

        for activity in activities:
            start = activity[0]
            end = activity[1]
            label = activity[2]

            span = 1000*60*30

            print("Activity: "+label)

            audio_features = get_audio_features(user_dir, start - span, end + span)
            battery_features = get_battery_features(user_dir, start - span, end + span)
            activity_rec_data = get_activity_recognition_data(user_dir, start - span, end + span)
#            running_apps = get_running_apps_frequency(google, user_dir, start - span, end + span)
            bt_conn = get_bt_conn(user_dir, start - span, end + span)
            bt_scans = get_bt_scans(user_dir, start - span, end + span)
            current_events = get_calendar_current_events(user_dir, start - span, end + span)
            visible_cells = get_visible_cells(user_dir, start - span, end + span)
            display_status = get_display_data(user_dir, start - span, end + span)
            location_data = get_location_data(user_dir, start - span, end + span)
            weather_info = get_weather_info(user_dir, start - span, end + span)
            wifi_p2p = get_wifi_p2p_data(user_dir, start - span, end + span)
            wifi = get_wifi_data(user_dir, start - span, end + span)
            environment_data = get_environment_data(user_dir, start - span, end + span)
            motion_data = get_motion_data(user_dir, start - span, end + span)
            position_sensor_data = get_position_sensor_data(user_dir, start - span, end + span)

            # remove the 20% of the data at the beginning and end
            start = int(start + ((end - start) * 0.2))
            end = int(end - ((end - start) * 0.2))

            minute = start

            not_valid = 0

            while minute <= end:

                example = Example()
                example.audio = get_nearest_example(minute, audio_features, 60000)
                example.battery = get_nearest_example(minute, battery_features, 60000)
                example.activity_rec = get_nearest_example(minute, activity_rec_data, 60000)
                #example.running_apps = get_nearest_example(minute, running_apps, 180000)
                example.bt_conn = get_nearest_example(minute, bt_conn, None)
                example.bt_scan = get_nearest_example(minute, bt_scans, 60000)
                example.current_calendar_events = get_nearest_example(minute, current_events, 60000)
                if example.current_calendar_events == None:
                    example.current_calendar_events = 0
                example.visible_cells = get_nearest_example(minute, visible_cells, 60000)
                example.display = get_nearest_example(minute, display_status, 60000)
                example.location = get_nearest_example(minute, location_data, 180000)
                example.weather = get_nearest_example(minute, weather_info, 3600000)
                example.wifi_p2p = get_nearest_example(minute, wifi_p2p, 120000)
                example.wifi = get_nearest_example(minute, wifi, 180000)
                example.environment_sensors = get_nearest_example(minute, environment_data, 300000)
                example.motion_sensors = get_nearest_example(minute, motion_data, 300000)
                example.position_sensors = get_nearest_example(minute, position_sensor_data, 300000)
                example.time = minute
                example.label = label

                minute = minute + 60000

                exs = []
                if label in act_examples:
                    exs = act_examples[label]

                #if example.is_valid():
                exs.append(example)
                act_examples[label] = exs

        audio = 0
        batter = 0
        activity_rec = 0
        bt_con = 0
        bt_scan = 0
        cal = 0
        cel = 0
        dis = 0
        loc = 0
        weather = 0
        wp2p = 0
        wf = 0
        env = 0
        mot = 0
        pos = 0
        time = 0
        label = 0
        total_count = 0
        for l in act_examples.keys():
            for ex in act_examples[l]:
                #print(l + ": " + str(act_examples[l]))
                if ex.audio is not None:
                    audio = audio +1
                if ex.battery is not None:
                    batter = batter +1
                if ex.activity_rec is not None:
                    activity_rec = activity_rec +1
                if ex.current_calendar_events is not None:
                    cal = cal +1
                if ex.visible_cells is not None:
                    cel = cel +1
                if ex.display is not None:
                    dis = dis +1
                if ex.location is not None:
                    loc = loc + 1
                if ex.weather is not None:
                    weather = weather +1
                if ex.wifi_p2p is not None:
                    wp2p = wp2p +1
                if ex.wifi is not None:
                    wf = wf +1
                if ex.bt_conn is not None:
                    bt_con = bt_con +1
                if ex.bt_scan is not None:
                    bt_scan = bt_scan +1
                if ex.environment_sensors is not None:
                    env = env +1
                if ex.motion_sensors is not None:
                    mot = mot +1
                if ex.position_sensors is not None:
                    pos = pos+1

                total_count = total_count +1

        print("Audio: "+str(audio) + "/" + str(total_count))
        print("Battery: " + str(batter) + "/" + str(total_count))
        print("Activity rec: " + str(activity_rec) + "/" + str(total_count))
        print("BT CON: " + str(bt_con) + "/" + str(total_count))
        print("BT SCAN: " + str(bt_scan) + "/" + str(total_count))
        print("Calendar: " + str(cal) + "/" + str(total_count))
        print("Cells: " + str(cel) + "/" + str(total_count))
        print("Display: " + str(dis) + "/" + str(total_count))
        print("Location: " + str(loc) + "/" + str(total_count))
        print("Weather: " + str(weather) + "/" + str(total_count))
        print("Wi-Fi P2P: " + str(wp2p) + "/" + str(total_count))
        print("Wi-Fi: " + str(wf) + "/" + str(total_count))
        print("Environment: " + str(env) + "/" + str(total_count))
        print("Motion: " + str(mot) + "/" + str(total_count))
        print("Position: " + str(pos) + "/" + str(total_count))
