class Example:

    time = None

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

    wifi_p2p = None
    wifi = None

    bt_conn = None
    bt_scan = None

    environment_sensors = None
    motion_sensors = None
    position_sensors = None


    def is_valid(self):
        fields = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]

        for field in fields:
            if getattr(self, field) is None:
                return False

        return True