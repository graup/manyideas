library(rga)
rga.open(instance="ga", where="ga.dat")
ids = c('171975010')  # only users
ids = c('171995485')  # all visitors
start.date = '2018-04-05'
end.date = '2018-04-14'
daily <- ga$getData(ids, start.date, end.date, 
                    metrics = "ga:users,ga:newUsers,ga:sessions", dimensions = "ga:date", 
                    sort = "", filters = "", segment = "",
                    start = 1, max = 1000)
daily$date <- as.Date(daily$date, "%Y-%m-%d")

stats = read.csv("stats_2018-05-25T06-43.csv", header=T) #stats_2018-04-12T06-43
stats$date <- as.Date(stats$date, "%Y-%m-%d")
stats = stats[4:nrow(stats),]
stats = stats[stats$date <= '2018-04-14',]




### Setup plot
dev.off()
RESO <- 300  # Resolution
PS <- 19  # Pointsize
LO <- matrix(c(1,1,1), nrow=3, ncol=1)
WIDTHS <- c(12) #widths of each figure in layout (i.e. column widths) in inch
HEIGHTS <- c(2,2,3)  #heights of each figure in layout (i.e. row heights) in inch
OMA <- c(0,0,0,0)  #Outer margins c(bottom, left, top, right)
HEIGHT <- sum(HEIGHTS) + OMA[1]*PS*1/72 + OMA[3]*PS*1/72
WIDTH <- sum(WIDTHS) + OMA[2]*PS*1/72 + OMA[4]*PS*1/72
png(paste("/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/deployment/user-stats.png", sep=""), width=WIDTH, height=HEIGHT, units="in", res=RESO)
par(oma=OMA, ps=PS) #settings before layout
layout(LO, heights=HEIGHTS, widths=WIDTHS)
par(cex=1)



par(mfrow=c(3,1))

par(mar=c(1,5,0,3), omi=c(0.2,0.2,0.5,0.2))
plot(users ~ date, data=daily, xaxt = "n", type = "l", ylab='Visitors', xlab='', ylim=c(0, max(daily$users)))
grid(NA, NULL)
abline(v = stats$date,  lty = "dotted", col = "lightgray")


#ga$getData(ids, start.date, end.date, 
#           metrics = "ga:totalEvents", dimensions = "ga:eventCategory,ga:eventAction,ga:eventLabel", 
#           sort = "", filters = "", segment = "",
#           start = 1, max = 1000)


par(mar=c(1,5,0,3))
plot(signups ~ date, data=stats, xaxt = "n", type = "l", ylab='Signups', xlab='', ylim=c(0, max(stats$signups)))
grid(NA, NULL)
abline(v = stats$date,  lty = "dotted", col = "lightgray")


par(mar=c(3,5,0,3))
plot(issue_count ~ date, data=stats, xaxt = "n", type = "l", ylab='Ideas', xlab='', ylim=c(0, max(stats$issue_count)))
axis(side=1, at=stats$date, labels=format(stats$date, "%Y-%m-%d\n%a"), padj = 0.5)
grid(NA, NULL)
abline(v = stats$date,  lty = "dotted", col = "lightgray")





