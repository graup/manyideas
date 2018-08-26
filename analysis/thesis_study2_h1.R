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
clusplot(d, fit$cluster, color=TRUE, labels=2, lines=0, main="Cluster based on GCOS/MVS scores")
data$group_survey = NA
data$group_survey[as.integer(names(fit$cluster))] = fit$cluster
data$group_survey = as.factor(data$group_survey)
control_cluster_no = which.max(cluster_means[,'amotivation.norm'])
d$cluster = as.factor(fit$cluster)
levels(data$group_survey) = c('control', 'autonomy')[c(control_cluster_no, 3-control_cluster_no)]  #theorized cluster meanings
summary(data$group_survey)

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
clusplot(d, fit_mvs$cluster, color=TRUE, labels=2, lines=0, main="Cluster based on post-survey MVS scores")

ord <- rev(order(abs(fit$centers[1,]-fit$centers[2,])))
print("Cluster 1")
colnames(cluster_means[,cluster_means[1,] > cluster_means[2,]])  # amotivation, impoersonal, external, control
print("Cluster 2")
colnames(cluster_means[,cluster_means[1,] < cluster_means[2,]])  # identified, intrinsic, autonomy, integrated

# de-norm (col - min(col))/(max(col)-min(col))
d <- data[!is.na(data$intrinsic),]
norm_max = apply(d[,mvs_scales], 2, max)
norm_min = apply(d[,mvs_scales], 2, min)
((cluster_means)*(norm_max-norm_min)+norm_min)/4


# try only GCOS
s <- as.integer(runif(1)*1000)
print(s)
set.seed(2018041627 + 361)
d = data[!is.na(data$control.norm), c(gcos_scales)]
fit_gcos <- kmeans(d, 2, iter.max=100)
fit_gcos$cluster <- 3 - fit_gcos$cluster
# check if clustering separates scales
cluster_means <- fit_gcos$centers
ncol(cluster_means[,cluster_means[1,] > cluster_means[2,]])
ncol(cluster_means[,cluster_means[2,] > cluster_means[1,]])
library(caret)
confusionMatrix(fit_mvs$cluster, fit_gcos$cluster)

confusionMatrix(fit_mvs$cluster, fit_gcos$cluster)


# Compare with PCA to check if it has the same clustering
library(FactoMineR)
q = ncol(d)
result <- PCA(d, ncp=2, quali.sup=q)
summary(result)
result$var$cor[rev(order(abs(result$var$contrib[,"Dim.1"]))),"Dim.1"]  # +control    +external  +introjected
result$var$cor[rev(order(abs(result$var$contrib[,"Dim.2"]))),"Dim.2"]  # +identified    +intrinsic  -amotivation
plot(result, choix="ind", habillage=q)
plotellipses(result, q)

levels(data$group_survey) = c('control', 'autonomy')[c(control_cluster_no, 3-control_cluster_no)]  #theorized cluster meanings
summary(data$group_survey)


confusionMatrix(data$group, factor(data$group_survey, levels(data$group_survey)[c(2,1)]))



# check representation of treatments
xtabs(~treatment, data[!is.na(data$group_survey),])
apply(prop.table(xtabs(~treatment+group, data)), c(1,2), percent)
xtabs(~treatment+group_survey, data)
apply(prop.table(xtabs(~treatment+group_survey, data)), c(1,2), percent)
# find users to nudge again
data[is.na(data$group_survey) & data$treatment == 'autonomy',]$email


# Combined factor for treatment+group for later
data$TreatmentGroup <- interaction(data$treatment, data$group)
data$TreatmentGroup = factor(data$TreatmentGroup, levels(data$TreatmentGroup)[c(2,3,1,5,4,6)])
data$TreatmentGroupSurvey <- interaction(data$treatment, data$group_survey)
data$TreatmentGroupSurvey = factor(data$TreatmentGroupSurvey, levels(data$TreatmentGroupSurvey)[c(2,1,3,5,4,6)])
summary(data$group)
summary(data$TreatmentGroup)
summary(data$TreatmentGroupSurvey)
#prop.table(summary(data$TreatmentGroup))


# Correlation between all factors, for lazy people
library(corrplot)
#c <- cor(model.matrix(~.-1+TreatmentGroup, data=data[,c(seq(4, 16), 54)]))
#corrplot(c)
d <- data[!is.na(data$group_survey), c(64, seq(51, 60), 4, 5, 7, seq(9, 16), seq(27, 47), 62, 66)]
p.mat <- data.frame(matrix(0, ncol = length(colnames(d)), nrow = length(colnames(d))))
colnames(p.mat) <- colnames(d)
rownames(p.mat) <- colnames(d)
p.mat[which(sapply(d[1,], is.numeric)), which(sapply(d[1,], is.numeric))] <- cor.mtest(d[,colnames(d)[sapply(d[1,], is.numeric)]], conf.level = .95)$p
c <- cor(model.matrix(~.-1, data=d))  # & data$TreatmentGroupSurvey != 'autonomy.1'  & data$TreatmentGroupSurvey != 'baseline.1'
p.mat.base <- data.frame(matrix(1, ncol = length(colnames(c)), nrow = length(colnames(c))))
colnames(p.mat.base) <- colnames(c)
rownames(p.mat.base) <- colnames(c)
names_both = intersect(rownames(p.mat.base), rownames(p.mat))
p.mat.base[names_both, names_both] = p.mat[names_both, names_both]
# if plotting significance levels, only numeric factors are considered!
for (col in colnames(d)[sapply(d[1,], is.numeric)]) {
  frm <- as.formula(paste(col, 'group_survey', sep='~'))
  a <- aov(frm, data=data)
  p <- unlist(summary(a))["Pr(>F)1"]
  p.mat.base[c(1,2),col] = p
  p.mat.base[col, c(1,2)] = p
}
for (col in colnames(d)[sapply(d[1,], is.numeric)]) {
  frm <- as.formula(paste(col, 'TreatmentGroupSurvey', sep='~'))
  a <- aov(frm, data=data)
  p <- unlist(summary(a))["Pr(>F)1"]
  nr = nrow(p.mat.base)
  p.mat.base[c(seq(nr-5,nr)),col] = p
  p.mat.base[col, c(seq(nr-5,nr))] = p
}

corrplot(c, method="ellipse", diag=FALSE, order="AOE", p.mat = data.matrix(p.mat.base),  # or alphabet
         sig.level = 0.01,
         insig="label_sig",
         pch = "*", pch.cex = 1,)



# compairosn of mean between survey groups
xtabs(~treatment, data[!is.na(data$intrinsic),])
xtabs(like_count ~ group_survey, data) / xtabs( ~ group_survey, data)
xtabs(like_count ~ TreatmentGroupSurvey, data) / xtabs( ~ TreatmentGroupSurvey, data)



# DEMOGRAPHICS
par(mfrow=c(3,1), oma=c(0,0,2,0))

stacked_barplot <- function(tab, ylab, labels) {
  par(mar=c(3, 3, 0, 2))
  midpoints <- barplot(as.matrix(tab), horiz=TRUE, beside = FALSE, col=gray.colors(length(tab), start=0.5))
  axis(side = 1, at = c(0, sum(tab)))
  title(ylab=ylab, line=1)
  sums = c(0, cumsum(tab))
  props = prop.table(tab)
  for (i in 1:length(sums)) text(sums[i] + tab[i]*0.5, midpoints, labels=c(paste(labels[i], percent(props[i]), sep="\n")))
}
stacked_barplot(xtabs(~sex, data=data), ylab="Sex", labels=c('female', 'male'))
stacked_barplot(xtabs(~occupation, data=data), ylab="Status", labels=levels(data$occupation))
stacked_barplot(xtabs(~age, data=data), ylab="Age", labels=c('18-26', '27-32', '33-40', '56+'))
title(outer=TRUE, main="Participants demorgaphics")


a <- aov(event_count~TreatmentGroupSurvey, data=data)
summary(a)

# Plots to get an idea about the data
plot(issue_count ~ treatment, data=data) # median=0, might not make much sense to analyze this variable further
plot(like_count ~ treatment, data=data)
plot(event_count ~ treatment, data=data)
plot(like_count ~ sex, data=data)  # women are more active than men??
plot(like_count ~ age, data=data)
plot(like_count ~ occupation, data=data)

plot(any_interaction ~ group_survey, data=data)

plot(plan_continue_3_ ~ treatment, data=data)  # maybe interesting
plot(plan_continue_3_ ~ group_survey, data=data)  # maybe interesting
plot(plan_continue_3_ ~ TreatmentGroupSurvey, data=data)
plot(reason_dropout_5_2_reward ~ treatment, data=data)
plot(reason_dropout_5_2_reward ~ TreatmentGroupSurvey, data=data)

plot(session_duration ~ treatment, data=data)
plot(avg_session_duration ~ treatment, data=data)
plot(avg_issue_length ~ treatment, data=data)
plot(event_count ~ treatment, data=data)  #no
plot(like_count ~ treatment, data=data)  #no

# Interaction plots
library(plyr)
with(data, interaction.plot(treatment, group_survey, event_count))


par(mar=c(3,15,3,3))
boxplot(data[,31:47], horizontal=TRUE, las=1)
abline(h=c(3.5, 9.5), lty=3, col="#888888")


# AttrkDiff mini scores
par(mar=c(3,6,3,3))
boxplot(data[,27:30], horizontal=TRUE, las=1)
summary(data[,27:30])
apply(data[,27:30], 2, function(col) c(mean=mean(col[!is.na(col)]), sd=sd(col[!is.na(col)])))


d <- data[!is.na(data$TreatmentGroupSurvey),]
t.test(d[d$TreatmentGroupSurvey=='control.control',]$event_count,
       d[d$TreatmentGroupSurvey=='autonomy.control',]$event_count)  #p=0.19

m = aov(session_duration.log ~ group_survey, data=dt)
anova(m) # report anova, omnibus test
plot(session_duration.log ~ group_survey, data=dt)
library(multcomp)

for (col in colnames(data)[27:47]) {
  frm <- as.formula(paste(col, 'TreatmentGroupSurvey', sep='~'))
  a <- aov(frm, data=data)
  p <- unlist(summary(a))["Pr(>F)1"]
  if (p<0.05) {
    print(col)
    print(p)
  }
  #summary(a)
}
# goodness, reason_dropout_5_1_unclear, reason_join_0_7_amotivation


with(data[!is.na(data$event_count),], {
  interaction.plot(treatment, group, event_count, fun=mean)
  abline(h=median(event_count), lty=3, col='#999999')
  text(3.5, median(event_count),
       paste('global median =', round(mean(event_count), 2),
             '\nglobal sd =', round(sd(event_count), 2)), cex=.85)
})
with(data[data$like_count>0,], {
  interaction.plot(treatment, group, like_count)
  abline(h=mean(like_count), lty=3, col='#999999')
  text(3.5, mean(like_count),
       paste('global mean =', round(mean(like_count), 2),
             '\nglobal sd =', round(sd(like_count), 2)), cex=.85)
})
with(data[data$avg_issue_length>0,], {
  interaction.plot(treatment, group, avg_issue_length)
  abline(h=mean(avg_issue_length), lty=3, col='#999999')
  text(3.5, mean(avg_issue_length),
       paste('global mean =', round(mean(avg_issue_length), 2),
             '\nglobal sd =', round(sd(avg_issue_length), 2)), cex=.85)
})

#with(data[data$like_received_count>0,], interaction.plot(treatment, group, like_received_count, ylim=c(0, 20)))
menasd <- ddply(data, ~ treatment+group, summarise, mean=mean(avg_issue_length), sd=sd(avg_issue_length))
menasd[order(menasd$group),]  # High sd, does this plot really make sense?

#with(data[data$like_count>0,], interaction.plot(treatment, group, like_count, ylim=c(0, 10)))  # N=68
#menasd <- ddply(data, ~ treatment+group, summarise, like_count.mean=mean(like_count), like_count.sd=sd(like_count))
#menasd[order(menasd$group),]  # High sd, does this plot really make sense?

# GA data N=105
with(data[!is.na(data$event_count),], interaction.plot(treatment, group, event_count, ylim=c(0, 50)))
with(data[!is.na(data$session_duration),], interaction.plot(treatment, group, session_duration, ylim=c(0, 1000)))
with(data[!is.na(data$session_count),], interaction.plot(treatment, group, session_count, ylim=c(0, 5)))
with(data[!is.na(data$avg_session_duration),], interaction.plot(treatment, group, avg_session_duration, ylim=c(0, 1000)))


menasd <- ddply(data, ~ treatment+group, summarise,
                session_duration.log.mean=mean(session_duration.log), session_duration.log.sd=sd(session_duration.log))
menasd[order(menasd$group),]  # High sd, does this plot really make sense?




# Verify that data is poisson distributed
hist(data$like_count, breaks=length(levels(factor(data$like_count))))
library(fitdistrplus)
library(gamlss)
library(VGAM)

fit_pois = fitdist(data[!is.na(data$session_duration) & !is.na(data$group_survey),]$event_count, "lnorm", discrete=TRUE)
plot(fit_pois)
gofstat(fit_pois) # event_count seems possin distributed


par(ask=TRUE) 
for (cond in levels(data$group_survey)) {
  dt <- data$session_duration[!is.na(data$session_duration) & data$session_duration > 0 & !is.na(data$group_survey) & data$group_survey == cond]
  print(nrow(dt))
  fit_pois = fitdist(dt, "lnorm", discrete=TRUE)
  plot(fit_pois)
}
# log normal seems to fit for session_duration
dt <- data[data$session_duration > 0 & !is.na(data$group_survey),]
m = aov(session_duration.log ~ group_survey, data=dt)
anova(m) # report anova, omnibus test
plot(session_duration.log ~ group_survey, data=dt)
library(multcomp)
summary(glht(m, mcp(group_survey="Tukey")), test=adjusted(type="holm")) # Tukey means compare all pairs


fit_zpois = fitdist(dt, "ZIP", discrete=TRUE, start=list(mu=2, sigma=0.5))
plot(fit_zpois) # zero-inflate poisson might work but..
gofstat(fit_pois) # p<0.001.. still not a good fit
fit_nb = fitdist(dt, "nbinom", discrete=TRUE, start = list(mu=2, size = 10))  # sigma = 0.5
fit_znb = fitdist(dt, "zinegbin", discrete=TRUE, start = list(munb=2, size = 10)) 
plot(fit_nb)
# goodness-of-fit test. p>0.05 = we don't differ significantly from that distribution
gofstat(fit_nb)  # == fit_znb
# nbinom seems to fit best

# Poisson regression for count responses.
# Data does not seem to be poisson distributed, still keeping the code for later
library(multcomp)
library(car)
m_pois = glm(like_count ~ TreatmentGroup, data=data, family=poisson)
summary(m_pois)  # AIC: 809
Anova(m_pois, type=3) # overall signficiant, so justified to continue with pariwise comparisons
summary(glht(m_pois, mcp(TreatmentGroup="Tukey")), test=adjusted(type="holm"))  # mostly non-significant



m <- glm(reason_dropout_5_2_reward ~ treatment, data=data[!is.na(data$reason_dropout_5_2_reward),])
Anova(m, type=3)
summary(glht(m, mcp(treatment="Tukey")), test=adjusted(type="holm"))  # mostly non-significant


fit.issue_length = fitdist(data$avg_issue_length, "pois")
plot(fit.issue_length) # zero-inflate poisson might work but..
gofstat(fit.issue_length) # p<0.001.. still not a good fit



library(car)
leveneTest(issue_count ~ treatment, data=data)  #>0.05, ok
fit.lm <- lm(issue_count ~ treatment, data=data)
Anova(fit.lm, type=3)


m = glm(issue_count ~ treatment, data=data, family="poisson")
aov <- Anova(m, type=3)
aov
summary(aov, multivariate=F)

#qqnorm(residuals(m)); qqline(residuals(m)) # s'ok! Poisson regression makes no normality assumption

# conduct pairwise comparisons among levels of Technique
library(multcomp)
summary(glht(m, mcp(treatment="Tukey")), test=adjusted(type="holm")) # Tukey means compare all pairs



fit.lm <- lm(log(avg_issue_length) ~ treatment, data=data[data$avg_issue_length>0,])
summary(fit.lm)
boxplot(log(avg_issue_length) ~ treatment, data=data[data$avg_issue_length>0,])
m_pois = lm(log(avg_issue_length) ~ treatment, data=data[data$avg_issue_length>0,])   #binomial for has_returned 
summary(m_pois)
Anova(m_pois, type=3)
#summary(glht(m_pois, mcp(treatment="Tukey")), test=adjusted(type="holm"))
# issue_count pois: signficiant in control over autonomy and baseline (<0.05), not baseline over autonomy
# like_count pois: significant in both control and baseline over autonomy (p<0.01), but not control over baseline
# avg_issue_length lognormal: significant in all pairs p<0.05
# has_returned binomial
library(MASS)
m_nb <- glm.nb(event_count ~ treatment, data=data$event_count[!is.na(data$event_count)])
summary(m_nb)
summary(glht(m_nb, mcp(treatment="Tukey")), test=adjusted(type="holm"))
# event_count:


# Negative binomial regression
# https://stats.idre.ucla.edu/r/dae/negative-binomial-regression/
library(MASS)
m_nb <- glm.nb(log(avg_issue_length) ~ treatment, data=data[data$avg_issue_length>0,])
summary(m_nb)
summary(glht(m_nb, mcp(treatment="Tukey")), test=adjusted(type="holm"))

m_nb <- glm.nb(event_count ~ treatment:group_survey, data=data)
summary(m_nb)  # AIC: 488
# Report only meaningful pairwise comparisons
summary(glht(m_nb, mcp(treatment="Tukey", group_survey="Tukey")),
        test=adjusted(type="holm"))



library(lsmeans)
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
# event_count, interaction
boxplot(event_count~treatment+group_survey, data=data, main="event count by treatment.group")
plot_median_arrows(aggregate(event_count ~ treatment*group_survey, data=data, FUN=median)$event_count)
mod.pois = glm(event_count ~  treatment * group_survey, data=data, family='poisson')
Anova(mod.pois, type=3)
lsmeans(mod.pois, tukey ~ treatment | group_survey)
# in control group, treatment autonomy has significantly smaller event_count than control (p<0.05)

boxplot(log(avg_session_duration)~treatment, data=data, main="event count by treatment.group")
mod.pois = glm(log(avg_session_duration) ~  treatment , data=data, family='Gamma')
lsmeans(mod.pois, tukey ~ treatment)

# like_count
boxplot(like_count~treatment+group_survey, data=data, main="like count by treatment.group")
plot_median_arrows(aggregate(like_count ~ treatment*group_survey, data=data, FUN=median)$like_count)
mod.bn = glm.nb(like_count ~  treatment * group_survey, data=data)
lsmeans(mod.bn, tukey ~ treatment | group_survey)
# in control group, treatment autonomy has significantly smaller like_count than control (p<0.05)

# issue length
boxplot(avg_issue_length~treatment+group_survey, data=data, main="average issue length by treatment.group")
plot_median_arrows(aggregate(avg_issue_length ~ treatment*group_survey, data=data, FUN=median)$avg_issue_length)
fitdi = fitdist(data[!is.na(data$avg_issue_length) & data$avg_issue_length>0,]$avg_issue_length, "gamma")
plot(fitdi)
gofstat(fitdi)
mod.bn = glm(log(avg_issue_length) ~  treatment * group_survey, data=data[data$avg_issue_length>0,], family="Gamma")
lsmeans(mod.bn, tukey ~ treatment | group_survey)

mod.bn = glm(avg_issue_length ~  treatment, data=data[data$avg_issue_length>0,], family="Gamma")
lsmeans(mod.bn, tukey ~ treatment)

# lognorm seems fitting
fitdi = fitdist(data[!is.na(data$avg_issue_length) & data$avg_issue_length>0,]$avg_issue_length, "lnorm")
plot(fitdi)
gofstat(fitdi)

# attrakdiff
boxplot(beauty~group_survey, data=data)
mod.pois = glm(beauty ~  group_survey, data=data)
summary(mod.pois)
lsmeans(mod.pois, tukey ~ group_survey)

# issue_count
boxplot(issue_count~treatment+group_survey, data=data, main="like count by treatment.group")
plot_median_arrows(aggregate(issue_count ~ treatment*group_survey, data=data, FUN=median)$issue_count)
mod.bn = glm.nb(issue_count ~  treatment * group_survey, data=data)
lsmeans(mod.bn, tukey ~ treatment | group_survey)

boxplot(like_count~treatment, data=data, main="issue_count by treatment")
plot_median_arrows(aggregate(like_count ~ treatment, data=data, FUN=median)$like_count)
mod.bn = glm.nb(like_count ~  treatment, data=data)
lsmeans(mod.bn, tukey ~ treatment)

# reason_dropout_5_1_unclear
# reason_dropout_5_2_reward
boxplot(reason_dropout_5_1_unclear~treatment+group_survey, data=data, main="like count by treatment.group")
plot_median_arrows(aggregate(reason_dropout_5_1_unclear ~ treatment*group_survey, data=data, FUN=median)$reason_dropout_5_1_unclear)
mod.bn = lm(reason_dropout_5_1_unclear ~  treatment * group_survey, data=data)
Anova(mod.bn, type=3)
summary(mod.bn) # s. for group_surveyautonomy p<0.01
lsmeans(mod.bn, tukey ~ treatment | group_survey)

mod.bn = glm(reason_dropout_5_2_reward ~  treatment, data=data)
Anova(mod.bn, type=3)

# has_returned
boxplot(session_count~treatment+group_survey, data=data[data$session_count>0,])
plot_median_arrows(aggregate(session_count ~ treatment*group_survey, data=data, FUN=median)$session_count)
mod.bn = glm.nb(session_count ~ treatment * group_survey, data=data[data$session_count>0,])
summary(mod.bn) # s. for group_surveyautonomy p<0.01
lsmeans(mod.bn, tukey ~ treatment | group_survey)

# Zero-inflated Poisson regression for count responses
library(pscl)
m_zinp = zeroinfl(like_count ~ TreatmentGroup, dist="poisson", link="logit", data=data)
m_zinb = zeroinfl(like_count ~ TreatmentGroup, dist="negbin", link="logit", data=data)
summary(m_zinp)
Anova(m_zinp, type=3)

pchisq(2 * (logLik(m_zinb) - logLik(m_zinp)), df = 1, lower.tail = FALSE)  # ~0, m_zinb is better than m_zinp


## compute contrasts "by hand" for ZINB
get_contr <- function(d, fit) {
  nr <- length(levels(d))
  contr <- matrix(0, nrow = nr*(nr-1)/2, ncol = length(coef(fit))) 
  colnames(contr) <- names(coef(fit)) 
  combs <- combn(1:6, 2)
  rownames(contr) <- paste(levels(d)[combs[2,]], 
                           levels(d)[combs[1,]], sep = " - ") 
  contr[,2:6] <- contrMat(numeric(nr), type = "Tukey")[,1:5] 
  contr
}
summary(glht(m_zinp, linfct=get_contr(data$TreatmentGroup, m_zinp)), test=adjusted(type="holm"))
#summary(glht(m_zinb, linfct=get_contr(data$TreatmentGroup, m_zinb)), test=adjusted(type="holm"))




# these two are identical, so I basically rewrote the mcp function :D
summary(glht(m_pois, mcp(TreatmentGroup="Tukey")), test=adjusted(type="holm"))
summary(glht(m_pois, linfct = get_contr(data$TreatmentGroup, m_pois)), test=adjusted(type="holm"))

