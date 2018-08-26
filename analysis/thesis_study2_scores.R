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


data[rev(mvs_scales)] = data[rev(mvs_scales)] / 4
data[rev(gcos_scales)] = data[rev(gcos_scales)] / 12

### Boxplots of score distributions
# MVS distribution
dev.off()
RESO <- 300  # Resolution
PS <- 12  # Pointsize
LO <- matrix(c(1,1,2), nrow=1, ncol=3)
WIDTHS <- c(4,4,4) #widths of each figure in layout (i.e. column widths) in inch
HEIGHTS <- c(5)  #heights of each figure in layout (i.e. row heights) in inch
OMA <- c(0,0,0,0)  #Outer margins c(bottom, left, top, right)
HEIGHT <- sum(HEIGHTS) + OMA[1]*PS*1/72 + OMA[3]*PS*1/72
WIDTH <- sum(WIDTHS) + OMA[2]*PS*1/72 + OMA[4]*PS*1/72
png(paste("/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/deployment/test-scores.png", sep=""), width=WIDTH, height=HEIGHT, units="in", res=RESO)
par(oma=OMA, ps=PS) #settings before layout
layout(LO, heights=HEIGHTS, widths=WIDTHS)
par(cex=1)
#par(mfrow=c(1,2))
par(mar=c(3,3,2,1))
boxplot(data[rev(mvs_scales)], names=stringr::str_to_title(rev(mvs_scales)), main="Motivation to Volunteer", xlab="Subscale score distribution", yaxt = "n", ylim=c(1,5))
axis(side = 2, at = seq(1, 5, 1))
# GCOS distribution
par(mar=c(3,1,2,3))
boxplot(data[rev(gcos_scales)], names=stringr::str_to_title(rev(gcos_scales)),  main="General causality orientation", xlab="Subscale score distribution", yaxt = "n", ylim=c(1,7))
axis(side = 4, at = seq(1, 7, 1))

nrow(data[!is.na(data$intrinsic),])
