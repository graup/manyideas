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

d <- data

d$avg_issue_length_log = log(d$avg_issue_length)
is.na(d$avg_issue_length_log) <- sapply(d$avg_issue_length_log, is.infinite)

#is.na(d$avg_issue_length) <- sapply(d$avg_issue_length, function(a) a <= 0)

d$session_duration_min = d$session_duration/60

# log(avg_issue_length) like_count

# Survey data by treatment, plots
N_ = aggregate(issue_count ~ treatment, data=d, FUN=length)
tbl.mean = aggregate(cbind(issue_count, like_count, event_count, like_received_count, session_duration_min, avg_issue_length, avg_issue_length_log) ~ treatment, data=d, FUN=function(col){
                             mean(col)
                           })
tbl.sd = aggregate(cbind(issue_count, like_count, event_count, like_received_count, session_duration_min, avg_issue_length,  avg_issue_length_log) ~ treatment, data=d, FUN=function(col){
                           sd(col)
                         })
tbl.df = data.frame(tbl.mean[,2:ncol(tbl.mean)])
rownames(tbl.df) <- tbl.mean[,1]
#colnames(tbl.df) <- rnames
tbl.df2 = data.frame(tbl.sd[,2:ncol(tbl.sd)])
rownames(tbl.df2) <- tbl.sd[,1]
tbl.df.se <- tbl.df2 / sqrt(N_[,2])

tbl.df

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
png(paste("/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/deployment/issue-count.png", sep=""), width=WIDTH, height=HEIGHT, units="in", res=RESO)
par(oma=OMA, ps=PS) #settings before layout
layout(LO, heights=HEIGHTS, widths=WIDTHS)
par(cex=1)


tbl.df.all = tbl.df
tbl.df.se.all = tbl.df.se
tbl.df = tbl.df.all$avg_issue_length
tbl.df.se = tbl.df.se.all$avg_issue_length
  
par(mar=c(3,3,3,5), xpd=TRUE, lheight=1)
barCenters <- barplot(height = as.matrix(tbl.df), col=c("#BADB00","#dddddd","#00CFDB"),
                      beside = TRUE, horiz=TRUE,
                      xlim = c(0, max(tbl.df)+max(tbl.df.se) * 2),
                      main = "", cex.names=1, ylab = "", xlab = "Rating", las=1, border = NA, axes = TRUE)

axis(3)
text(c(0,0,0)+0.1, barCenters[,ncol(barCenters)], rownames(tbl.df), adj = c(0, 0.5), cex=0.8)
arrows(
  as.matrix(tbl.df) - as.matrix(tbl.df.se) * 2, barCenters,
  as.matrix(tbl.df) + as.matrix(tbl.df.se) * 2, barCenters, lwd = 1.5, angle = 90,
  code = 3, length = 0.02, col="#888888")
