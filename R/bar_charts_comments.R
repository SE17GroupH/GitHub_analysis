data<-read.csv("comments_count_team1.csv")
counts<-data$counts
date<-data$date
barplot(counts, main="Comments Count for Team1", names.arg=date)