from datetime import datetime


class Example:

    time_info = None

    label = None

    audio = None
    battery = None
    activity_rec = None
    #running_apps = None
    current_calendar_events = None
    visible_cells = None
    display = None
    location = None
    weather = None

    multimedia = None

    wifi_p2p = None
    wifi = None

    bt_conn = None
    bt_scan = None

    environment_sensors = None
    motion_sensors = None
    position_sensors = None
    
    def __init__(self, time, label, audio_features, battery_features, activity_rec_data, bt_conn, bt_scans,
                 current_events, visible_cells, display_status, location_data, weather_info, wifi_p2p, wifi,
                 environment_data, motion_data, position_sensor_data, multimedia_data):

        min_millis = 60000

        self.audio = Example.get_nearest_example(time, audio_features, min_millis)
        self.battery = Example.get_nearest_example(time, battery_features, min_millis)
        self.activity_rec = Example.get_nearest_example(time, activity_rec_data, 5 * min_millis)
        # self.running_apps = self.get_nearest_example(minute, running_apps, 180000)
        self.bt_conn = Example.get_nearest_example(time, bt_conn, None)
        self.bt_scan = Example.get_nearest_example(time, bt_scans, min_millis)

        if self.bt_scan is None:
            self.bt_scan = []

        self.current_calendar_events = Example.get_nearest_example(time, current_events, 60 * 4 * min_millis)

        if self.current_calendar_events is None:
            self.current_calendar_events = 0

        self.multimedia = self.get_nearest_example(time, multimedia_data, 2 * min_millis)

        if ".png" in self.multimedia or ".jpg" in self.multimedia:
            self.multimedia = 1
        elif ".avi" in self.multimedia or ".mp4" in self.multimedia:
            self.multimedia = 2
        elif self.multimedia is None:
            self.multimedia = 0

        self.visible_cells = Example.get_nearest_example(time, visible_cells, min_millis)
        self.display = Example.get_nearest_example(time, display_status, None)
        self.location = Example.get_nearest_example(time, location_data, None)
        self.weather = Example.get_nearest_example(time, weather_info, None)
        self.wifi_p2p = Example.get_nearest_example(time, wifi_p2p, None)

        if self.wifi_p2p is None:
            self.wifi_p2p = []

        self.wifi = Example.get_nearest_example(time, wifi, None)

        if self.wifi is None:
            self.wifi = []

        self.environment_sensors = Example.get_nearest_example(time, environment_data, 3 * min_millis)
        self.motion_sensors = Example.get_nearest_example(time, motion_data, 3 * min_millis)
        self.position_sensors = Example.get_nearest_example(time, position_sensor_data, 3 * min_millis)
        self.get_time_info(time)
        self.label = label

    @staticmethod
    def get_nearest_example(time, data, max_diff):

        diffs = []

        for key in data.keys():
            diffs.append(abs(time - key))

        example = None

        if len(diffs) != 0:

            if max_diff is not None and min(diffs) <= max_diff:
                key = list(data.keys())[diffs.index(min(diffs))]
                example = data[key]

            elif max_diff is None:
                key = list(data.keys())[diffs.index(min(diffs))]
                example = data[key]

        return example

    def get_time_info(self, timestamp):

        dt = datetime.fromtimestamp(timestamp / 1000.0)

        # day_type  0 = working day     1 = weekend
        day_type = 0

        # time       0 = morning         1 = afternoon       2 = evening         3 = night
        time = 0

        if dt.weekday() >= 5:
            day_type = 1

        if 5 <= dt.hour <= 12:
            time = 0
        elif 13 <= dt.hour <= 16:
            time = 1
        elif 17 <= dt.hour <= 22:
            time = 2
        elif 23 <= dt.hour <= 4:
            time = 3

        self.time_info = (day_type, time)

    def is_valid(self):
        fields = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]

        for field in fields:
            if getattr(self, field) is None:
                return False

        return True
