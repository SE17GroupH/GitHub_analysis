data<-read.csv("comments_count_team1.csv")
counts<-data$counts
date<-data$date
barplot(counts, main="Comments Count for Team1", names.arg=date)



# Stacked Bar Plot with Colors and Legend
data<-read.csv("commits_count_team1.csv")
counts <- table(data$commits, data$pr)
date<-data$date
barplot(counts, main="Comments and Pull Requests",
  names.arg=date, col=c("darkblue","red"))