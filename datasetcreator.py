#!venv/bin/python

import argparse
import os
import shutil

from tqdm import tqdm

from model import Example
import reader
from play_store import GooglePlayStore
from utils import get_dataset_header


def parse_arguments():

    parser = argparse.ArgumentParser(description='Creates the dataset for the ContextLabeler experiment.')

    parser.add_argument('-in', dest='inputDir', required=True,
                        help='Path of the directory which contains raw sensors data.')

    parser.add_argument('-out', dest='outputDir', required=True,
                        help='The path of the directory that will be used to store the dataset.')

    parser.add_argument('-google', dest='googleDir', required=True,
                        help='Path of the directory which contains the Google Store application categories.')

    parser.add_argument('-norm', dest='normalize_data', required=True,
                        help='Normalize data or not (0/1)')

    return parser.parse_args()


def print_data_to_file(outDir, examples, google):

    data_file = outDir + "/" + "data"
    labels_file = outDir + "/" + "labels"

    if not os.path.exists(data_file):
        with open(data_file, 'w') as data:
            header = get_dataset_header(google)
            data.write(header + "\n")

    with open(data_file, 'a+') as data, open(labels_file, 'a+') as labels:
        for example in examples:
            data.write(','.join(str(x) for x in example.get_features_vector()) + "\n")
            labels.write(example.label + "\n")


'''=====================================================================================================================
MAIN
====================================================================================================================='''

if __name__ == '__main__':

    args = parse_arguments()

    main_dir = args.inputDir
    output_dir = args.outputDir
    google_dir = args.googleDir

    normalize = False
    if args.normalize_data == "1":
        normalize = True

    if not os.path.isdir(output_dir):
        #shutil.rmtree(output_dir, ignore_errors=True)
        os.makedirs(output_dir)

    users_dirs = [dI for dI in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, dI))]

    google = GooglePlayStore(google_dir)

    user_dir = args.inputDir

    activities = reader.read_activities(user_dir)

    audio_features, battery_features, activity_rec_data, bt_conn, bt_scans, current_events, visible_cells,\
        display_status, location_data, weather_info, wifi_p2p, wifi, environment_data, motion_data,\
        position_sensor_data, multimedia_data, running_apps = reader.load_data(user_dir, google, normalize)

    total_examples = 0

    for activity in tqdm(activities, desc="Activities for user " + user_dir):
        start = activity[0]
        end = activity[1]
        label = activity[2]

        # remove the 10% of the data at the beginning and end
        span = 0.1
        start = start + int((end-start) * span)
        end = end - int((end-start) * span)

        time = start

        min_millis = 60000

        examples = []

        while time <= end:

            example = Example(time, label, audio_features, battery_features, activity_rec_data, bt_conn, bt_scans,
                              current_events, visible_cells, display_status, location_data, weather_info, wifi_p2p,
                              wifi, environment_data, motion_data, position_sensor_data, multimedia_data,
                              running_apps, normalize)

            if example.is_valid():
                examples.append(example)

            time = time + min_millis

        print_data_to_file(output_dir, examples, google)

        total_examples = total_examples + len(examples)

    print("Total examples: "+str(total_examples))

        #print(label + ": " + str(len(examples)) + " - " + str((activity[1]-activity[0])/(1000*60)) + "min")