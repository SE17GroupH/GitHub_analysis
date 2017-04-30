data<-read.csv("SE17GroupH_Zap_issues.csv")
#assignee combination
assignee<-data$assignee
counts<-table(assignee)
ordered_counts<-sort(counts)
barplot(ordered_counts, main="Issues assigned to team members", names.arg="")
text(x=midpts, y=-2, names(ordered_counts), cex=0.8, srt=45, xpd=TRUE)

#issues created by
created_by<-data$created_by
counts<-table(created_by)
ordered_counts<-sort(counts)
barplot(ordered_counts, main="Issues created by team members")

#issue open by week
data<-read.csv("Group0_issues.csv")
created_at<-data$created_at
open_dates<-strftime(created_at, format="%W")
open_counts<-table(open_dates)
barplot(open_counts, main="Issues opened", xlab="week")


#issue closed by week
closed_at<-data$closed_at
closed_dates<-strftime(closed_at, format="%W")
closed_counts<-table(closed_dates)
barplot(closed_counts, main="Issues closed", xlab="week")

#issues duration
duration<-data$duration
less24<-sum(duration<=24)
more24<-sum(duration>24)
duration_table<-matrix(c(less24, more24), ncol=2, byrow=TRUE)
colnames(duration_table)<-c("less than 24hrs", "more than 24hrs")
rownames(duration_table)<-c("counts")
duration_table<-as.table(duration_table)
mp<-barplot(duration_table, main="Issue open time")
text(mp, c(less24, more24), labels = c(less24, more24), pos = 1, col="white")