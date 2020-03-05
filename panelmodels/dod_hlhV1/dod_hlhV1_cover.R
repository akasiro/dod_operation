rm(list = ls())
library(lme4)
library(stargazer)
library(car)
cover <- read.csv('../../../datasets/derived/reg20200206/dod_lv1lv2_cover20200221.csv')
# 1.generate varabiles
# 1.1 diff centered by grand mean (Bickel, 2007; Hox, 2002)
Cdiff <- cover$diff - mean(cover$diff)
# 1.2 squared diff centered by grand mean
Cdiff2 <- Cdiff * Cdiff
# 1.3 logged cover
# in the model that dependent variable will be log(coverage)

# 2.descriptive analysis

# 3.VIF

# 4.regression
# 4.1 Model1 control varibles
Model1 <- lmer(coverage *100 ~ span + price + payInApp + size + compatibility + contentRank + age + samepubappnum+ (1|lv2id_x), data=cover)
# 4.2 Model2 baseline model
Model2 <- lmer(coverage * 100 ~ Cdiff + Cdiff2 + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (Cdiff | lv2id_x) + (Cdiff2 | lv2id_x) + (1|lv2id_x), data=cover)
# 4.3 Model3 moderation model action_gv
Model3 <- lmer(coverage *100 ~ Cdiff + Cdiff2 + gv_action + Cdiff*gv_action + Cdiff2*gv_action + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (Cdiff | lv2id_x) + (Cdiff2 | lv2id_x) + (1|lv2id_x), data = cover)
# 4.4 Model4 moderation model c_hetro
Model4 <- lmer(coverage *100 ~ Cdiff + Cdiff2 + c_hetro + Cdiff*c_hetro + Cdiff2*c_hetro + span + price + payInApp + size + compatibility + contentRank + age + samepubappnum + (Cdiff | lv2id_x) + (Cdiff2 | lv2id_x) + (1|lv2id_x), data = cover)
# 5.output and graph
# stargazer(cover, type = 'html', title = 'Descriptive Analysis', out='../../../fig_tables/dod_hlhV1/regression_coverlag1_V1.htm')
stargazer(vif(lm(coverage * 100~ Cdiff + Cdiff2 +span + price + payInApp + size + compatibility + contentRank + age + samepubappnum, data=cover)), title = 'VIF test',type = 'html', out='../../../fig_tables/dod_hlhV1/vif_cover_V1.htm')
stargazer(Model1, Model2, Model3, Model4, type= 'html', out='../../../fig_tables/dod_hlhV1/regression_cover_V1.htm')