import argparse


import os

from model import Example
import reader


def parse_arguments():

    parser = argparse.ArgumentParser(description='Creates the dataset for the ContextLabeler experiment.')

    parser.add_argument('-in', dest='inputDir', required=True,
                        help='Path of the directory which contains raw sensors data.')

    parser.add_argument('-out', dest='outputDir', required=True,
                        help='The path of the directory that will be used to store the dataset.')

    return parser.parse_args()


'''=====================================================================================================================
MAIN
====================================================================================================================='''

if __name__ == '__main__':

    args = parse_arguments()

    main_dir = args.inputDir
    users_dirs = [dI for dI in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, dI))]

    #reading_apps(google, main_dir, users_dirs)

    for user in users_dirs:

        user_dir = main_dir + "/" + user

        activities = reader.read_activities(user_dir)

        audio_features, battery_features, activity_rec_data, bt_conn, bt_scans, current_events, visible_cells,\
            display_status, location_data, weather_info, wifi_p2p, wifi, environment_data, motion_data,\
            position_sensor_data, multimedia_data = reader.load_data(user_dir)

        for activity in activities:
            start = activity[0]
            end = activity[1]
            label = activity[2]

            print("Activity: "+label)

            # remove the 10% of the data at the beginning and end
            span = 0.1
            start = int(start + ((end - start) * span))
            end = int(end - ((end - start) * span))

            time = start

            not_valid = 0

            min_millis = 60000

            examples = []

            while time <= end:

                example = Example(time, label, audio_features, battery_features, activity_rec_data, bt_conn, bt_scans,
                                  current_events, visible_cells, display_status, location_data, weather_info, wifi_p2p,
                                  wifi, environment_data, motion_data, position_sensor_data, multimedia_data)

                if example.is_valid():
                    examples.append(examples)

                time = time + min_millis

            print(label + ": " + str(len(examples)) + " - " + str((activity[1]-activity[0])/(1000*60)) + "min")