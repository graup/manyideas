library(stargazer)
library(cluster) 
library(caret)

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



# post-hoc clustering with MVS sscales
set.seed(2018041627 + 735)
d = data[!is.na(data$intrinsic), c(mvs_scales_norm)]
fit_mvs <- kmeans(d, 2, iter.max=100)
# check if clustering separates scales. both should have more than 0 high means
cluster_means <- fit_mvs$centers
ncol(cluster_means[,cluster_means[1,] > cluster_means[2,]])
ncol(cluster_means[,cluster_means[2,] > cluster_means[1,]])

clusplot(d, fit_mvs$cluster, color=TRUE, labels=2, lines=0, main="Cluster based on post-survey MVS scores")
confusionMatrix(fit_mvs$cluster, fit_mvs$cluster)  # accuracy: 1

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


data$session_duration_minutes = data$session_duration / 60


# Select data for tables
d = data[!is.na(data$intrinsic), ]
d[,mvs_scales] = d[,mvs_scales]/4

## Engagement data by treatment + group_survey

N_ = aggregate(issue_count ~ group_survey*treatment, data=d, FUN=length)
tbl = aggregate(cbind(event_count, issue_count, like_count, comment_count, session_duration_minutes, avg_issue_length) ~ group_survey*treatment, data=d, FUN=function(col){
  #c(mean=mean(col), sd=sd(col))
  vals = sprintf("%4.1f", c(mean(col), sd(col)))
  paste(vals[1], ' (', vals[2], ')', sep='')
})
tbl = do.call(data.frame, tbl)
tbl$N = N_[,3]

tbl = tbl[order(tbl$group_survey),]
tbl2 = data.frame(t(tbl[,3:ncol(tbl)]))
colnames(tbl2) <- paste(tbl[,1], tbl[,2], sep=".")

stargazer(tbl2, digits=1, summary=FALSE, font.size='small')


# event_count interaction
dev.off()
RESO <- 300  # Resolution
PS <- 14  # Pointsize
LO <- matrix(c(1), nrow=1, ncol=1)
WIDTHS <- c(10) #widths of each figure in layout (i.e. column widths) in inch
HEIGHTS <- c(4)  #heights of each figure in layout (i.e. row heights) in inch
OMA <- c(0,0,0,0)  #Outer margins c(bottom, left, top, right)
HEIGHT <- sum(HEIGHTS) + OMA[1]*PS*1/72 + OMA[3]*PS*1/72
WIDTH <- sum(WIDTHS) + OMA[2]*PS*1/72 + OMA[4]*PS*1/72
png(paste("/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/deployment/event-count-interaction.png", sep=""), width=WIDTH, height=HEIGHT, units="in", res=RESO)
par(oma=OMA, ps=PS) #settings before layout
layout(LO, heights=HEIGHTS, widths=WIDTHS)
par(cex=1)
par(mar=c(5,5,1,1))
plot_median_arrows = function(medians) {
  abline(v=3.5)
  for (i in c(0, 1)) {
    for (j in c(-1, +1)) {
      arrows(i*3 + 2 + j*0.4, medians[i*3+2],
             i*3 + 2 + j*0.6, medians[i*3+2+j],
             length=0.15, col="red")
    }
  }
}
boxplot(event_count~treatment+group_survey, data=data, main="", ylab='event count', names=c('Autonomy', 'Baseline', 'Control','Autonomy', 'Baseline', 'Control'))
plot_median_arrows(aggregate(event_count ~ treatment*group_survey, data=data, FUN=median)$event_count)
mtext("Control Group                                                      Autonomy Group", 1, line=3)



## Engagement data by treatment

tbl = aggregate(cbind(event_count, issue_count, like_count, comment_count, session_duration_minutes, avg_issue_length) ~ treatment, data=d, FUN=function(col){
  vals = sprintf("%4.1f", c(mean(col), sd(col)))
  paste(vals[1], ' (', vals[2], ')', sep='')
})

N_ = aggregate(event_count ~ treatment, data=d, FUN=length)
tbl$N = N_[,2]

tbl = tbl[order(tbl$treatment),]
tbl2 = data.frame(t(tbl[,2:ncol(tbl)]))
colnames(tbl2) <- tbl[,1]

stargazer(tbl2, digits=1, summary=FALSE, font.size='small')

barplot(height = tbl$event_count.mean,
        beside = TRUE, las = 1,
        ylim = c(0, plotTop),
        cex.names = 0.75,
        main = "",
        ylab = "Rating",
        xlab = "Question",
        border = "black", axes = TRUE,
        legend.text = TRUE,
        args.legend = list(title = "Treatment", 
                           x = "topright",
                           cex = .7))


## Survey data by treatment + group_survey
rnames = c('Plan to continue use',               
           'Dropout reason Not interesting',
           'Dropout reason Unclear',
           'Dropout reason Insufficient reward',    
           'Dropout reason No impact',
           'Dropout reason Not enough time',
           'Dropout reason Contributed enough',     
           'Join reason Interesting',
           'Join reason Fun',
           'Join reason Important',     
           'Join reason Relatedness',
           'Join reason Sharing',
           'Join reason Help research',          
           'Join reason Reward',
           'Join reason motivation',
           'N')
tbl = aggregate(cbind(plan_continue_3_,               
                      reason_dropout_5_0_interesting, reason_dropout_5_1_unclear, reason_dropout_5_2_reward,    
                      reason_dropout_5_3_impact, reason_dropout_5_4_time, reason_dropout_5_5_enough,     
                      reason_join_0_0_interesting, reason_join_0_1_fun, reason_join_0_2_important,     
                      reason_join_0_3_relatedness, reason_join_0_4_sharing, reason_join_0_5_help,          
                      reason_join_0_6_reward, reason_join_0_7_amotivation) ~ group_survey*treatment, data=d, FUN=function(col){
  vals = sprintf("%.1f", c(mean(col), sd(col)))
  paste(vals[1], ' (', vals[2], ')', sep='')
})

N_ = aggregate(intrinsic ~ group_survey*treatment, data=d, FUN=length)
tbl$N = N_[,3]

tbl = tbl[order(tbl$group_survey),]
tbl2 = data.frame(t(tbl[,3:ncol(tbl)]))
colnames(tbl2) <- paste(tbl[,1], tbl[,2], sep=".")
rownames(tbl2) <- rnames
stargazer(tbl2, digits=1, summary=FALSE, font.size='small')


## Survey data by treatment

tbl = aggregate(cbind(intrinsic, integrated, identified, introjected, external, amotivation,
                      plan_continue_3_, plan_revisit_2_,               
                      reason_dropout_5_0_interesting, reason_dropout_5_1_unclear, reason_dropout_5_2_reward,    
                      reason_dropout_5_3_impact, reason_dropout_5_4_time, reason_dropout_5_5_enough,     
                      reason_join_0_0_interesting, reason_join_0_1_fun, reason_join_0_2_important,     
                      reason_join_0_3_relatedness, reason_join_0_4_sharing, reason_join_0_5_help,          
                      reason_join_0_6_reward, reason_join_0_7_amotivation) ~ treatment, data=d, FUN=function(col){
  vals = sprintf("%.1f", c(mean(col), sd(col)))
  paste(vals[1], ' (', vals[2], ')', sep='')
})

N_ = aggregate(event_count ~ treatment, data=d, FUN=length)
tbl$N = N_[,2]

tbl = tbl[order(tbl$group_survey),]
tbl2 = data.frame(t(tbl[,2:ncol(tbl)]))
colnames(tbl2) <- tbl[,1]

stargazer(tbl2, digits=1, summary=FALSE, font.size='small')


library(lsmeans)
library(car)
mod = lm(cbind(intrinsic, integrated, identified, introjected, external, amotivation,
               plan_continue_3_, plan_revisit_2_,               
               reason_dropout_5_0_interesting, reason_dropout_5_1_unclear, reason_dropout_5_2_reward,    
               reason_dropout_5_3_impact, reason_dropout_5_4_time, reason_dropout_5_5_enough,     
               reason_join_0_0_interesting, reason_join_0_1_fun, reason_join_0_2_important,     
               reason_join_0_3_relatedness, reason_join_0_4_sharing, reason_join_0_5_help,          
               reason_join_0_6_reward, reason_join_0_7_amotivation) ~ treatment, data=d)
Anova(mod, type=3)
summary(mod)
lsmeans(mod, tukey ~ treatment ) # | group_survey)

# omnibus significant:  AvB, AvC, BvC
# external  0.01, , 0.4
# reason_dropout_5_0_interesting  0.07, , 
# reason_dropout_5_1_unclear
# reason_join_0_1_fun
# reason_join_0_6_reward , , 0.08
mod = lm(reason_join_0_7_amotivation ~ treatment, data=d)
Anova(mod, type=3)
lsmeans(mod, tukey ~ treatment)

lsm
#pairs(lsm, adjust="tukey")
#lsm
#contrast(lsm, list(CvB = c(0,1,-1), AvB=c(-1,1,0), AvC=c(-1,0,1)), adjust="bon")


# Survey data by treatment, plots
rnames = c('Plan to continue use',               
           'Dropout reason\nNot interesting',
           'Dropout reason\nUnclear',
           'Dropout reason\nInsufficient reward',    
           'Dropout reason\nNo impact',
           'Dropout reason\nNot enough time',
           'Dropout reason\nContributed enough',     
           'Join reason\nInteresting',
           'Join reason\nFun',
           'Join reason\nImportant',     
           'Join reason\nRelatedness',
           'Join reason\nSharing',
           'Join reason\nHelp research',          
           'Join reason\nReward',
           'Join reason\nAmotivation')
tbl.mean = aggregate(cbind(plan_continue_3_,               
                           reason_dropout_5_0_interesting, reason_dropout_5_1_unclear, reason_dropout_5_2_reward,    
                           reason_dropout_5_3_impact, reason_dropout_5_4_time, reason_dropout_5_5_enough,     
                           reason_join_0_0_interesting, reason_join_0_1_fun, reason_join_0_2_important,     
                           reason_join_0_3_relatedness, reason_join_0_4_sharing, reason_join_0_5_help,          
                           reason_join_0_6_reward, reason_join_0_7_amotivation) ~ treatment, data=d, FUN=function(col){
  mean(col)
})
tbl.sd = aggregate(cbind(plan_continue_3_,               
                         reason_dropout_5_0_interesting, reason_dropout_5_1_unclear, reason_dropout_5_2_reward,    
                         reason_dropout_5_3_impact, reason_dropout_5_4_time, reason_dropout_5_5_enough,     
                         reason_join_0_0_interesting, reason_join_0_1_fun, reason_join_0_2_important,     
                         reason_join_0_3_relatedness, reason_join_0_4_sharing, reason_join_0_5_help,          
                         reason_join_0_6_reward, reason_join_0_7_amotivation) ~ treatment, data=d, FUN=function(col){
  sd(col)
})
tbl.df = data.frame(tbl.mean[,2:ncol(tbl.mean)])
rownames(tbl.df) <- tbl.mean[,1]
colnames(tbl.df) <- rnames
tbl.df2 = data.frame(tbl.sd[,2:ncol(tbl.sd)])
rownames(tbl.df2) <- tbl.sd[,1]
tbl.df.se <- tbl.df2 / sqrt(N_[,2])

#N_ = aggregate(event_count ~ treatment, data=d, FUN=length)



### Setup plot
dev.off()
RESO <- 300  # Resolution
PS <- 19  # Pointsize
LO <- matrix(c(1), nrow=1, ncol=1)
WIDTHS <- c(10) #widths of each figure in layout (i.e. column widths) in inch
HEIGHTS <- c(20)  #heights of each figure in layout (i.e. row heights) in inch
OMA <- c(0,0,0,0)  #Outer margins c(bottom, left, top, right)
HEIGHT <- sum(HEIGHTS) + OMA[1]*PS*1/72 + OMA[3]*PS*1/72
WIDTH <- sum(WIDTHS) + OMA[2]*PS*1/72 + OMA[4]*PS*1/72
png(paste("/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/deployment/survey-questions2.png", sep=""), width=WIDTH, height=HEIGHT, units="in", res=RESO)
par(oma=OMA, ps=PS) #settings before layout
layout(LO, heights=HEIGHTS, widths=WIDTHS)
par(cex=1)

par(mar=c(3,14,3,5), xpd=TRUE, lheight=1)
barCenters <- barplot(height = as.matrix(tbl.df), col=c("#BADB00","#dddddd","#00CFDB"),
        beside = TRUE, xlim = c(0, 7), horiz=TRUE,
        main = "", cex.names=1, ylab = "", xlab = "Rating", las=1, border = NA, axes = TRUE)

grid(NULL, NA, col="#444444")

barCenters <- barplot(add=TRUE, height = as.matrix(tbl.df), col=c("#BADB00","#dddddd","#00CFDB"),
                      beside = TRUE, xlim = c(0, 7), horiz=TRUE,
                      main = "", cex.names=1, ylab = "", xlab = "Rating", las=1, border = NA, axes = TRUE)

axis(3, at=0:7)
text(c(0,0,0)+0.1, barCenters[,ncol(barCenters)], rownames(tbl.df), adj = c(0, 0.5), cex=0.8)
arrows(
       as.matrix(tbl.df) - as.matrix(tbl.df.se) * 2, barCenters,
       as.matrix(tbl.df) + as.matrix(tbl.df.se) * 2, barCenters, lwd = 1.5, angle = 90,
       code = 3, length = 0.02, col="#888888")



summary(data[, c('plan_continue_3_',               
             'reason_dropout_5_0_interesting', 'reason_dropout_5_1_unclear', 'reason_dropout_5_2_reward',    
             'reason_dropout_5_3_impact', 'reason_dropout_5_4_time', 'reason_dropout_5_5_enough',     
             'reason_join_0_0_interesting', 'reason_join_0_1_fun', 'reason_join_0_2_important',     
             'reason_join_0_3_relatedness', 'reason_join_0_4_sharing', 'reason_join_0_5_help',          
             'reason_join_0_6_reward', 'reason_join_0_7_amotivation')])

par(mar=c(3,14,3,5), xpd=TRUE, lheight=1)

boxplot(data[, c('plan_continue_3_',               
                 'reason_dropout_5_0_interesting', 'reason_dropout_5_1_unclear', 'reason_dropout_5_2_reward',    
                 'reason_dropout_5_3_impact', 'reason_dropout_5_4_time', 'reason_dropout_5_5_enough',     
                 'reason_join_0_0_interesting', 'reason_join_0_1_fun', 'reason_join_0_2_important',     
                 'reason_join_0_3_relatedness', 'reason_join_0_4_sharing', 'reason_join_0_5_help',          
                 'reason_join_0_6_reward', 'reason_join_0_7_amotivation')], horizontal=TRUE, las=2)
