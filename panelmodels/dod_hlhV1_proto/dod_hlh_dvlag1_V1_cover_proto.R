rm(list = ls())
library(lme4)
library(stargazer)
library(car)
cover_lag1 <- read.csv('../../../datasets/derived/reg20200303/dod_lv1lv2_cover_lag1dv20200303.csv')
# 1.generate varabiles
# 1.1 Cdiff centered by grand mean (Bickel, 2007; Hox, 2002)
Cdiff <- cover_lag1$diff - mean(cover_lag1$diff)
# 1.2 squared Cdiff centered by grand mean
Cdiff2 <- Cdiff * Cdiff


# 1.3 logged cover
# in the model that dependent variable will be log(coverage)

# 2.descriptive analysis


# 3.VIF Thus, the researcher might consider collinearity to be a problem if VIF > 5 or 10 (Fox, 2016)

# 4.regression
# 4.1.1 Model1.1 control varibles
Model1.1 <- lmer(coverage_1*100 ~ span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (1|lv2id), data=cover_lag1)
# 4.1.2 Model1.2 baseline model
Model1.2 <- lmer(coverage_1*100 ~ Cdiff + Cdiff2 + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (Cdiff | lv2id) + (Cdiff2 | lv2id) + (1|lv2id), data=cover_lag1)
# 4.1.3 Model1.3 Moderation gvaction
Model1.3 <- lmer(coverage_1*100 ~ Cdiff + Cdiff2 +gv_action + Cdiff*gv_action + Cdiff2*gv_action + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (Cdiff | lv2id) + (Cdiff2 | lv2id) + (1|lv2id), data=cover_lag1)
# 4.1.4 Model1.4 Moderation c_hetro
Model1.4 <- lmer(coverage_1*100 ~ Cdiff + Cdiff2 + c_hetro + Cdiff*c_hetro + Cdiff2*c_hetro + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (Cdiff | lv2id) + (Cdiff2 | lv2id) + (1|lv2id), data=cover_lag1)

# 5.output and graph
stargazer(vif(lm(coverage_1*100 ~ Cdiff + Cdiff2 +span + price + payInApp + size + compatibility + contentRank + age + samepubappnum, data=cover_lag1)), title = 'VIF test',type = 'html', out='../../../fig_tables/dod_hlhV1_proto/vif_coverlag1_V1_proto.htm')
stargazer(Model1.1, Model1.2,Model1.3, Model1.4, type = 'html', out='../../../fig_tables/dod_hlhV1_proto/regression_coverlag1_V1_proto.htm')
