import csv
from collections import Counter
from play_store import GooglePlayStore
from tqdm import tqdm


'''=====================================================================================================================
ACTIVITES (LABELS)
===================================================================================================================='''


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


def get_activity_recognition_data(main_dir):
    file_name = main_dir + '/activity.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            data[time] = (int(row[1]), int(row[2]), row[3], row[4], row[5], row[6], row[7], row[8])

    return data


'''=====================================================================================================================
INSTALLED APPS
====================================================================================================================='''


def get_installed_apps_frequency(google, main_dir):
    file_name = main_dir + '/installed_apps.csv'

    frequencies = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
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


def get_running_apps_frequency(google, main_dir):
    file_name = main_dir + '/running_apps.csv'

    categories = GooglePlayStore.get_apps_categories()

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        data = {}

        for row in rows:
            time = int(row[0])

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


def get_weather_info(main_dir):
    file_name = main_dir + '/weather.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            data[time] = (int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]),
                          float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]))
    return data


'''=====================================================================================================================
READS INSTALLED APPLICATIONS
====================================================================================================================='''


def read_installed_apps(main_dir, sub_dirs):

    google = GooglePlayStore()

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


def get_audio_features(main_dir):
    file_name = main_dir + '/audio.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            data[time] = (int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), bool_val(row[6]),
                          bool_val(row[7]), bool_val(row[8]), bool_val(row[9]), bool_val(row[10]))

    return data


'''=====================================================================================================================
BATTERY
====================================================================================================================='''


def get_battery_features(main_dir):
    file_name = main_dir + '/battery.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            data[time] = (float(row[1]), int(row[2]))

    return data


'''=====================================================================================================================
BLUETOOTH CONNECTIONS
====================================================================================================================='''


def get_bt_conn(main_dir):
    file_name = main_dir + '/bt_conn.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
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


def get_bt_scans(main_dir):
    file_name = main_dir + '/bt_scan.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

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


def get_calendar_current_events(main_dir):
    file_name = main_dir + '/calendar_current_events.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

            if "compleanno" not in row[5]:
                data[time] = (row[5], row[6])
    return data


'''=====================================================================================================================
DISPLAY
====================================================================================================================='''


def get_display_data(main_dir):
    file_name = main_dir + '/display.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            data[time] = (int(row[1]), int(row[2]))

    return data


'''=====================================================================================================================
LOCATION
====================================================================================================================='''


def get_location_data(main_dir):
    file_name = main_dir + '/location.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            data[time] = (float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]))

    return data


'''=====================================================================================================================
WIFI-P2P
====================================================================================================================='''


def get_wifi_p2p_data(main_dir):
    file_name = main_dir + '/wifi_p2p_scans.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

            devices = []

            for device in row:
                if device != row[0]:
                    devices.append(device)

            data[time] = devices

    return data


'''=====================================================================================================================
ENVIRONMENT SENSORS
====================================================================================================================='''


def get_environment_data(main_dir):
    file_name = main_dir + '/environment_sensors.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

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


def get_motion_data(main_dir):
    file_name = main_dir + '/motion_sensors.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

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


def get_position_sensor_data(main_dir):
    file_name = main_dir + '/position_sensors.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

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


def get_wifi_data(main_dir):
    file_name = main_dir + '/wifi_scans.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

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


def get_visible_cells(main_dir):
    file_name = main_dir + '/cells.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

            cells = []
            if row[1] != "":
                for element in row:
                    if element != row[0]:
                        cells.append((element.split(",")[0], element.split(",")[1], element.split(",")[2]))

            data[time] = cells

    return data


'''=====================================================================================================================
MULTIMEDIA DATA
====================================================================================================================='''


def get_multimedia_data(main_dir):
    file_name = main_dir + '/multimedia.csv'

    data = {}

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            data[int(row[0])] = row[1]

    return data


'''=====================================================================================================================
MULTIMEDIA DATA
====================================================================================================================='''


def load_data(user_dir):

    audio_features = get_audio_features(user_dir)
    battery_features = get_battery_features(user_dir)
    activity_rec_data = get_activity_recognition_data(user_dir)
    #running_apps = get_running_apps_frequency(google, user_dir)
    bt_conn = get_bt_conn(user_dir)
    bt_scans = get_bt_scans(user_dir)
    current_events = get_calendar_current_events(user_dir)
    visible_cells = get_visible_cells(user_dir)
    display_status = get_display_data(user_dir)
    location_data = get_location_data(user_dir)
    weather_info = get_weather_info(user_dir)
    wifi_p2p = get_wifi_p2p_data(user_dir)
    wifi = get_wifi_data(user_dir)
    environment_data = get_environment_data(user_dir)
    motion_data = get_motion_data(user_dir)
    position_sensor_data = get_position_sensor_data(user_dir)
    multimedia_data = get_multimedia_data(user_dir)

    return audio_features, battery_features, activity_rec_data, bt_conn, bt_scans, current_events, visible_cells,\
           display_status, location_data, weather_info, wifi_p2p, wifi, environment_data, motion_data,\
           position_sensor_data, multimedia_data