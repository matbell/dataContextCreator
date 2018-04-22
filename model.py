from datetime import datetime
import calendar
from math import ceil


class Example:
    
    def __init__(self, time, label, audio_features, battery_features, activity_rec_data, bt_conn, bt_scans,
                 current_events, visible_cells, display_status, location_data, weather_info, wifi_p2p, wifi,
                 environment_data, motion_data, position_sensor_data, multimedia_data, running_apps, normalize):

        min_millis = 60000

        self.audio = Example.get_nearest_example(time, audio_features, None)

        self.battery = Example.get_nearest_example(time, battery_features, None)

        self.activity_rec = Example.get_nearest_example(time, activity_rec_data, None)
        self.current_apps = self.get_nearest_example(time, running_apps, None)
        self.bt_conn = Example.get_nearest_example(time, bt_conn, None)
        self.bt_scan = Example.get_nearest_example(time, bt_scans, min_millis)

        if self.bt_scan is None:
            self.bt_scan = []

        self.current_calendar_events = Example.get_nearest_example(time, current_events, 10 * min_millis)

        if self.current_calendar_events is None:
            self.current_calendar_events = []

        self.multimedia = self.get_nearest_example(time, multimedia_data, 5 * min_millis)
        if self.multimedia is None:
            self.multimedia = 0

        self.visible_cells = Example.get_nearest_example(time, visible_cells, None)
        self.display = Example.get_nearest_example(time, display_status, None)
        self.display_on_count = Example.get_display_on_count(time, display_status, 5 * min_millis)
        self.location = Example.get_nearest_example(time, location_data, None)
        self.weather = Example.get_nearest_example(time, weather_info, None)
        self.wifi_p2p = Example.get_nearest_example(time, wifi_p2p, None)

        if self.wifi_p2p is None:
            self.wifi_p2p = []

        self.wifi = Example.get_nearest_example(time, wifi, None)

        if self.wifi is None:
            self.wifi = []

        #self.environment_sensors = Example.get_nearest_example(time, environment_data, 30 * min_millis)
        #self.motion_sensors = Example.get_nearest_example(time, motion_data, 20 * min_millis)
        #self.position_sensors = Example.get_nearest_example(time, position_sensor_data, 20 * min_millis)
        self.get_time_info(time, normalize)
        self.raw_time = time
        self.label = label

    @staticmethod
    def get_nearest_example(time, data, max_diff=None):

        relevant_data = {k: v for k, v in data.items() if k <= time}

        example = None

        if len(relevant_data) != 0:

            key = min(relevant_data.keys(), key=lambda k: abs(k - time))

            if max_diff is None or (max_diff is not None and abs(time-key) <= max_diff):
                example = relevant_data.get(time, relevant_data[key])

        return example

    @staticmethod
    def get_display_on_count(time, data, max_diff=None):

        relevant_data = {k: v for k, v in data.items() if k <= time and k >= (abs(max_diff - time))}

        count = 0

        for data in relevant_data.values():
            if data[0] == 2:
                count += 1

        return count

    def week_of_month(self, dt):
        """ Returns the week of the month for the specified date.
        """

        first_day = dt.replace(day=1)

        dom = dt.day
        adjusted_dom = dom + first_day.weekday()

        return int(ceil(adjusted_dom / 7.0))

    def get_time_info(self, timestamp, normalize):

        dt = datetime.fromtimestamp(timestamp / 1000.0)

        dt.replace(microsecond=0)

        # Hour
        start = datetime(dt.year, dt.month, dt.day, 0, 0, 0)
        end = datetime(dt.year, dt.month, dt.day, 23, 59, 59)

        norm_hour = (dt - start).seconds / (end - start).seconds

        if normalize:
            # Day of the week (0 = Monday, 6 = Sunday)
            norm_day_of_week = dt.weekday()/6
        else:
            norm_day_of_week = dt.weekday()

        if normalize:
            # Month of the year (1 = Gen, 12 = Dec)
            norm_month = (dt.month-1)/11
        else:
            norm_month = (dt.month - 1)

        if normalize:
            # Week of the month
            week = self.week_of_month(dt) / 4
        else:
            week = self.week_of_month(dt)

        if normalize:
            # Day of month
            number_of_days = calendar.monthrange(dt.year, dt.month)[1]
            norm_day_of_month = (dt.day - 1) / (number_of_days - 1)
        else:
            norm_day_of_month = dt.day - 1

        # day_type  0 = working day     1 = weekend
        day_type = 0

        # time       0 = morning         1 = afternoon       2 = evening         3 = night
        hour_semantic = 0

        if dt.weekday() >= 5:
            day_type = 1

        if 5 <= dt.hour <= 12:
            hour_semantic = 0
        elif 13 <= dt.hour <= 16:
            hour_semantic = 1
        elif 17 <= dt.hour <= 22:
            hour_semantic = 2
        elif 23 <= dt.hour <= 24 or 0 <= dt.hour <= 4:
            hour_semantic = 3

        if normalize:
            hour_semantic = hour_semantic / 3

        #self.time_info = (norm_month, week, norm_day_of_month, norm_day_of_week, day_type, norm_hour, hour_semantic)
        self.time_info = (day_type, norm_hour, hour_semantic)

    def is_valid(self):
        fields = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]

        for field in fields:
            if getattr(self, field) is None:
                print(field + " is None!")
                return False

        return True

    def get_features_vector(self):

        features = []

        # ---- TIME (7 features) --------
        features.extend(self.time_info)

        # ---- AUDIO (10 features) -------
        features.extend(self.audio)

        # ---- DISPLAY (2 features) -----
        features.extend(self.display)

        # ---- DISPLAY COUNT -----
        features.append(self.display_on_count)

        # ---- BATTERY (2 features) -----
        features.extend(self.battery)

        # ---- ACTIVITY RECOGNITION (8 features) -----
        features.extend(self.activity_rec)

        # ---- RUNNING APPS CATEGORIES (57 features) -----
        features.extend(self.current_apps)

        # ---- BLUETOOTH CONNECTIONS (6 features) -----
        bt = []
        for dev in self.bt_conn:
            bt.append(dev[0])
            bt.append(dev[1])

        bt = (bt + [0] * 3 * 2)[:3 * 2]
        features.extend(bt)

        # ---- BLUETOOTH SCANS (10 features) -----
        bt = []
        self.bt_scan.sort(key=lambda tup: tup[2], reverse=False)
        for dev in self.bt_scan[0:5]:
            bt.append(dev[0])
            bt.append(dev[1])

        bt = (bt + [0] * 5 * 2)[:5 * 2]
        features.extend(bt)

        # ---- CALENDAR CURRENT EVENTS (1 features) -----
        if len(self.current_calendar_events) > 0:
            features.append(1)
        else:
            features.append(0)

        # ---- MULTIMEDIA (1 features) -----
        features.append(self.multimedia)

        # ---- LOCATION (3 features) -----
        features.extend([self.location[0], self.location[1], self.location[4]])

        # ---- WEATHER (9 features) -----
        features.extend(self.weather[:9])

        # ---- WIFI-P2P (5 features) ----
        wifi_p2p = []
        wifi_p2p.extend(self.wifi_p2p)
        wifi_p2p = (wifi_p2p + [0] * 5)[:5]
        features.extend(wifi_p2p)

        # ---- WIFI (20 features) ----
        wifi = []
        self.wifi.sort(key=lambda tup: tup[1], reverse=True)
        for ap in self.wifi[0:5]:
            wifi.append(ap[0])
            wifi.append(ap[1])
            wifi.append(ap[3])
            wifi.append(ap[4])

        wifi = (wifi + [0] * 5*4)[:5*4]
        features.extend(wifi)

        # ---- ENVIRONMENT SENSORS (8 features = light sensor) ----
        #features.extend(self.environment_sensors)

        # ---- MOTION SENSORS (120 features) ----
        #features.extend(self.motion_sensors)

        # ---- POSITION SENSORS (8 features = proximity sensor) ----
        #features.extend(self.position_sensors)

        return features
