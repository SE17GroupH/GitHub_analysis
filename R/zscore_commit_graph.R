require(ggplot2)
data<-read.csv('group1_commit_data.csv')
commit<-data$commits
week<-data$week
norm_commit<-rnorm(commit, mean = mean(commit), sd=1)
scale(commit, center = TRUE, scale = TRUE)
zscore<-(commit-mean(commit)/sd(commit))

zscore_norm<-(norm_commit-mean(norm_commit)/sd(norm_commit))
# plot(week, zscore, type="o", col="blue")
# plot(week, zscore_norm, type="o", col="blue")
df<-data.frame(gp=week, y=zscore_norm)
p<-ggplot(df, aes(gp, y, group=1))+geom_point()+geom_line()
p+geom_hline(yintercept=-0.5, col="red")


# scatter.smooth(x=1:length(data$week), y=zscore_norm)
# axis(side=1, at=c(1:16))


# Finding intersection with threshold

# abline(h=-0.5, type="o", col="red", lty = 2)
#lines(h=-0.5, type="o", col="red", lty = 2)
# x1<-zscore_norm
# threshold <- -0.5
# x2<-threshold
# # Find points where x1 is above x2.
# above<-x1>x2
# # Points always intersect when above=TRUE, then FALSE or reverse
# intersect.points<-which(diff(above)!=0)
# # Find the slopes for each line segment.
# x1.slopes<-x1[intersect.points+1]-x1[intersect.points]
# x2.slopes<-x2[intersect.points+1]-x2[intersect.points]
# # Find the intersection for each segment.
# x.points<-intersect.points + ((x2[intersect.points] - x1[intersect.points]) / (x1.slopes-x2.slopes))
# y.points<-x1[intersect.points] + (x1.slopes*(x.points-intersect.points))
# # Plot.
# plot(x1,type='l')
# lines(x2,type='l',col='red')
# points(x.points,y.points,col='blue')

#mark points
