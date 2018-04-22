
def normalize_mac(mac):
    max_mac = mac_to_int("FF:FF:FF:FF:FF:FF")

    return mac_to_int(mac)/max_mac


def mac_to_int(mac):
    return int(mac.replace(':', ''), 16)


def int_to_mac(mac):
    ':'.join(format(s, '02x') for s in bytes.fromhex(str(mac)))


#TIME_HEADER = ["month", "week_of_month", "day_of_month", "day_of_week", "weekday", "time", "time_type"]
TIME_HEADER = ["weekday", "time", "time_type"]

AUDIO_HEADER = ["audio_ring_mode", "audio_alarm_volume", "audio_music_volume", "audio_notification_volume",
                "audio_ring_volume", "audio_bt_sco_on", "audio_mic_mute", "audio_music_active", "audio_speaker_on",
                "audio_headset_on"]

DISPLAY_HEADER = ["display_status", "display_rotation", "display_activation_counter"]

BATTERY_HEADER = ["battery_percentage", "battery_device_plugged"]

ACTIVITY_REC_HEADER = ["activity_rec_in_vehicle", "activity_rec_on_bicycle", "activity_rec_on_foot",
                       "activity_rec_running", "activity_rec_still", "activity_rec_tilting", "activity_rec_walking",
                       "activity_rec_unknown"]

RUNNING_APPS_HEADER = ["running_apps_art_and_design", "running_apps_auto_and_vehicles", "running_apps_beauty",
                       "running_apps_books_and_reference", "running_apps_business", "running_apps_comics",
                       "running_apps_communication", "running_apps_dating", "running_apps_education",
                       "running_apps_entertainment", "running_apps_events", "running_apps_finance",
                       "running_apps_food_and_drink", "running_apps_health_and_fitness", "running_apps_house_and_home",
                       "running_apps_libraries_and_demo", "running_apps_lifestyle", "running_apps_maps_and_navigation",
                       "running_apps_medical", "running_apps_music_and_audio", "running_apps_news_and_magazines",
                       "running_apps_parenting", "running_apps_personalization", "running_apps_photography",
                       "running_apps_productivity", "running_apps_shopping", "running_apps_social",
                       "running_apps_sports", "running_apps_tools", "running_apps_travel_and_local",
                       "running_apps_video_players_and_editor", "running_apps_wear_os", "running_apps_weather",
                       "running_apps_games_action", "running_apps_games_adventure", "running_apps_games_arcade",
                       "running_apps_games_board", "running_apps_games_card", "running_apps_games_casino",
                       "running_apps_games_causal", "running_apps_games_educational", "running_apps_games_music",
                       "running_apps_games_puzzle", "running_apps_games_racing", "running_apps_games_role_playing",
                       "running_apps_games_simulation", "running_apps_games_sports", "running_apps_games_strategy",
                       "running_apps_games_trivia", "running_apps_games_word", "running_apps_games_ages_5_and_under",
                       "running_apps_games_ages_6_8", "running_apps_games_ages_9_and_up",
                       "running_apps_games_action_and_adventure", "running_apps_games_brain_games",
                       "running_apps_family_creativity", "running_apps_family_education",
                       "running_apps_family_music_and_video", "running_apps_pretend_play"]

#RUNNING_APPS_HEADER = ["running_app"]

BT_CON_HEADER = ["bt_con_device_1_address", "bt_con_device_1_major_class", "bt_con_device_2_address",
                 "bt_con_device_2_major_class", "bt_con_device_3_address", "bt_con_device_3_major_class"]

BT_SCAN_HEADER = ["bt_scan_device_1_address", "bt_scan_device_1_major_class", "bt_scan_device_2_address",
                  "bt_scan_device_2_major_class", "bt_scan_device_3_address", "bt_scan_device_3_major_class",
                  "bt_scan_device_4_address", "bt_scan_device_4_major_class", "bt_scan_device_5_address",
                  "bt_scan_device_5_major_class"]

CALENDAR_HEADER = ["calendar_current_events"]

MULTIMEDIA_HEADER = ["multimedia"]

LOCATION_HEADER = ["location_lat", "location_lon", "location_bearing"]

WEATHER_HEADER = ["weather_code", "weather_temp", "weather_temp_min", "weather_temp_max", "weather_humidity",
                  "weather_pressure", "weather_wind_speed", "weather_wind_direction", "weather_cloudiness"]

WIFI_P2P_HEADER = ["wifi_p2p_device_1_address", "wifi_p2p_device_2_address", "wifi_p2p_device_3_address",
                   "wifi_p2p_device_4_address", "wifi_p2p_device_5_address"]

WIFI_HEADER = ["wifi_ap_1_bssid", "wifi_ap_1_signal_level", "wifi_ap_1_connected", "wifi_ap_1_configured",
               "wifi_ap_2_bssid", "wifi_ap_2_signal_level", "wifi_ap_2_connected", "wifi_ap_2_configured",
               "wifi_ap_3_bssid", "wifi_ap_3_signal_level", "wifi_ap_3_connected", "wifi_ap_3_configured",
               "wifi_ap_4_bssid", "wifi_ap_4_signal_level", "wifi_ap_4_connected", "wifi_ap_4_configured",
               "wifi_ap_5_bssid", "wifi_ap_5_signal_level", "wifi_ap_5_connected", "wifi_ap_5_configured"]

'''
ENVIRONMENT_SENSORS_HEADER = ["sensor_light_min", "sensor_light_max", "sensor_light_mean",
                              "sensor_light_quadratic_mean", "sensor_light_25_percentile", "sensor_light_50_percentile",
                              "sensor_light_75_percentile", "sensor_light_100_percentile"]


MOTION_SENSORS_HEADER = ["sensor_accelerometer_x_min", "sensor_accelerometer_x_max", "sensor_accelerometer_x_mean",
                         "sensor_accelerometer_x_quadratic_mean", "sensor_accelerometer_x_25_percentile",
                         "sensor_accelerometer_x_50_percentile", "sensor_accelerometer_x_75_percentile",
                         "sensor_accelerometer_x_100_percentile",
                         "sensor_accelerometer_y_min", "sensor_accelerometer_y_max", "sensor_accelerometer_y_mean",
                         "sensor_accelerometer_y_quadratic_mean", "sensor_accelerometer_y_25_percentile",
                         "sensor_accelerometer_y_50_percentile", "sensor_accelerometer_y_75_percentile",
                         "sensor_accelerometer_y_100_percentile",
                         "sensor_accelerometer_z_min", "sensor_accelerometer_z_max", "sensor_accelerometer_z_mean",
                         "sensor_accelerometer_z_quadratic_mean", "sensor_accelerometer_z_25_percentile",
                         "sensor_accelerometer_z_50_percentile", "sensor_accelerometer_z_75_percentile",
                         "sensor_accelerometer_z_100_percentile",
                         "sensor_gravity_x_min", "sensor_gravity_x_max", "sensor_gravity_x_mean",
                         "sensor_gravity_x_quadratic_mean", "sensor_gravity_x_25_percentile",
                         "sensor_gravity_x_50_percentile", "sensor_gravity_x_75_percentile",
                         "sensor_gravity_x_100_percentile",
                         "sensor_gravity_y_min", "sensor_gravity_y_max", "sensor_gravity_y_mean",
                         "sensor_gravity_y_quadratic_mean", "sensor_gravity_y_25_percentile",
                         "sensor_gravity_y_50_percentile", "sensor_gravity_y_75_percentile",
                         "sensor_gravity_y_100_percentile",
                         "sensor_gravity_z_min", "sensor_gravity_z_max", "sensor_gravity_z_mean",
                         "sensor_gravity_z_quadratic_mean", "sensor_gravity_z_25_percentile",
                         "sensor_gravity_z_50_percentile", "sensor_gravity_z_75_percentile",
                         "sensor_gravity_z_100_percentile",
                         "sensor_gyroscope_x_min", "sensor_gyroscope_x_max", "sensor_gyroscope_x_mean",
                         "sensor_gyroscope_x_quadratic_mean", "sensor_gyroscope_x_25_percentile",
                         "sensor_gyroscope_x_50_percentile", "sensor_gyroscope_x_75_percentile",
                         "sensor_gyroscope_x_100_percentile",
                         "sensor_gyroscope_y_min", "sensor_gyroscope_y_max", "sensor_gyroscope_y_mean",
                         "sensor_gyroscope_y_quadratic_mean", "sensor_gyroscope_y_25_percentile",
                         "sensor_gyroscope_y_50_percentile", "sensor_gyroscope_y_75_percentile",
                         "sensor_gyroscope_y_100_percentile",
                         "sensor_gyroscope_z_min", "sensor_gyroscope_z_max", "sensor_gyroscope_z_mean",
                         "sensor_gyroscope_z_quadratic_mean", "sensor_gyroscope_z_25_percentile",
                         "sensor_gyroscope_z_50_percentile", "sensor_gyroscope_z_75_percentile",
                         "sensor_gyroscope_z_100_percentile",
                         "sensor_linear_acc_x_min", "sensor_linear_acc_x_max", "sensor_linear_acc_x_mean",
                         "sensor_linear_acc_x_quadratic_mean", "sensor_linear_acc_x_25_percentile",
                         "sensor_linear_acc_x_50_percentile", "sensor_linear_acc_x_75_percentile",
                         "sensor_linear_acc_x_100_percentile",
                         "sensor_linear_acc_y_min", "sensor_linear_acc_y_max", "sensor_linear_acc_y_mean",
                         "sensor_linear_acc_y_quadratic_mean", "sensor_linear_acc_y_25_percentile",
                         "sensor_linear_acc_y_50_percentile", "sensor_linear_acc_y_75_percentile",
                         "sensor_linear_acc_y_100_percentile",
                         "sensor_linear_acc_z_min", "sensor_linear_acc_z_max", "sensor_linear_acc_z_mean",
                         "sensor_linear_acc_z_quadratic_mean", "sensor_linear_acc_z_25_percentile",
                         "sensor_linear_acc_z_50_percentile", "sensor_linear_acc_z_75_percentile",
                         "sensor_linear_acc_z_100_percentile",
                         "sensor_rotation_vec_x_min", "sensor_rotation_vec_x_max", "sensor_rotation_vec_x_mean",
                         "sensor_rotation_vec_x_quadratic_mean", "sensor_rotation_vec_x_25_percentile",
                         "sensor_rotation_vec_x_50_percentile", "sensor_rotation_vec_x_75_percentile",
                         "sensor_rotation_vec_x_100_percentile",
                         "sensor_rotation_vec_y_min", "sensor_rotation_vec_y_max", "sensor_rotation_vec_y_mean",
                         "sensor_rotation_vec_y_quadratic_mean", "sensor_rotation_vec_y_25_percentile",
                         "sensor_rotation_vec_y_50_percentile", "sensor_rotation_vec_y_75_percentile",
                         "sensor_rotation_vec_y_100_percentile",
                         "sensor_rotation_vec_z_min", "sensor_rotation_vec_z_max", "sensor_rotation_vec_z_mean",
                         "sensor_rotation_vec_z_quadratic_mean", "sensor_rotation_vec_z_25_percentile",
                         "sensor_rotation_vec_z_50_percentile", "sensor_rotation_vec_z_75_percentile",
                         "sensor_rotation_vec_z_100_percentile"]

POSITION_SENSORS_HEADER = ["sensor_proximity_min", "sensor_proximity_max", "sensor_proximity_mean",
                           "sensor_proximity_quadratic_mean", "sensor_proximity_25_percentile",
                           "sensor_proximity_50_percentile", "sensor_proximity_75_percentile",
                           "sensor_proximity_100_percentile"]
'''

def get_dataset_header(google):

    header = TIME_HEADER + AUDIO_HEADER + DISPLAY_HEADER + BATTERY_HEADER + ACTIVITY_REC_HEADER \
             + google.store_categories + BT_CON_HEADER + BT_SCAN_HEADER + CALENDAR_HEADER + MULTIMEDIA_HEADER \
             + LOCATION_HEADER + WEATHER_HEADER + WIFI_P2P_HEADER + WIFI_HEADER
             #+ ENVIRONMENT_SENSORS_HEADER + MOTION_SENSORS_HEADER + POSITION_SENSORS_HEADER

    return ','.join(header)

