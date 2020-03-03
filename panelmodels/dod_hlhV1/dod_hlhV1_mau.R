rm(list = ls())
library(lme4)
library(stargazer)
library(car)
mau <- read.csv('../../../datasets/derived/reg20200206/dod_lv1lv2_mau20200221.csv')
# 1.generate varabiles
# 1.1 diff centered by grand mean (Bickel, 2007; Hox, 2002)
Cdiff <- mau$diff - mean(mau$diff)
# 1.2 squared diff centered by grand mean
Cdiff2 <- Cdiff * Cdiff
# 1.3 logged cover
# in the model that dependent variable will be log(coverage)

# 2.descriptive analysis
stargazer(mau, type = 'text', title = 'Descriptive Analysis')

# 3.VIF
stargazer(vif(lm(mau~ Cdiff + Cdiff2 +span + price + payInApp + size + compatibility + contentRank + age + samepubappnum, data=mau)), title = 'VIF test',type = 'text')
# 4.regression
# 4.1 Model1 control varibles
Model1 <- lmer(mau ~ span + price + payInApp + size + compatibility + contentRank + age + samepubappnum+ (1|lv2id_x), data=mau)
# 4.2 Model2 baseline model
Model2 <- lmer(mau ~ diff + diff2 + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (Cdiff | lv2id_x) + (Cdiff2 | lv2id_x) + (1|lv2id_x), data=mau)
# 5.output and graph
stargazer(Model1, Model2, type= 'text')
