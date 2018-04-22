#!/bin/bash

if [ "$#" -ne "4" ]; then
	echo "Usage: gen_data.sh INPUT_DIR OUT_DATA_FILE OUT_LABEL_FILE NORMALIZE"
	exit 1
fi

./datasetcreator.py -in $1 -out ../output -google ../google_cache -norm $4

if [ "$4" -eq "1" ]; then
	echo "Normalizing raw sensors data"
	./normalize_sensors_data.R ../output/data $2
fi

mv ../output/label $3
