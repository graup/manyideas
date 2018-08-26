setwd('/Users/paul/Documents/_Studium/Master Inf/Thesis/code/pilot-study')

test_scales = c('test_A', 'test_C', 'test_I')
mvs_scales = c('intrinsic', 'integrated', 'identified', 'introjected', 'external', 'amotivation')

data = read.csv("data/data.csv", sep=";", header=T)
num_total = nrow(data)

factor_cols <- c("order", "pair_order", "mvs_check", "comp_check", "age", "education", "sex")
data[factor_cols] <- lapply(data[factor_cols], factor)

data = data[data$duration>=300,]  # filter out very quick responses
data = data[data$comp_check=='1',]  # filter out failing the check
data = data[data$mvs_check=='1',]  # filter out failing the check
data = data[data$gcos_check=='1',]  # filter out failing the check
data$age = factor(data$age, levels(data$age)[c(2:5, 1)])  # reorder age factor
num_eligible = nrow(data)
summary(data)
print(paste('Total:', num_total))
print(paste('Eligible:', num_eligible))
print(paste('Ratio of invalid data:', 1-num_eligible/num_total))


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
png(paste("/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/mturk2/test-scores.png", sep=""), width=WIDTH, height=HEIGHT, units="in", res=RESO)
par(oma=OMA, ps=PS) #settings before layout
layout(LO, heights=HEIGHTS, widths=WIDTHS)
par(cex=1)
#par(mfrow=c(1,2))
par(mar=c(3,3,2,1))
boxplot(data[rev(mvs_scales)]/4, names=stringr::str_to_title(rev(mvs_scales)), main="Motivation to Volunteer", xlab="Subscale score distribution", yaxt = "n")
axis(side = 2, at = seq(1, 5, 1))
# GCOS distribution
par(mar=c(3,1,2,3))
boxplot(data[rev(test_scales)]/12, names=c('Impersonal','Control','Autonomy'), main="General causality orientation", xlab="Subscale score distribution", yaxt = "n")
axis(side = 4, at = seq(1, 7, 1))

