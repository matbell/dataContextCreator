seqlast <- function (from, to, by) {
  vec <- do.call(what = seq, args = list(from, to, by))
  if ( tail(vec, 1) != to ) {
    return(c(vec, to))
  } else {
    return(vec)
  }
}

# set output's digit format 
options(digits = 22)

# read inputs
activities = read.table("data/test/activities.csv")

activity = read.table("data/test/activity.csv", header = T)
audio = read.table("data/test/audio.csv", header = T)
battery = read.table("data/test/battery.csv", header = T)
display = read.table("data/test/display.csv", header = T)

# For each Activity
for(i in 1:nrow(activities)) {
  activity_row <- activities[i,]
  
  start = round(activity_row$V1 + (activity_row$V2 - activity_row$V1) * 0.1, 0)
  end = round(activity_row$V2 - (activity_row$V2 - activity_row$V1) * 0.1, 0)
  label = activity_row$V3
  
  for(date in seqlast(start, end, by=60000)){
    
    audio_row = audio[which.min(abs(date-audio$time)),]
    battery_row = battery[which.min(abs(date-battery$time)),]
    
    #mapply(c, activity_row, audio_row, SIMPLIFY=FALSE)
    print(data)
    
    battery_row = battery[which.min(abs(date-battery$V1)),]
    display_row = activity[which.min(abs(date-display$V1)),]
  }
}