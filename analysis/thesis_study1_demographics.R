setwd('/Users/paul/Documents/_Studium/Master Inf/Thesis/code/pilot-study')
percent <- function(x, digits = 2, format = "f", ...) paste0(formatC(100 * x, format = format, digits = digits, ...), "%")

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

data[data$sex=='',]$age = '2732'
data[data$sex=='',]$education = '1'
data[data$sex=='',]$sex = 'female'

data = droplevels(data)


dev.off()
RESO <- 300  # Resolution
PS <- 16  # Pointsize
LO <- matrix(c(1,1,1), nrow=3, ncol=1)
WIDTHS <- c(10) #widths of each figure in layout (i.e. column widths) in inch
HEIGHTS <- c(3.5)  #heights of each figure in layout (i.e. row heights) in inch
OMA <- c(0,0,0,0)  #Outer margins c(bottom, left, top, right)
HEIGHT <- sum(HEIGHTS) + OMA[1]*PS*1/72 + OMA[3]*PS*1/72
WIDTH <- sum(WIDTHS) + OMA[2]*PS*1/72 + OMA[4]*PS*1/72
png(paste("/Users/paul/Documents/_Studium/Master Inf/Thesis/study results/mturk2/demographics.png", sep=""), width=WIDTH, height=HEIGHT, units="in", res=RESO)
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
stacked_barplot(xtabs(~education, data=data), ylab="Education", labels=c('HS/GED', 'College', 'Bachelor', 'Master', 'PhD'))
stacked_barplot(xtabs(~age, data=data), ylab="Age", labels=c('18-26', '27-32', '33-40', '41-55', '56+'))
title(outer=TRUE, main="")
