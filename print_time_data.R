

min_time = 1520515827838
max_time = 1520583336015

files = list.files(path="../data/test2/times/", pattern="*.csv", full.names=T, recursive=FALSE)
activities = read.table("../data/test2/activities.csv", header = F)
colnames(activities) = c("start", "end", "label")

i=1
p = ggplot()

for(file in files){
  data = read.table(file, header = F)
  colnames(data) = c("time")
  q = paste("SELECT data.time,",toString(i))
  q = paste(q, "as value FROM data, activities WHERE data.time >= activities.start AND data.time <= activities.end")
  
  df = sqldf(q)
  
  p = p + geom_point(data = df, aes(x = time, y = value), shape=16, size=3)
  i = i+1
}

p

#lapply(files, function(x) {
#  data = read.table(x, header = F)
#  colnames(data) = c("time")
  
#  q1 = "SELECT data.time, "
#  q2 = toString(i)
#  q = paste("SELECT data.time,",toString(i))
#  q = paste(q, "as value, activities.label FROM data, activities WHERE data.time >= activities.start AND data.time <= activities.end")
  
#  data = sqldf(q)
  
#  i <<- i + 1

#  ggplot(data) + geom_point(aes(x = time, y = value, colour=label), shape=16, size=3) + 
#    theme(axis.ticks.y = element_blank(),
#          axis.text.y = element_blank(),
#          axis.title.y = element_blank(),
#          plot.title = element_text(margin = margin(t = 10, b = -20)))
    #ggtitle(basename(x))
    
  #ggsave(gsub(".csv", ".jpg", basename(x)), plot = last_plot(), device = "jpeg", dpi = 300, path = "../data/test2/figures/")