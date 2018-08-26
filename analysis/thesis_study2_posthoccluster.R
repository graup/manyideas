setwd('/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/deployment')
percent <- function(x, digits = 2, format = "f", ...) paste0(formatC(100 * x, format = format, digits = digits, ...), "%")

gcos_scales = c('autonomy', 'control', 'impersonal')
gcos_scales_norm = c('autonomy.norm', 'control.norm', 'impersonal.norm')
mvs_scales = c('intrinsic', 'integrated', 'identified', 'introjected', 'external', 'amotivation')
mvs_scales_norm = c('intrinsic.norm', 'integrated.norm', 'identified.norm', 'introjected.norm', 'external.norm', 'amotivation.norm')
test_scales = c(gcos_scales, mvs_scales)
test_scales_norm = c(gcos_scales_norm, mvs_scales_norm)

data = read.csv("data_2018-04-15T13-31.csv", header=T)
# remove all without treatment
data = data[data$treatment!='',]
# remove non-participants
non_participants =  c("wodn9955", "admin", 'mcpanic', 'Paula', 'hellohello', 'Sy', 'hyungyu.sh', "contoso", "watcher", "khw", "\354\234\240\354\204\261\352\265\254\353\257\274")
data = data[!(data$username %in% non_participants),]

data_email = read.csv("id-email.csv", header=T, sep=';')
data = merge(data, data_email, by='id', all.x = TRUE)

data_ga = read.csv("ga-users.csv", header=T)
data = merge(data, data_ga, by='id', all.x = TRUE)

data_survey = read.csv("survey.csv", header=T, sep=';')
data = merge(data, data_survey, by='email', all = TRUE)

# Force factors
factor_cols = c('id', 'username', 'group', 'treatment', 'occupation', 'sex', 'age')
data[factor_cols] <- lapply(data[factor_cols], factor)

# Reorder some factors
data$age = factor(data$age, levels(data$age)[c(2:4, 1)])
data$occupation = factor(data$occupation, levels(data$occupation)[c(5,2,1,4,3)])

data$any_interaction = data$like_count > 0 | data$issue_count > 0 | data$comment_count > 0


# Remove useless variables
data[,c("flag_count")] <- list(NULL)

# normalized test scales
d <- data[!is.na(data$intrinsic),]
data[,test_scales_norm] <- NA
data[!is.na(data$intrinsic), test_scales_norm] = apply(d[,test_scales], 2, function(col) {
  (col - min(col))/(max(col)-min(col))
})
#apply(d[,test_scales], 2, min))/apply(d[,test_scales], 2, max) #- apply(d[, test_scales]-min(d[,test_scales]), 2, median)/84
#data[!is.na(data$intrinsic), mvs_scales_norm] = (d[,mvs_scales]-4)/20 - apply(d[, mvs_scales]-4, 2, median)/20

data$avg_issue_length = as.integer(data$avg_issue_length)
data$session_duration.log = log(data$session_duration)
data$avg_session_duration = data$session_duration/data$session_count
data$avg_session_duration[is.nan(data$avg_session_duration)] <- NA
data$has_returned = data$session_count > 1

print(nrow(data))
nrow(data[data$like_received_count>0,])
nrow(data[!is.na(data$intrinsic),])

# split of survey respondents
xtabs(~group+treatment, data[!is.na(data$autonomy),])
xtabs(~treatment, data[!is.na(data$autonomy),])
nrow(data[!is.na(data$autonomy),])

#par(mfrow=c(1,2), oma=c(0,0,2,0))

# kmeans for survey personality tests
library(cluster) 
d = data[!is.na(data$intrinsic), c(test_scales_norm)]
#s <- as.integer(runif(1)*1000) print(s)
set.seed(2018041627 + 659)
fit <- kmeans(d, 2, iter.max=100)
ord <- rev(order(abs(fit$centers[1,]-fit$centers[2,])))
cluster_means <- fit$centers[,ord]  # cluster means, ordered by highest variance
cluster_means
length(cluster_means[,cluster_means[1,] > cluster_means[2,]])
print("Cluster 1")
colnames(cluster_means[,cluster_means[1,] > cluster_means[2,]])  # amotivation, impoersonal, external, control
print("Cluster 2")
colnames(cluster_means[,cluster_means[1,] < cluster_means[2,]])  # identified, intrinsic, autonomy, integrated
#clusplot(d, fit$cluster, color=TRUE, labels=2, lines=0, main="Cluster based on GCOS/MVS scores")
data$group_survey = NA
data$group_survey[as.integer(names(fit$cluster))] = fit$cluster
data$group_survey = as.factor(data$group_survey)
control_cluster_no = which.max(cluster_means[,'amotivation.norm'])
d$cluster = as.factor(fit$cluster)
levels(data$group_survey) = c('control', 'autonomy')[c(control_cluster_no, 3-control_cluster_no)]  #theorized cluster meanings
summary(data$group_survey)




### Setup plot
dev.off()
RESO <- 300  # Resolution
PS <- 19  # Pointsize
LO <- matrix(c(1), nrow=3, ncol=1)
WIDTHS <- c(12) #widths of each figure in layout (i.e. column widths) in inch
HEIGHTS <- c(8)  #heights of each figure in layout (i.e. row heights) in inch
OMA <- c(0,0,0,0)  #Outer margins c(bottom, left, top, right)
HEIGHT <- sum(HEIGHTS) + OMA[1]*PS*1/72 + OMA[3]*PS*1/72
WIDTH <- sum(WIDTHS) + OMA[2]*PS*1/72 + OMA[4]*PS*1/72
png(paste("/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/deployment/cluster.png", sep=""), width=WIDTH, height=HEIGHT, units="in", res=RESO)
par(oma=OMA, ps=PS) #settings before layout
layout(LO, heights=HEIGHTS, widths=WIDTHS)
par(cex=1)


par(mar=c(6,5,0,3), omi=c(0.2,0.2,0.5,0.2))


# try only MVS
s <- as.integer(runif(1)*1000)
print(s)
set.seed(2018041627 + 735)
d = data[!is.na(data$intrinsic), c(mvs_scales_norm)]
fit_mvs <- kmeans(d, 2, iter.max=100)
#fit_mvs$cluster <- 3 - fit_mvs$cluster
# check if clustering separates scales
cluster_means <- fit_mvs$centers
ncol(cluster_means[,cluster_means[1,] > cluster_means[2,]])
ncol(cluster_means[,cluster_means[2,] > cluster_means[1,]])
library(caret)
confusionMatrix(fit$cluster, fit_mvs$cluster)
clusplot(d, fit_mvs$cluster, color=TRUE, labels=2, lines=0, main="")

ord <- rev(order(abs(fit$centers[1,]-fit$centers[2,])))
print("Cluster 1")
colnames(cluster_means[,cluster_means[1,] > cluster_means[2,]])  # amotivation, impoersonal, external, control
print("Cluster 2")
colnames(cluster_means[,cluster_means[1,] < cluster_means[2,]])  # identified, intrinsic, autonomy, integrated

# de-norm (col - min(col))/(max(col)-min(col))
d <- data[!is.na(data$intrinsic),]
norm_max = apply(d[,mvs_scales], 2, max)
norm_min = apply(d[,mvs_scales], 2, min)
denormed = ((cluster_means)*(norm_max-norm_min)+norm_min)/4
denormed


poisson.test(data[data$treatment == "autonomy",]$event_count,
       data[data$treatment == "autonomy" & data$group_survey == "autonomy",]$event_count)

t.test(data[data$treatment == "control",]$event_count,
       data[data$treatment == "control" & data$group_survey == "control",]$event_count)
