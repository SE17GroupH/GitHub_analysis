data<-read.csv('group1_commit_data.csv')
commit<-data$commits
norm_commit<-rnorm(commit, mean =0, sd=1)
scale(commit, center = TRUE, scale = TRUE)
zscore<-(commit-mean(commit)/sd(commit))
zscore_norm<-(norm_commit-mean(norm_commit)/sd(norm_commit))
plot(week, zscore_norm, type="o", col="blue")
axis(side=1, at=c(1:16))

plot(week,zscore, type="o", col="blue")
axis(side=1, at=c(1:16))