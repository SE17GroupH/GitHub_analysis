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