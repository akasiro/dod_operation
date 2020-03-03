rm(list = ls())
library(lme4)
library(stargazer)
library(car)
cover_lag1 <- read.csv('../../../datasets/derived/reg20200206/dod_lv1lv2_cover_lag1dv20200303.csv')
# 1.generate varabiles
# 1.1 diff centered by grand mean (Bickel, 2007; Hox, 2002)
Cdiff <- cover_lag1$diff - mean(cover_lag1$diff)
# 1.2 squared diff centered by grand mean
Cdiff2 <- Cdiff * Cdiff
# 1.3 logged cover
# in the model that dependent variable will be log(coverage)

# 2.descriptive analysis
stargazer(cover_lag1, type = 'html', title = 'Descriptive Analysis in coverage sample', out='../../../fig_tables/dod_hlhV1/descriptive_coverlag1_V1.htm')

# 3.VIF Thus, the researcher might consider collinearity to be a problem if VIF > 5 or 10 (Fox, 2016)
stargazer(vif(lm(coverage_1 ~ Cdiff + Cdiff2 +span + price + payInApp + size + compatibility + contentRank + age + samepubappnum, data=cover_lag1)), title = 'VIF test',type = 'html', out='../../../fig_tables/dod_hlhV1/vif_coverlag1_V1.htm')
# 4.regression
# 4.1.1 Model1.1 control varibles
Model1.1 <- lmer(coverage_1 ~ span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (1|lv2id_x), data=cover_lag1)
# 4.1.2 Model1.2 baseline model
Model1.2 <- lmer(coverage_1 ~ diff + diff2 + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (diff | lv2id_x) + (diff2 | lv2id_x) + (1|lv2id_x), data=cover_lag1)
# 4.1.3 Model1.3 Moderation gvaction
Model1.3 <- lmer(coverage_1 ~ diff + diff2 +gv_action + diff*gv_action + diff2*gv_action + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (diff | lv2id_x) + (diff2 | lv2id_x) + (1|lv2id_x), data=cover_lag1)
# 4.1.4 Model1.4 Moderation c_hetro
Model1.4 <- lmer(coverage_1 ~ diff + diff2 + c_hetro + diff*c_hetro + diff2*c_hetro + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (diff | lv2id_x) + (diff2 | lv2id_x) + (1|lv2id_x), data=cover_lag1)
# 4.2.1 Model2.1 log dv control
Model2.1 <- lmer(log(coverage_1) ~ span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (1|lv2id_x), data=cover_lag1)
# 4.2.2 Model2.2 log dv baseline
Model2.2 <- lmer(log(coverage_1) ~ diff + diff2 + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (diff | lv2id_x) + (diff2 | lv2id_x) + (1|lv2id_x), data=cover_lag1)
# 4.2.3 Model2.3 log Moderation gvaction
Model2.3 <- lmer(log(coverage_1) ~ diff + diff2 + gv_action + diff*gv_action + diff2*gv_action + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (diff | lv2id_x) + (diff2 | lv2id_x) + (1|lv2id_x), data=cover_lag1)
# 4.1.4 Model2.4 log Moderation c_hetro
Model2.4 <- lmer(log(coverage_1) ~ diff + diff2 + c_hetro + diff*c_hetro + diff2*c_hetro + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (diff | lv2id_x) + (diff2 | lv2id_x) + (1|lv2id_x), data=cover_lag1)
# 5.output and graph
stargazer(Model1.1, Model1.2,Model1.3, Model1.4, type = 'html', out='../../../fig_tables/dod_hlhV1/regression_coverlag1_V1.htm')
stargazer(Model2.1, Model2.2,Model2.3, Model2.4, type = 'html', out='../../../fig_tables/dod_hlhV1/regression_coverlag1_ln_V1.htm')