import argparse
import os
import shutil
from tqdm import tqdm

from play_store import GooglePlayStore
import reader


def parse_arguments():

    parser = argparse.ArgumentParser(description='Creates the dataset for the ContextLabeler experiment.')

    parser.add_argument('-input', dest='inputDir', required=True,
                        help='Path of the directory which contains raw sensors data.')
    parser.add_argument('-output', dest='outputDir', required=True,
                        help='Path of the directory where data will be stored.')

    return parser.parse_args()


'''=====================================================================================================================
MAIN
====================================================================================================================='''

if __name__ == '__main__':

    args = parse_arguments()

    main_dir = args.inputDir
    output_dir = args.outputDir

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    users_dirs = [dI for dI in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, dI))]

    google = GooglePlayStore(output_dir, new_files=True)
    google.fetch_apps_categories()

    print("Reading both installed and running applications...")
    apps = reader.read_all_apps(main_dir, users_dirs)

    for package in tqdm(apps, desc="Downloading apps categories"):
        google.get_package_category(package)

    print("Data saved in " + google.cache_file + " and " + google.app_categories_file)