import csv
from collections import Counter
from tqdm import tqdm
import os.path

from utils import normalize_mac, mac_to_int

'''
Files:
    - activities.csv                    labels
    - activity.csv                      activity recognition
    - apps_usage.csv                    apps usage statistics
    - audio.csv                         audio settings
    - battery.csv                       battery status
    - bt_conn.csv                       connected BT devices
    - bt_scan.csv                       BT devices in proximity
    - calendar_current_events.csv       current calendar events
    - calls.csv                         calls log
    - cells.csv                         visible phone cells
    - display.csv                       display status
    - environment_sensors.csv           temperature, light, pressure, relative humidity
    - hardware_info.csv                 Android ID, Wi-Fi MAC, WFD MAC, BT MAC, brand, model, manufacturer, device ID
    - installed_apps.csv                list of installed packages
    - location.csv                      GPS location
    - motion_sensors.csv                accelerometer, gravity, gyroscope, acceleration, rotation
    - position_sensors.csv              game rotation vector,geomagnetic rotation, magnetic, proximity      
    - running_apps.csv                  list of running apps (last 5 minutes)
    - sms.csv                           received/sent sms
    - weather.csv                       weather conditions
    - wifi_p2p_scans.csv                list of Wi-Fi P2P devices in proximity
    - wifi_scans.csv                    list of Wi-FI AP in proximity
    - multimedia.csv                    picture/videos
'''


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
            if normalize:
                data[time] = (int(row[1])/100, int(row[2])/100, int(row[3])/100, int(row[4])/100, int(row[5])/100,
                              int(row[6])/100, int(row[7])/100, int(row[8])/100)
            else:
                data[time] = (int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]),
                              int(row[8]))

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

    print("Reading running apps from " + file_name)

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        data = {}

        for row in rows:
            time = int(row[0])

            categories = google.get_categories()

            for element in row:
                if element != row[0]:
                    category = google.get_package_category(element)
                    if category is not None:
                        categories[category] = 1

            data[time] = list(categories.values())

    return data


def get_running_apps(google, main_dir):
    file_name = main_dir + '/running_apps.csv'

    print("Reading running apps from " + file_name)

    global normalize

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        data = {}

        categories = google.get_categories()

        for row in rows:
            time = int(row[0])

            cat = 0

            for element in row:
                if element != row[0]:
                    category = google.get_package_category(element)
                    if category is not None:
                        cat = categories[category]

            if normalize:
                cat = cat / 59
            data[time] = cat

    return data


'''=====================================================================================================================
WEATHER
====================================================================================================================='''


def get_weather_info(main_dir):
    file_name = main_dir + '/weather.csv'

    data = {}

    global normalize

    # temp = [-50, 50]
    temp_c_max = 50
    temp_c_range = 100

    #wind speed = [0, 100] m/s
    max_wind_speed = 100

    # wind direction http://snowfence.umn.edu/Components/winddirectionanddegreeswithouttable3.htm
    max_wind_direction = 348.75

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

            if normalize:
                #http://www.openweathermap.com/current
                weather_code = int(row[1])/962
                temp = (float(row[2]) + temp_c_max)/temp_c_range
                temp_min = (float(row[3]) + temp_c_max) / temp_c_range
                temp_max = (float(row[4]) + temp_c_max) / temp_c_range
                humidity = float(row[5]) / 100.0
                pressure = float(row[6])
                wind_speed = float(row[7]) / max_wind_speed
                wind_direction = float(row[8]) / max_wind_direction
                cloudiness = float(row[9]) / 100.0

                data[time] = (weather_code, temp, temp_min, temp_max, humidity, pressure, wind_speed, wind_direction,
                              cloudiness, float(row[10]), float(row[11]))
            else:
                data[time] = (int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]),
                              float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]))
    return data


'''=====================================================================================================================
READS INSTALLED APPLICATIONS
====================================================================================================================='''


def read_installed_apps(main_dir, sub_dirs, google):

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


'''
 Reads both installed and running apps
'''


def read_all_apps(main_dir, sub_dirs):

    apps = set()

    for dir in sub_dirs:

        installed_apps_file = main_dir + "/" + dir + '/installed_apps.csv'
        running_apps_file = main_dir + "/" + dir + '/running_apps.csv'

        with open(installed_apps_file) as csvfile:
            rows = csv.reader(csvfile, delimiter='\t')

            for row in rows:
                try:
                    for element in row[1:]:
                        apps.add(element)
                except ValueError:
                    continue

        with open(running_apps_file) as csvfile:
            rows = csv.reader(csvfile, delimiter='\t')

            for row in rows:
                try:
                    for element in row[1:]:
                        apps.add(element)
                except ValueError:
                    continue

    return apps


def bool_val(val):
    if val == "false":
        return 0
    return 1


'''=====================================================================================================================
AUDIO
====================================================================================================================='''


def get_audio_features(main_dir):
    file_name = main_dir + '/audio.csv'

    data = {}

    global normalize

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

            # row[1] = ringer_mode (0: silent, 1: vibrate, 2: normal)
            if normalize:
                data[time] = (int(row[1])/2, float(row[2]), float(row[3]), float(row[4]), float(row[5]),
                              bool_val(row[6]), bool_val(row[7]), bool_val(row[8]), bool_val(row[9]), bool_val(row[10]))
            else:
                data[time] = (int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), bool_val(row[6]),
                              bool_val(row[7]), bool_val(row[8]), bool_val(row[9]), bool_val(row[10]))

    return data


'''=====================================================================================================================
BATTERY
====================================================================================================================='''


def get_battery_features(main_dir):
    file_name = main_dir + '/battery.csv'

    data = {}

    global normalize

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])

            level = float(row[1])
            connected = int(row[2])

            if normalize:
                connected = connected / 4

            data[time] = (level, connected)

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
                        if normalize:
                            # Max BT Major device class is "Uncategorized" = 7936
                            # https://developer.android.com/reference/android/bluetooth/BluetoothClass.Device.Major.html
                            devices.append((normalize_mac(element.split(",")[1]), int(element.split(",")[2])/7936))
                        else:
                            devices.append((mac_to_int(element.split(",")[1]), int(element.split(",")[2])))

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
                    # Append MAC ADDRESS, Device BT Major ID, and RSSI
                    if element != row[0]:
                        if normalize:
                            # Max BT Major device class is "Uncategorized" = 7936
                            # https://developer.android.com/reference/android/bluetooth/BluetoothClass.Device.Major.html
                            devices.append((normalize_mac(element.split(",")[1]), int(element.split(",")[2])/7936,
                                            element.split(",")[3]))
                        else:
                            devices.append((mac_to_int(element.split(",")[1]), int(element.split(",")[2]),
                                            element.split(",")[3]))

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

            if len(row) > 1 and len(row[1]) > 1:
                data[time] = row[5]

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
            if normalize:
                # row[1] = display state (0: unknown, 1: sate_off, 2: state_on, 3: state_doze, 4: state_doze_suspend)
                data[time] = (int(row[1])/4, int(row[2]))
            else:
                data[time] = (int(row[1]), int(row[2]))

    return data


'''=====================================================================================================================
LOCATION
====================================================================================================================='''


def get_location_data(main_dir):
    file_name = main_dir + '/location.csv'

    data = {}

    # lat = [-90, 90]
    max_lat = 90
    lat_range = 180

    # lat = [-180, 180]
    max_lng = 180
    lng_range = 360

    # bearing = [0, 360]
    max_bearing = 360

    with open(file_name) as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')

        for row in rows:
            time = int(row[0])
            if normalize:
                # https://developers.google.com/android/reference/com/google/android/gms/maps/model/LatLng
                data[time] = ((float(row[1]) + max_lat)/lat_range, (float(row[2]) + max_lng)/lng_range, float(row[3]),
                              float(row[4]), float(row[5])/max_bearing, float(row[6]))
            else:
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
                    if(len(device)) > 0:
                        if normalize:
                            devices.append(normalize_mac(device))
                        else:
                            devices.append(mac_to_int(device))

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
            raw_sensor_data = row[1:]
            sensors = [raw_sensor_data[x:x + 14] for x in range(0, len(raw_sensor_data), 14)]
            # Keep only light data
            raw_sensor_data = sensors[1]
            raw_sensor_data = raw_sensor_data[:8]
            raw_sensor_data = [float(a) for a in raw_sensor_data]
            if len(set(raw_sensor_data)) > 1:
                data[time] = raw_sensor_data

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
            raw_sensor_data = [float(a) for a in raw_sensor_data]

            sensors = [raw_sensor_data[x:x + 42] for x in range(0, len(raw_sensor_data), 42)]
            raw_sensor_data = []

            for sensor in sensors:
                dimensions = [sensor[x:x + 14] for x in range(0, len(sensor), 14)]

                for dim in dimensions:
                    raw_sensor_data.extend(dim[:8])

            if len(set(raw_sensor_data)) > 1:
                data[time] = raw_sensor_data

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
            raw_sensor_data = [float(a) for a in raw_sensor_data]
            # Keep only data related to the Proximity sensor
            raw_sensor_data = raw_sensor_data[-14:]

            if len(set(raw_sensor_data)) > 1:
                data[time] = raw_sensor_data[:8]

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
                if device != row[0] and len(device) > 0:
                    bssid = device.split(",")[1]
                    signal = int(device.split(",")[2])
                    dbm = device.split(",")[3]

                    # False = 0.5, because 0 means MISSING VALUE
                    connected = 0.5
                    if device.split(",")[5] == "true":
                        connected = 1
                    configured = 0.5
                    if device.split(",")[6] == "true":
                        configured = 1

                    if normalize:
                        bssid = normalize_mac(bssid)
                        # Max signal level = 4
                        devices.append((bssid, signal/4, dbm, connected, configured))
                    else:
                        bssid = mac_to_int(bssid)
                        devices.append((bssid, signal, dbm, connected, configured))

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

    if os.path.isfile(file_name):
        with open(file_name) as csvfile:
            rows = csv.reader(csvfile, delimiter='\t')

            for row in rows:

                file_type = 0

                if len(row) <= 1 or len(row[1]) == 0:
                    file_type = 0
                elif ".png" in row[1] or ".jpg" in row[1]:
                    file_type = 1
                elif ".avi" in row[1] or ".mp4" in row[1]:
                    file_type = 2

                if normalize:
                    data[int(row[0])] = file_type/2
                else:
                    data[int(row[0])] = file_type

    return data


'''=====================================================================================================================
MULTIMEDIA DATA
====================================================================================================================='''


def load_data(user_dir, google, norm):

    global normalize
    normalize = norm

    audio_features = get_audio_features(user_dir)
    battery_features = get_battery_features(user_dir)
    activity_rec_data = get_activity_recognition_data(user_dir)
    running_apps = get_running_apps_frequency(google, user_dir)
    #running_apps = get_running_apps(google, user_dir)
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
           position_sensor_data, multimedia_data, running_apps