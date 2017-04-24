data<-read.csv('group1_commit_data.csv')
commit<-data$commits
scale(commit, center = TRUE, scale = TRUE)
zscore<-(commit-mean(commit)/sd(commit))
plot(week,zscore, type="o", col="blue")
axis(side=1, at=c(1:16))