# processing counts
data<-read.csv("comments1.csv")
dates<-data$created_convert
a<-table(dates)
write.table(a, file="comments_count_team1.csv", sep=",")

