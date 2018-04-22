#!/usr/bin/env Rscript

# args[1] = input data (non-normalized sensors data)
# args[2] = output file with normalized sensors data

suppressMessages(library(dplyr))
suppressMessages(library(purrr))
suppressMessages(library(purrrlyr))

rescale_func <- function(df, sensor){
  
  col_names_to_rescale = c(paste(sensor, "_min", sep=""), paste(sensor, "_max", sep=""), paste(sensor, "_mean", sep=""), paste(sensor, "_quadratic_mean", sep=""), paste(sensor, "_25_percentile", sep=""), paste(sensor, "_50_percentile", sep=""), paste(sensor, "_75_percentile", sep=""), paste(sensor, "_100_percentile", sep=""))
  
  data_selected <-
    df %>%
    select(col_names_to_rescale) %>%
    dmap(function(x){(x-min(.[,1]))/(max(.[,2])-min(.[,1]))})
  
  return(list(data_selected, col_names_to_rescale))
}

args = commandArgs(trailingOnly=TRUE)

data = read.table(args[1], header = T, sep = ",")

sensors = c("sensor_light", "sensor_accelerometer_x", "sensor_accelerometer_y", "sensor_accelerometer_z", "sensor_gravity_x", "sensor_gravity_y", "sensor_gravity_z", "sensor_gyroscope_x", "sensor_gyroscope_y", "sensor_gyroscope_z", "sensor_linear_acc_x", "sensor_linear_acc_y", "sensor_linear_acc_z", "sensor_rotation_vec_x", "sensor_rotation_vec_y", "sensor_rotation_vec_z", "sensor_proximity")

for(sensor in sensors){
  out <- rescale_func(data, sensor)
  rescaled_data <- out[[1]]
  columns <- out[[2]]
  data[, columns] <- rescaled_data[, columns]
}

write.table(data, file = args[2], sep=",", quote = FALSE)
