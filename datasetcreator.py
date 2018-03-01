import argparse
import csv

import numpy as np
from tqdm import tqdm
import os
from collections import Counter
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

    data = []

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data.append((time, int(row[1]), int(row[2]), row[3], row[4], row[5], row[6], row[7], row[8]))

    return data


'''=====================================================================================================================
INSTALLED APPS
====================================================================================================================='''


def get_installed_apps_frequency(google, main_dir, start, end):
    file_name = main_dir + '/installed_apps.csv'

    frequencies = []

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

                frequencies.append((time, f))

    return frequencies


'''=====================================================================================================================
RUNNING APPS
====================================================================================================================='''


def get_running_apps_frequency(google, main_dir, start, end):
    file_name = main_dir + '/running_apps.csv'

    categories = GooglePlayStore.get_apps_categories()

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        data = []

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

                data.append((time, c))

    return data


'''=====================================================================================================================
WEATHER
====================================================================================================================='''


def get_weather_info(main_dir, start, end):
    file_name = main_dir + '/weather.csv'

    data = []

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data.append((time, int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]),
                             float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10]),
                             float(row[11])))
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

    data = []

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data.append((time, float(row[1]), int(row[2])))
    return data


'''=====================================================================================================================
BLUETOOTH CONNECTIONS
====================================================================================================================='''


def get_bt_conn(main_dir, start, end):
    file_name = main_dir + '/bt_conn.csv'

    data = []

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

                data.append((time, devices))
    print(data)
    return data


'''=====================================================================================================================
BLUETOOTH SCANS
====================================================================================================================='''


def get_bt_scans(main_dir, start, end):
    file_name = main_dir + '/bt_scan.csv'

    data = []

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

                data.append((time, devices))
    return data


'''=====================================================================================================================
CALENDAR CURRENT EVENTS
====================================================================================================================='''


def get_calendar_current_events(main_dir, start, end):
    file_name = main_dir + '/calendar_current_events.csv'

    data = []

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                if "compleanno" not in row[5]:
                    data.append((time, row[5], row[6]))
    return data


'''=====================================================================================================================
DISPLAY
====================================================================================================================='''


def get_display_data(main_dir, start, end):
    file_name = main_dir + '/display.csv'

    data = []

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data.append((time, int(row[1]), int(row[2])))
    return data


'''=====================================================================================================================
LOCATION
====================================================================================================================='''


def get_location_data(main_dir, start, end):
    file_name = main_dir + '/location.csv'

    data = []

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:
                data.append((time, float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]),
                             float(row[6])))
    return data


'''=====================================================================================================================
WIFI-P2P
====================================================================================================================='''


def get_wifi_p2p_data(main_dir, start, end):
    file_name = main_dir + '/wifi_p2p_scans.csv'

    data = []

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if start <= time <= end:

                devices = []

                for device in row:
                    if device != row[0]:
                        devices.append(device)

                data.append((time, devices))
    return data


'''=====================================================================================================================
ENVIRONMENT SENSORS
====================================================================================================================='''


def get_environment_data(main_dir, start, end):
    file_name = main_dir + '/environment_sensors.csv'

    data = []

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

                    data.append((time, light_data))
    return data


'''=====================================================================================================================
MOTION SENSORS
====================================================================================================================='''


def get_motion_data(main_dir, start, end):
    file_name = main_dir + '/motion_sensors.csv'

    data = []

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

                    data.append((time, sensor_data))
    return data


'''=====================================================================================================================
POSITION SENSORS
====================================================================================================================='''


def get_position_sensor_data(main_dir, start, end):
    file_name = main_dir + '/position_sensors.csv'

    data = []

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

                    data.append((time, sensor_data))
    return data


'''=====================================================================================================================
WIFI
====================================================================================================================='''


def get_wifi_data(main_dir, start, end):
    file_name = main_dir + '/wifi_scans.csv'

    data = []

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

                data.append((time, devices))
    return data


'''=====================================================================================================================
VISIBLE CELLS
====================================================================================================================='''


def get_visible_cells(main_dir, start, end):
    file_name = main_dir + '/cells.csv'

    data = []

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

                data.append((time, cells))
    return data


'''=====================================================================================================================
MAIN
====================================================================================================================='''


def get_nearest_example(time, data, max_diff):

    diffs = []

    for key in data.keys():
        diffs.append(abs(time-key))

    example = None
    if min(diffs) <= max_diff:
        key = list(data.keys())[diffs.index(min(diffs))]
        example = data[key]
        print(min(diffs)/1000)

    return example


if __name__ == '__main__':

    args = parse_arguments()
    google = GooglePlayStore()

    main_dir = args.inputDir
    users_dirs = [dI for dI in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, dI))]

    #reading_apps(google, main_dir, users_dirs)

    for user in users_dirs:

        user_dir = main_dir + "/" + user

        activities = read_activities(user_dir)

        for activity in activities:
            start = activity[0]
            end = activity[1]
            label = activity[2]

            #remove the 20% of the data at the beginning and end
            start = int(start + ((end - start) * 0.2))
            end = int(end - ((end - start) * 0.2))

            audio_features = get_audio_features(user_dir, start, end)
            '''
            battery_features = get_battery_features(user_dir, start, end)
            activity_rec_data = get_activity_recognition_data(user_dir, start, end)
            running_apps = get_running_apps_frequency(google, user_dir, start, end)
            bt_conn = get_bt_conn(user_dir, start, end)
            bt_scans = get_bt_scans(user_dir, start, end)
            current_events = get_calendar_current_events(user_dir, start, end)
            visible_cells = get_visible_cells(user_dir, start, end)
            display_status = get_display_data(user_dir, start, end)
            location_data = get_location_data(user_dir, start, end)
            weather_info = get_weather_info(user_dir, start, end)
            wifi_p2p = get_wifi_p2p_data(user_dir, start, end)
            wifi = get_wifi_data(user_dir, start, end)
            environment_data = get_environment_data(user_dir, start, end)
            motion_data = get_motion_data(user_dir, start, end)
            position_sensor_data = get_position_sensor_data(user_dir, start, end)
            print(label + ": "+str(start)+" - "+str(end))
            print("Audio samples: "+str(len(audio_features)))
            print("Battery samples: " + str(len(battery_features)))
            print("Activity Recognition samples: " + str(len(activity_rec_data)))
            print("Running Apps samples: " + str(len(running_apps)))
            print("Current events: " + str(len(current_events)))
            print("Visible cells: " + str(len(visible_cells)))
            print("Display statuses: " + str(len(display_status)))
            #app_installed_frequencies = get_installed_apps_frequency(google, user_dir, start, end)
            '''

            count = 0
            minute = start
            #print(activity)
            while minute < end:
                audio = get_nearest_example(minute, audio_features, 60000)
                minute = minute + 60000
                if audio is not None:
                    count = count +1

            print("Examples in " + str(int((end-start)/60000)) + " minutes: "+str(count))

