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


# kmeans for survey personality tests
library(cluster) 
# post-hoc clustering with MVS sscales
#s <- as.integer(runif(1)*1000)
#print(s)
set.seed(2018041627 + 735)
d = data[!is.na(data$intrinsic), c(mvs_scales_norm)]
fit_mvs <- kmeans(d, 2, iter.max=100)
# check if clustering separates scales. both should have more than 0 high means
cluster_means <- fit_mvs$centers
ncol(cluster_means[,cluster_means[1,] > cluster_means[2,]])
ncol(cluster_means[,cluster_means[2,] > cluster_means[1,]])

confusionMatrix(fit_mvs$cluster, fit_mvs$cluster)  # accuracy: 0.973

data$group_survey = NA
data$group_survey[as.integer(names(fit_mvs$cluster))] = fit_mvs$cluster
data$group_survey = as.factor(data$group_survey)
control_cluster_no = which.max(cluster_means[,'amotivation.norm'])
d$cluster = as.factor(fit_mvs$cluster)
levels(data$group_survey) = c('control', 'autonomy')[c(control_cluster_no, 3-control_cluster_no)]  #theorized cluster meanings
summary(data$group_survey)
# de-norm (col - min(col))/(max(col)-min(col))
d <- data[!is.na(data$intrinsic),]
norm_max = apply(d[,mvs_scales], 2, max)
norm_min = apply(d[,mvs_scales], 2, min)
((cluster_means)*(norm_max-norm_min)+norm_min)/4

# Combined factor for treatment+group for later
data$TreatmentGroup <- interaction(data$treatment, data$group)
data$TreatmentGroup = factor(data$TreatmentGroup, levels(data$TreatmentGroup)[c(2,3,1,5,4,6)])
data$TreatmentGroupSurvey <- interaction(data$treatment, data$group_survey)
data$TreatmentGroupSurvey = factor(data$TreatmentGroupSurvey, levels(data$TreatmentGroupSurvey)[c(2,1,3,5,4,6)])
summary(data$group)
summary(data$TreatmentGroup)
summary(data$TreatmentGroupSurvey)



# DEMOGRAPHICS

dev.off()
RESO <- 300  # Resolution
PS <- 16  # Pointsize
LO <- matrix(c(1,1,1), nrow=3, ncol=1)
WIDTHS <- c(10) #widths of each figure in layout (i.e. column widths) in inch
HEIGHTS <- c(3.5)  #heights of each figure in layout (i.e. row heights) in inch
OMA <- c(0,0,0,0)  #Outer margins c(bottom, left, top, right)
HEIGHT <- sum(HEIGHTS) + OMA[1]*PS*1/72 + OMA[3]*PS*1/72
WIDTH <- sum(WIDTHS) + OMA[2]*PS*1/72 + OMA[4]*PS*1/72
png(paste("/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/deployment/demographics.png", sep=""), width=WIDTH, height=HEIGHT, units="in", res=RESO)
par(oma=OMA, ps=PS) #settings before layout
layout(LO, heights=HEIGHTS, widths=WIDTHS)
par(cex=1)


par(mfrow=c(3,1), oma=c(0,0,1,0))

stacked_barplot <- function(tab, ylab, labels) {
  par(mar=c(3, 3, 0, 2))
  midpoints <- barplot(as.matrix(tab), horiz=TRUE, beside = FALSE, col=gray.colors(length(tab), start=0.5))
  axis(side = 1, at = c(0, sum(tab)))
  title(ylab=ylab, line=1)
  sums = c(0, cumsum(tab))
  props = prop.table(tab)
  for (i in 1:length(sums)) text(sums[i] + tab[i]*0.5, midpoints, labels=c(paste(labels[i], percent(props[i], 0), sep="\n")))
}
stacked_barplot(xtabs(~sex, data=data), ylab="Sex", labels=c('female', 'male'))
stacked_barplot(xtabs(~occupation, data=data), ylab="Status", labels=levels(data$occupation))
stacked_barplot(xtabs(~age, data=data), ylab="Age", labels=c('18-26', '27-32', '33-40', '56+'))
title(outer=TRUE, main="")


