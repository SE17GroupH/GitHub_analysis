data<-read.csv("group1_commit_data.csv")
counts<-data.frame(data$week, data$user1, data$user2, data$user3)
rownames(counts)<-counts[,1]
counts[,1]<-NULL
final_counts<-t(counts)
barplot(as.matrix(final_counts), col=c("darkblue", "red", "yellow"), legend=c("user1", "user2", "user3"))