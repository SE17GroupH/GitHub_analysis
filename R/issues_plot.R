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
subset<-data[which(data$pull_request=="No"),]
duration<-subset$duration
less24<-sum(duration<=24)
more24<-sum(duration>24)
duration_table<-matrix(c(less24, more24), ncol=2, byrow=TRUE)
colnames(duration_table)<-c("less than 24hrs", "more than 24hrs")
rownames(duration_table)<-c("counts")
duration_table<-as.table(duration_table)
mp<-barplot(duration_table, main="Issue open time")
text(mp, c(less24, more24), labels = c(less24, more24), pos = 1, col="white")

## for group 3
remove<-c("None")
remove_none<-setdiff(duration, remove)
less24<-sum(remove_none<=24)
more24<-sum(remove_none>24)


# Comments
comments<-data$comments
comment0<-sum(comments == 0)
comments5<-sum(comments>0 & comments<=5)
comments10<-sum(comments>5 & comments<=10)
comments15<-sum(comments>10 & comments<=15)
comments20<-sum(comments>15 & comments<=20)
comments20plus<-sum(comments>20)
comments_table<-matrix(c(comment0, comments5, comments10, comments15, comments20, comments20plus), ncol=6, byrow=TRUE)
colnames(comments_table)<-c("0", "1-5", "6-10", "11-15", "16-20", "20+")
rownames(comments_table)<-c("counts")
comments_table<-as.table(comments_table)
mp<-barplot(comments_table, main="Comments count", xlab="Number of comments per issue")
text(mp, c(comment0, comments5, comments10, comments15, comments20, comments20plus), labels = c(comment0, comments5, comments10, comments15, comments20, comments20plus), pos = 1, col="white")

# pie charts for issues with bug label vs nonbug label
buglabel<-data$bug
bugtrue<-sum(buglabel=="True")
bugfalse<-sum(buglabel=="False")
slices <- c(bugtrue, bugfalse) 
lbls <- c("bug label", "non bug labels")
pct <- round(slices/sum(slices)*100)
lbls <- paste(lbls, pct) # add percents to labels 
lbls <- paste(lbls,"%",sep="") # ad % to labels 
pie(slices,labels = lbls, col=rainbow(length(lbls)), main="Bug label vs non bug labels")

#pie charts for issues creators
data<-read.csv("Group0_issues.csv")
created_by<-data$created_by
user1<-sum(created_by=="user1")
user2<-sum(created_by=="user2")
user3<-sum(created_by=="user3")
user4<-sum(created_by=="user4")
slices <- c(user1, user2, user3, user4)
lbls <- c("user1", "user2", "user3", "user4")
pct <- round(slices/sum(slices)*100)
lbls <- paste(lbls, pct) # add percents to labels 
lbls <- paste(lbls,"%",sep="") # ad % to labels 
pie(slices,labels = lbls, col=rainbow(length(lbls)), main="Percentage of issues created per member")


#pie chart for assignee
assignee<-data$assignee
user1<-length(grep("user1", assignee))
user2<-length(grep("user2", assignee))
user3<-length(grep("user3", assignee))
slices <- c(user1, user2, user3)
lbls <- c("user1", "user2", "user3")
pct <- round(slices/sum(slices)*100)
lbls <- paste(lbls, pct) # add percents to labels 
lbls <- paste(lbls,"%",sep="") # ad % to labels 
pie(slices,labels = lbls, col=rainbow(length(lbls)), main="Percentage of issues assigned per member")


#issues with milestone vs without
milestone<-data$milestone
without_milestone<-sum(milestone=="None")
with_milestone<-length(milestone)-without_milestone
slices <- c(with_milestone, without_milestone)
lbls <- c("assigned milestone", "without milestone")
pct <- round(slices/sum(slices)*100)
lbls <- paste(lbls, pct) # add percents to labels 
lbls <- paste(lbls,"%",sep="") # ad % to labels 
pie(slices,labels = lbls, col=rainbow(length(lbls)), main="Issues assigned with milestone vs Issues without milestone")