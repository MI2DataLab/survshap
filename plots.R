library(ggplot2)
library(DALEX)
library(ggpubr)
library(latex2exp)

### Experiment 1 

# Figure 2 
brier <- read.csv("results/exp1_model_brier_score.csv")
p1 <- ggplot(brier, aes(x=time, y=brier_score, color = label, linetype=label)) +
  geom_line() + 
  theme_minimal() +
  scale_color_manual(name="", values=c("#4378bf", "#ae2c87"), labels=c("CPH", "RSF")) + 
  scale_linetype_manual(name="", values=c(1, 5), labels=c("CPH", "RSF")) +
  labs(x="Time", y="Brier score", title="Model performance") + 
  theme(legend.position = "bottom",  plot.title = element_text(hjust = 0.5), legend.title = element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) +
  geom_hline(aes(yintercept=0.25), alpha=0.3) 
p1
ggsave("plots/exp1_brier_score.pdf", device="pdf", width=1300, height=1000, units="px")


# Figure 3
alpha_other <- 0.75


example_rsf <- read.csv("results/exp1_example_rsf.csv")
p1 <- ggplot(example_rsf, aes(x = variable, y = value, color = variable_name, 
                        alpha=variable_name, size=variable_name, linetype=variable_name)) +
  geom_hline(aes(yintercept=0), alpha=0.3) + 
  geom_line() +
  theme_minimal() +
  scale_color_manual(name="Variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c"),
                     labels=c(TeX("$x^{(1)}$"), 
                              TeX("$x^{(2)}$"), 
                              TeX("$x^{(3)}$"), 
                              TeX("$x^{(4)}$"), 
                              TeX("$x^{(5)}$"))) +
  scale_alpha_manual(name="Variable", values=c(1, rep(alpha_other, 4)), 
                     labels=c(TeX("$x^{(1)}$"), 
                              TeX("$x^{(2)}$"), 
                              TeX("$x^{(3)}$"), 
                              TeX("$x^{(4)}$"), 
                              TeX("$x^{(5)}$"))) +
  scale_linetype_manual(name="Variable", values=c(1, 2, 4, 5, 6),
                        labels=c(TeX("$x^{(1)}$"), 
                                 TeX("$x^{(2)}$"), 
                                 TeX("$x^{(3)}$"), 
                                 TeX("$x^{(4)}$"), 
                                 TeX("$x^{(5)}$"))) +
  scale_size_manual(name="Variable", values=c(1, rep(0.5, 4)),
                    labels=c(TeX("$x^{(1)}$"), 
                             TeX("$x^{(2)}$"), 
                             TeX("$x^{(3)}$"), 
                             TeX("$x^{(4)}$"), 
                             TeX("$x^{(5)}$"))) + 
  scale_y_continuous(limits=c(-0.23, 0.2)) +
  labs(x=element_blank(), y="\nSurvSHAP(t) value", title="Random Survival Forest") +
  theme(plot.title = element_text(hjust = 0.5)) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))

p1b <- ggplot(example_rsf, aes(x = variable_name, y = value, fill = variable_name)) +
      geom_boxplot(size=0.25, outlier.size=0.5) + 
      theme_minimal() +
        scale_fill_manual(name="variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c")) +
        labs(x=element_blank(), y=element_blank(), title="") +
        scale_y_continuous(limits=c(-0.23, 0.2)) +
  scale_x_discrete(labels=rep("",5)) +
  theme(axis.text.y = element_blank())


example_cph <- read.csv("results/exp1_example_cph.csv")
p2 <- ggplot(example_cph, aes(x = variable, y = value, color = variable_name, 
  alpha=variable_name, size=variable_name, linetype=variable_name)) +
  geom_hline(aes(yintercept=0), alpha=0.3) + 
  geom_line() +
  theme_minimal() +
  scale_color_manual(name="variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c"),
                     labels=c(TeX("$x^{(1)}$"), 
                              TeX("$x^{(2)}$"), 
                              TeX("$x^{(3)}$"), 
                              TeX("$x^{(4)}$"), 
                              TeX("$x^{(5)}$"))) +
  scale_alpha_manual(name="variable", values=c(1, rep(alpha_other, 4)), 
                     labels=c(TeX("$x^{(1)}$"), 
                              TeX("$x^{(2)}$"), 
                              TeX("$x^{(3)}$"), 
                              TeX("$x^{(4)}$"), 
                              TeX("$x^{(5)}$"))) +
  scale_linetype_manual(name="variable", values=c(1, 2, 4, 5, 6),
                        labels=c(TeX("$x^{(1)}$"), 
                                 TeX("$x^{(2)}$"), 
                                 TeX("$x^{(3)}$"), 
                                 TeX("$x^{(4)}$"), 
                                 TeX("$x^{(5)}$"))) +
  scale_size_manual(name="variable", values=c(1, rep(0.5, 4)),
                    labels=c(TeX("$x^{(1)}$"), 
                             TeX("$x^{(2)}$"), 
                             TeX("$x^{(3)}$"), 
                             TeX("$x^{(4)}$"), 
                             TeX("$x^{(5)}$"))) + 
  scale_y_continuous(limits=c(-0.23, 0.2)) +
  labs(x=element_blank(), y="\n ", title="Cox Proportional Hazards Model") +
  theme(plot.title = element_text(hjust = 0.5))

p2b <- ggplot(example_cph, aes(x = variable_name, y = value, fill = variable_name)) +
  geom_boxplot(size=0.25, outlier.size=0.5) + 
  theme_minimal() +
  scale_fill_manual(name="variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c")) +
  labs(x=element_blank(), y=element_blank(), title="") +
  scale_y_continuous(limits=c(-0.23, 0.2)) +
  scale_x_discrete(labels=rep("",5)) +
  theme(axis.text.y = element_blank())


example_norm_rsf <- read.csv("results/exp1_example_norm_rsf.csv")
p3 <- ggplot(example_norm_rsf, aes(x = variable, y = value, color = variable_name, 
                              alpha=variable_name, size=variable_name, linetype=variable_name)) +
  geom_hline(aes(yintercept=0), alpha=0.3) + 
  geom_line() +
  theme_minimal() +
  scale_color_manual(name="variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c"),
                     labels=c(TeX("$x^{(1)}$"), 
                             TeX("$x^{(2)}$"), 
                             TeX("$x^{(3)}$"), 
                             TeX("$x^{(4)}$"), 
                             TeX("$x^{(5)}$"))) +
  scale_alpha_manual(name="variable", values=c(1, rep(alpha_other, 4)), 
                     labels=c(TeX("$x^{(1)}$"), 
                              TeX("$x^{(2)}$"), 
                              TeX("$x^{(3)}$"), 
                              TeX("$x^{(4)}$"), 
                              TeX("$x^{(5)}$"))) +
  scale_linetype_manual(name="variable", values=c(1, 2, 4, 5, 6),
                        labels=c(TeX("$x^{(1)}$"), 
                                 TeX("$x^{(2)}$"), 
                                 TeX("$x^{(3)}$"), 
                                 TeX("$x^{(4)}$"), 
                                 TeX("$x^{(5)}$"))) +
  scale_size_manual(name="variable", values=c(1, rep(0.5, 4)),
                    labels=c(TeX("$x^{(1)}$"), 
                             TeX("$x^{(2)}$"), 
                             TeX("$x^{(3)}$"), 
                             TeX("$x^{(4)}$"), 
                             TeX("$x^{(5)}$"))) + 
  scale_y_continuous(limits=c(-0.6, 0.6)) +
  labs(x="Time", y="Normalized\nSurvSHAP(t) value", title="") 

p3b <- ggplot(example_norm_rsf, aes(x = variable_name, y = value, fill = variable_name)) +
  geom_boxplot(size=0.25, outlier.size=0.5) + 
  theme_minimal() +
  scale_fill_manual(name="variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c")) +
  labs(x="", y=element_blank(), title="") +
  scale_y_continuous(limits=c(-0.6, 0.6)) +
  scale_x_discrete(labels=rep("",5)) +
  theme(axis.text.y = element_blank())



example_norm_cph <- read.csv("results/exp1_example_norm_cph.csv")
p4 <- ggplot(example_norm_cph, aes(x = variable, y = value, color = variable_name, 
                             alpha=variable_name, size=variable_name, linetype=variable_name)) +
  geom_hline(aes(yintercept=0), alpha=0.3) + 
  geom_line() +
  theme_minimal() +
  scale_color_manual(name="variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c"),
                     labels=c(TeX("$x^{(1)}$"), 
                              TeX("$x^{(2)}$"), 
                              TeX("$x^{(3)}$"), 
                              TeX("$x^{(4)}$"), 
                              TeX("$x^{(5)}$"))) +
  scale_alpha_manual(name="variable", values=c(1, rep(alpha_other, 4)), 
                     labels=c(TeX("$x^{(1)}$"), 
                              TeX("$x^{(2)}$"), 
                              TeX("$x^{(3)}$"), 
                              TeX("$x^{(4)}$"), 
                              TeX("$x^{(5)}$"))) +
  scale_linetype_manual(name="variable", values=c(1, 2, 4, 5, 6),
                        labels=c(TeX("$x^{(1)}$"), 
                                 TeX("$x^{(2)}$"), 
                                 TeX("$x^{(3)}$"), 
                                 TeX("$x^{(4)}$"), 
                                 TeX("$x^{(5)}$"))) +
  scale_size_manual(name="variable", values=c(1, rep(0.5, 4)),
                    labels=c(TeX("$x^{(1)}$"), 
                             TeX("$x^{(2)}$"), 
                             TeX("$x^{(3)}$"), 
                             TeX("$x^{(4)}$"), 
                             TeX("$x^{(5)}$"))) + 
  scale_y_continuous(limits=c(-0.6, 0.6)) +
  labs(x="Time", y="\n", title = "")


p4b <- ggplot(example_norm_cph, aes(x = variable_name, y = value, fill = variable_name)) +
  geom_boxplot(size=0.25, outlier.size=0.5) + 
  theme_minimal() +
  scale_fill_manual(name="variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c")) +
  labs(x="", y=element_blank(), title = "") +
  scale_y_continuous(limits=c(-0.6, 0.6), ) +
  scale_x_discrete(labels=rep("",5)) +
  theme(axis.text.y = element_blank())

ggarrange(p1, p1b, p2, p2b, p3, p3b, p4, p4b, 
          ncol=4, nrow=2, common.legend = TRUE, legend="bottom", widths=c(8, 2, 8, 2))
ggsave("plots/exp1_example_shap.pdf", device="pdf", width=2700, height=1200, units="px")




# Figure 4
local_accuracy <- read.csv("results/exp1_local_accuracy.csv")
p1 <- ggplot(local_accuracy, aes(x=time, y=sigma, color = label, linetype=label)) +
  geom_line() + 
  theme_minimal() +
  scale_color_manual(name="", values=c("#4378bf", "#ae2c87"), labels=c("CPH", "RSF")) + 
  scale_linetype_manual(name="", values=c(1,5), labels=c("CPH", "RSF")) +
  scale_y_continuous(limits = c(0, 3e-7), 
                     labels = c("0", 
                                TeX("$1\\cdot 10^{-7}$"), 
                                TeX("$2\\cdot 10^{-7}$"), TeX("$3\\cdot 10^{-7}$"))) +
  labs(x="Time", y=TeX("\\sigma"), title="Local accuracy measure") + 
  theme(legend.position = "bottom",  plot.title = element_text(hjust = 0.5), legend.title = element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))
p1
ggsave("plots/exp1_local_accuracy.pdf", device="pdf", width=1300, height=1000, units="px")



# Figure 5
corr <- read.csv("results/exp1_corr.csv")
p2 <- ggplot(corr, aes(x=time, y=correlation, color = label, linetype=label)) +
  geom_line() + 
  theme_minimal() +
  scale_color_manual(name="model", values=c("#4378bf", "#ae2c87"), labels=c("CPH", "RSF")) + 
  ylim(c(0.98, 1)) +
  scale_linetype_manual(name="model", values=c(1,5), labels=c("CPH", "RSF")) +
  labs(x="Time", y=TeX("$\\rho"), title="GT-Shapley") +
  theme(legend.position = "bottom", plot.title = element_text(hjust = 0.5), legend.title=element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))
p2
ggsave("plots/exp1_gt_shapley.pdf", device="pdf", width=1300, height=1000, units="px")





# Figure 6
gt_shap_rsf <- read.csv("results/exp1_gt_shap_rsf.csv")
gt_shap_cph <- read.csv("results/exp1_gt_shap_cph.csv")


p1 <- ggplot(gt_shap_rsf, aes(x = variable, y = value, color = variable_name, 
                          linetype=variable_name)) +
  geom_line(alpha=0.9) +
  theme_minimal() +
  scale_color_manual(name="Variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c")) +
  scale_linetype_manual(name="Variable", values=c(1, 2, 4, 5, 6)) +
  scale_size_manual(name="Variable", values=c(1, rep(0.5, 4))) +
  scale_y_continuous(limits=c(0, 0.1)) +
  labs(x="Time", y="Normalized RMSE",  title="Random Survival Forest") +
  theme(plot.title = element_text(hjust = 0.5)) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) 
p1

p2 <- ggplot(gt_shap_cph, aes(x = variable, y = value, color = variable_name, 
                              linetype=variable_name)) +
  geom_line(alpha=0.9) +
  theme_minimal() +
  scale_color_manual(name="variable", values=c("#f05a71", "#4378bf", "#8bdcbe", "#ae2c87", "#ffa58c")) +
  scale_linetype_manual(name="variable", values=c(1, 2, 4, 5, 6)) +
  scale_size_manual(name="variable", values=c(1, rep(0.5, 4))) +
  scale_y_continuous(limits=c(0, 0.1)) +
  labs(x="Time", y=element_blank(), title="Cox Proportional Hazards Model") +
  theme(plot.title = element_text(hjust = 0.5)) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))
p2


ggarrange(p1, p2, ncol=2, nrow=1, common.legend = TRUE, legend="bottom")
ggsave("plots/exp1_error.pdf", device="pdf", width=2700, height=800, units="px")



### Experiment 2

# Figure 7 
brier <- read.csv("results/exp2_dataset0_model_brier_score.csv")
p1 <- ggplot(brier, aes(x=time, y=brier_score, color = label, linetype=label)) +
  geom_line() + 
  theme_minimal() +
  scale_color_manual(name="model", values=c("#4378bf", "#ae2c87"), labels=c("CPH", "RSF")) + 
  scale_linetype_manual(name="model", values=c(1,5), labels=c("CPH", "RSF")) +
  labs(x="Time", y="Brier score", title="dataset0") + 
  theme(legend.position = "bottom",  plot.title = element_text(hjust = 0.5), legend.title=element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) +
  geom_hline(aes(yintercept=0.25), alpha=0.3) 
p1

brier <- read.csv("results/exp2_dataset1_model_brier_score.csv")
p2 <- ggplot(brier, aes(x=time, y=brier_score, color = label, linetype=label)) +
  geom_line() + 
  theme_minimal() +
  scale_color_manual(name="model", values=c("#4378bf", "#ae2c87"), labels=c("CPH", "RSF")) + 
  scale_linetype_manual(name="model", values=c(1,5), labels=c("CPH", "RSF")) +
  labs(x="Time", y="Brier score", title="dataset1") + 
  theme(legend.position = "bottom",  plot.title = element_text(hjust = 0.5), legend.title = element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) +
  geom_hline(aes(yintercept=0.25), alpha=0.3) 
p2


ggarrange(p1, p2, ncol=1, nrow=2, common.legend = TRUE, legend="bottom")
ggsave("plots/exp2_brier_score.pdf", device="pdf", width=1000, height=1400, units="px")



## Figure 8

local_accuracy_cph_dataset0 <- read.csv("results/exp2_local_accuracy_cph_dataset0.csv")
p1 <- ggplot(local_accuracy_cph_dataset0, aes(x=time, y=sigma, color = method, linetype= method)) +
  geom_line() + 
  theme_minimal() +
  labs(x="Time", y=TeX("\\sigma"), title="Local accuracy measure") + 
  theme(legend.position = "bottom",  plot.title = element_text(hjust = 0.5), legend.title=element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) + 
  scale_color_manual(name="method", values=c("#4378bf", "#ae2c87"), labels=c("SurvLIME", "SurvSHAP(t)")) + 
  scale_linetype_manual(name="method", values=c(1,5), labels=c("SurvLIME", "SurvSHAP(t)")) +
  labs(x="Time", y=TeX("\\sigma"), title="Local accuracy measure") 
p1




local_accuracy_rsf_dataset0 <- read.csv("results/exp2_local_accuracy_rsf_dataset0.csv")
p2 <- ggplot(local_accuracy_rsf_dataset0, aes(x=time, y=sigma, color = method, linetype= method)) +
  geom_line() + 
  theme_minimal() +
  labs(x="Time", y=TeX("\\sigma"), title="Local accuracy measure") + 
  theme(legend.position = "bottom",  plot.title = element_text(hjust = 0.5), legend.title=element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) +
  scale_color_manual(name="method", values=c("#4378bf", "#ae2c87"), labels=c("SurvLIME", "SurvSHAP(t)")) + 
  scale_linetype_manual(name="method", values=c(1,5), labels=c("SurvLIME", "SurvSHAP(t)")) +
  labs(x="Time", y=TeX("\\sigma"), title="Local accuracy measure") 
p2


ggsave("plots/exp2_local_accuracy_rsf_dataset0.pdf", device="pdf", width=1300, height=1000, units="px")



# Figure 9
importance_labels <- c("5th", "4th", "3rd", "2nd", "1st")

# dataset 0
make_factors <- function(data){
  data$importance_ranking <- factor(data$importance_ranking, levels=sort(unique(data$importance_ranking), decreasing=TRUE))
  data$variable <- factor(data$variable, levels=rev(c("x3", "x2", "x5", "x4", "x1")))
  data
}

barplot_variable_ranking_dataset0 <- function(data, title="", ytitle=""){
  ggplot(data, aes(fill=variable, y=value, x=importance_ranking)) +
    geom_bar(position="stack", stat="identity", color="white", size=0.2, width=0.8, 
             orientation="x") +
    scale_fill_manual("Variable",
      values=c("#ae2c87", "#ffa58c", "#8bdcbe", "#46BAC2", "#4378bf"),
                      limits=c("x3", "x2", "x5", "x4", "x1"), 
                      labels=c(TeX("$x^{(3)}$"), 
                               TeX("$x^{(2)}$"), 
                               TeX("$x^{(5)}$"), 
                               TeX("$x^{(4)}$"), 
                               TeX("$x^{(1)}$"))) + 
    theme_minimal() +
    scale_y_continuous(expand = c(0, 0), 
                       breaks=c(seq(0, 100, 10), 102), 
                       minor_breaks = seq(5, 105, 5)) +
    scale_x_discrete(labels = importance_labels) +
    coord_flip() +
    geom_text(aes(label = value), 
              position = position_stack(vjust = 0.5), size = 3) + 
    labs(x=ytitle, y="Number of observations", title=title) +
    theme(plot.title = element_text(hjust = 0.5), axis.title.x = element_blank()) +
    guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))
}

d0_rsf_lime <- read.csv("results/exp2_survlime_orderings_rsf_dataset0.csv")
d0_rsf_lime <- make_factors((d0_rsf_lime))
p1 <- barplot_variable_ranking_dataset0(d0_rsf_lime, ytitle="Importance ranking", title="SurvLIME")
p1

d0_rsf_shap <- read.csv("results/exp2_survshap_orderings_rsf_dataset0.csv")
d0_rsf_shap <- make_factors((d0_rsf_shap))
p2 <- barplot_variable_ranking_dataset0(d0_rsf_shap, title="SurvSHAP(t)")
p2


p <- ggarrange(p1, p2, ncol=2, nrow=1, common.legend = TRUE, legend="bottom") +
  theme(plot.margin = margin(0.1,0.2,0.1,0.1, "cm")) 
annotate_figure(p, top = text_grob("dataset0", 
                                    size = 14))
ggsave("plots/exp2_rsf_orderings_dataset0.pdf", device="pdf", width=2600, height=800, units="px")



# dataset 1

make_factors <- function(data){
  data$importance_ranking <- factor(data$importance_ranking, levels=sort(unique(data$importance_ranking), decreasing=TRUE))
  data$variable <- factor(data$variable, levels=rev(c("x2", "x5", "x1", "x3", "x4")))
  data
}


barplot_variable_ranking_dataset1 <- function(data, title="", ytitle=""){
  ggplot(data, aes(fill=variable, y=value, x=importance_ranking)) +
    geom_bar(position="stack", stat="identity", color="white", size=0.2, width=0.8, 
             orientation="x") +
    scale_fill_manual("Variable",
      values=c("#ae2c87", "#ffa58c","#8bdcbe", "#46BAC2", "#4378bf"),
                      limits=c("x2", "x5", "x1", "x3", "x4"), 
                      labels=c(TeX("$x^{(2)}$"), 
                               TeX("$x^{(5)}$"), 
                               TeX("$x^{(1)}$"), 
                               TeX("$x^{(3)}$"), 
                               TeX("$x^{(4)}$"))) + 
    theme_minimal() +
    scale_y_continuous(expand = c(0, 0), 
                       breaks=c(seq(0, 100, 10), 102), 
                       minor_breaks = seq(5, 105, 5)) +
    scale_x_discrete(labels = importance_labels) +
    coord_flip() +
    geom_text(aes(label = value), 
              position = position_stack(vjust = 0.5), size = 3) + 
    labs(x=ytitle, y="number of observations", title=title) +
    theme(plot.title = element_text(hjust = 0.5), axis.title.x = element_blank()) +
    guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))
}


d1_rsf_lime <- read.csv("results/exp2_survlime_orderings_rsf_dataset1.csv")
d1_rsf_lime <- make_factors((d1_rsf_lime))
p1 <- barplot_variable_ranking_dataset1(d1_rsf_lime, ytitle="Importance ranking", title="SurvLIME")
p1

d1_rsf_shap <- read.csv("results/exp2_survshap_orderings_rsf_dataset1.csv")
d1_rsf_shap <- make_factors((d1_rsf_shap))
p2 <- barplot_variable_ranking_dataset1(d1_rsf_shap, title="SurvSHAP(t)")
p2


p <- ggarrange(p1, p2, ncol=2, nrow=1, common.legend = TRUE, legend="bottom") +
  theme(plot.margin = margin(0.1,0.2,0.1,0.1, "cm")) 
p
annotate_figure(p, top = text_grob("dataset1", 
                                   size = 14))

ggsave("plots/exp2_rsf_orderings_dataset1.pdf", device="pdf", width=2600, height=800, units="px")



### Experiment 3

# Figure 10
brier <- read.csv("results/exp3_model_brier_score.csv")
p1 <- ggplot(brier, aes(x=time, y=brier_score, color = label, linetype=label)) +
  geom_line() + 
  theme_minimal() +
  scale_color_manual(name="model", values=c("#4378bf", "#ae2c87"), labels=c("CPH", "RSF")) + 
  scale_linetype_manual(name="model", values=c(1,5), labels=c("CPH", "RSF")) +
  labs(x="Time", y="Brier score", title="Model performance") + 
  theme(legend.position = "bottom",  plot.title = element_text(hjust = 0.5), legend.title = element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) +
  geom_hline(aes(yintercept=0.25), alpha=0.3) 
p1
ggsave("plots/exp3_brier_score.pdf", device="pdf", width=1300, height=1000, units="px")


# Figure 11
alpha_other <- 1
example_rsf <- read.csv("results/exp3_example_rsf.csv")
p1 <- ggplot(example_rsf, aes(x = variable, y = value, color = variable_name, 
                              alpha=variable_name, size=variable_name, linetype=variable_name)) +
  geom_hline(aes(yintercept=0), alpha=0.3) + 
  geom_line() +
  theme_minimal() +
  scale_color_manual(name="Variable", values=c("#4378bf", "#ffa58c", "#f05a71", "#46bac2","#371ea3", "#8bdcbe", "#ae2c87", "#160e3b")) +
  scale_alpha_manual(name="Variable", values=c(rep(alpha_other, 2), 2, rep(alpha_other, 5))) +
  scale_linetype_manual(name="Variable", values=c(2, 4, 1, 5, 6, 7, 8, 9)) +
  scale_size_manual(name="Variable", values=c(rep(0.5, 2), 1, rep(0.5, 5))) + 
  scale_y_continuous(limits=c(-0.2, 0.1)) +
  labs(x="Time", y="SurvSHAP(t) value", title="SurvSHAP(t)") +
  theme(plot.title = element_text(hjust = 0.5), legend.position = "bottom", text = element_text(size=10)) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))
p1

p1b <- ggplot(example_rsf, aes(x = variable_name, y = value, fill = variable_name)) +
  geom_boxplot(size=0.25, outlier.size=0.5) + 
  theme_minimal() +
  scale_fill_manual(name="variable", values=c("#4378bf", "#ffa58c", "#f05a71", "#46bac2","#371ea3", "#8bdcbe", "#ae2c87", "#160e3b")) +
  labs(x=element_blank(), y=element_blank(), title="") +
  scale_y_continuous(limits=c(-0.2, 0.1)) +
  scale_x_discrete(labels=rep("",8)) +
  theme(axis.text.y = element_blank(), legend.position = "none") 


example_rsf_agg <- read.csv("results/exp3_example_rsf_agg.csv")

p2 <- ggplot(example_rsf_agg, aes(x=reorder(variable_name, aggregated_change), y=aggregated_change)) + 
  geom_bar(stat="identity", fill="#4378BF", width=0.85) +
  coord_flip() +
  theme_minimal() +
  labs(x="Variable", y=TeX("Aggregated SurvSHAP(t) $\\psi$"), title="Aggregated SurvSHAP(t)") +
  scale_y_continuous(expand=c(0.0001,1), limits = c(0, 710))  +
  theme(text = element_text(size=10)) +
  scale_x_discrete(labels=c("sex", "TIL density",
                            "largest basal\ntumor diameter", "ciliary body\ninfiltration",
                            "mitotic rate\nper 1mm2", "nucleoli size", "age at diagnosis", "BAP1 mutation")) +
  theme(plot.title = element_text(hjust = 0.5), legend.position = "bottom", text = element_text(size=10)) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))


ggarrange(ggarrange(p1, p1b, ncol=2, nrow=1, widths = c(10, 2), common.legend = TRUE, 
          legend = "bottom"), p2, widths=c(6, 4), ncol=2, nrow=1)
ggsave("plots/exp3_example_1.pdf", device="pdf", width=3000, height=1000, units="px")


example_rsf <- read.csv("results/exp3_example_rsf_2.csv")
p1 <- ggplot(example_rsf, aes(x = variable, y = value, color = variable_name, 
                               linetype=variable_name)) +
  geom_hline(aes(yintercept=0), alpha=0.3) + 
  geom_line() +
  theme_minimal() +
  scale_color_manual(name="Variable", values=c("#4378bf", "#ffa58c", "#f05a71", "#46bac2","#371ea3", "#8bdcbe", "#ae2c87", "#160e3b")) +
  scale_linetype_manual(name="Variable", values=c(2, 4, 1, 5, 6, 7, 8, 9)) +
  scale_y_continuous(limits=c(-0.25, 0.15)) +
  scale_x_continuous(limits=c(0, 5800)) +
  labs(x="Time", y="SurvSHAP(t) value", title="Random Survival Forest") +
  theme(plot.title = element_text(hjust = 0.5), legend.position = "bottom", text = element_text(size=10)) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))
p1

p1b <- ggplot(example_rsf, aes(x = variable_name, y = value, fill = variable_name)) +
  geom_boxplot(size=0.25, outlier.size=0.5) + 
  theme_minimal() +
  scale_fill_manual(name="Variable", values=c("#4378bf", "#ffa58c", "#f05a71", "#46bac2","#371ea3", "#8bdcbe", "#ae2c87", "#160e3b")) +
  labs(x=element_blank(), y=element_blank(), title="") +
  scale_y_continuous(limits=c(-0.25, 0.15)) +
  scale_x_discrete(labels=rep("",8)) +
  theme(axis.text.y = element_blank(), legend.position = "none") 
p1b

example_cph <- read.csv("results/exp3_example_cph_2.csv")
example_cph <- example_cph[example_cph$variable < 5800,]
p2 <- ggplot(example_cph, aes(x = variable, y = value, color = variable_name, 
                             linetype=variable_name)) +
  geom_hline(aes(yintercept=0), alpha=0.3) + 
  geom_line() +
  theme_minimal() +
  scale_color_manual(name="Variable", values=c("#4378bf", "#ffa58c", "#f05a71", "#46bac2","#371ea3", "#8bdcbe", "#ae2c87", "#160e3b")) +
  scale_linetype_manual(name="Variable", values=c(2, 4, 1, 5, 6, 7, 8, 9)) +
  scale_y_continuous(limits=c(-0.25, 0.15)) +
  scale_x_continuous(limits=c(0, 5800)) +
  labs(x="Time", y="\n", title="Cox Proportional Hazards Model") +
  theme(plot.title = element_text(hjust = 0.5), legend.position = "bottom", text = element_text(size=10)) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5))
p2

p2b <- ggplot(example_cph, aes(x = variable_name, y = value, fill = variable_name)) +
  geom_boxplot(size=0.25, outlier.size=0.5) + 
  theme_minimal() +
  scale_fill_manual(name="variable", values=c("#4378bf", "#ffa58c", "#f05a71", "#46bac2","#371ea3", "#8bdcbe", "#ae2c87", "#160e3b")) +
  labs(x=element_blank(), y=element_blank(), title="") +
  scale_y_continuous(limits=c(-0.25, 0.15)) +
  scale_x_discrete(labels=rep("",8)) +
  theme(axis.text.y = element_blank(), legend.position = "none") 


ggarrange(p1,p1b, p2, p2b, nrow=1, common.legend = TRUE, legend="bottom", widths=c(8, 2, 8, 2)) 

ggsave("plots/exp3_example_shap_2.pdf", device="pdf", width=2600, height=900, units="px")


# Figure 13
make_factors_cph <- function(data){
  data$importance_ranking <- factor(data$importance_ranking, levels=sort(unique(data$importance_ranking), decreasing=TRUE))
  data$variable <- factor(data$variable, levels=rev(c("age at diagnosis", "nucleoli size",  "BAP1 mutation",   "mitotic rate per 1mm2",
                                                      "TIL density", "largest basal tumor diameter",  "ciliary body infiltration",  "sex")))
  data
}

plot_label_count_threshold <- 4
importance_labels <- c("8th", "7th", "6th", "5th", "4th", "3rd", "2nd", "1st")     


exp3_cph_orderings_lime <- read.csv("results/exp3_survlime_orderings_cph.csv")
exp3_cph_orderings_lime <- make_factors_cph(exp3_cph_orderings_lime)
exp3_cph_orderings_lime$value_plot <- ifelse(exp3_cph_orderings_lime$value >= plot_label_count_threshold, exp3_cph_orderings_lime$value, "")

p1 <- ggplot(exp3_cph_orderings_lime, aes(fill=variable, y=value, x=importance_ranking)) +
  geom_bar(position="stack", stat="identity", color="white", size=0.2, width=0.8, 
           orientation="x") +
  theme_minimal() +
  coord_flip() +
  scale_fill_manual("Variable", values=c("#ae2c87", "#F05A71", "#ffa58c", "#c7f5bf", "#8bdcbe",   "#46BAC2", "#4378bf", "#3d42af"),
                    limits=c("age at diagnosis", "nucleoli size",  "BAP1 mutation",   "mitotic rate per 1mm2",
                             "TIL density", "largest basal tumor diameter",  "ciliary body infiltration",  "sex")) + 
  geom_text(aes(label = value_plot), 
            position = position_stack(vjust = 0.5), size = 3) +
  labs(x="Importance ranking", y="number of observations", title="SurvLIME") +
  theme(plot.title = element_text(hjust = 0.5), axis.title.x = element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) + 
  scale_y_continuous(expand = c(0, 0), 
                     breaks=c(seq(0, 150, 10))) +
  scale_x_discrete(labels = importance_labels) 
p1




exp3_cph_orderings_shap <- read.csv("results/exp3_survshap_orderings_cph.csv")
exp3_cph_orderings_shap <- make_factors_cph(exp3_cph_orderings_shap)
exp3_cph_orderings_shap$value_plot <- ifelse(exp3_cph_orderings_shap$value >= plot_label_count_threshold, exp3_cph_orderings_shap$value, "")

p2 <- ggplot(exp3_cph_orderings_shap, aes(fill=variable, y=value, x=importance_ranking)) +
  geom_bar(position="stack", stat="identity", color="white", size=0.2, width=0.8, 
           orientation="x") +
  theme_minimal() +
  coord_flip() +
  scale_fill_manual("Variable", values=c("#ae2c87", "#F05A71", "#ffa58c", "#c7f5bf", "#8bdcbe",   "#46BAC2", "#4378bf", "#3d42af"),
                    limits=c("age at diagnosis", "nucleoli size",  "BAP1 mutation",   "mitotic rate per 1mm2",
                             "TIL density", "largest basal tumor diameter",  "ciliary body infiltration",  "sex")) + 
  geom_text(aes(label = value_plot), 
            position = position_stack(vjust = 0.5), size = 3) +
  labs(x="", y="number of observations", title="SurvSHAP(t)") +
  theme(plot.title = element_text(hjust = 0.5), axis.title.x = element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) + 
  scale_y_continuous(expand = c(0, 0), 
                     breaks=c(seq(0, 150, 10))) +
  scale_x_discrete(labels = importance_labels) 

p <- ggarrange(p1, p2, ncol=2, nrow=1, common.legend = TRUE, legend="bottom") +
  theme(plot.margin = margin(0.1,0.2,0.1,0.1, "cm")) 
annotate_figure(p, top = text_grob("Cox Proportional Hazards Model", 
                                   size = 14))

ggsave("plots/exp3_cph_orderings.pdf", device="pdf", width=2600, height=1000, units="px")






make_factors_rsf <- function(data){
  data$importance_ranking <- factor(data$importance_ranking, levels=sort(unique(data$importance_ranking), decreasing=TRUE))
  data$variable <- factor(data$variable, levels=rev(c("nucleoli size",  "BAP1 mutation",   "age at diagnosis", "mitotic rate per 1mm2",
                                                      "largest basal tumor diameter",  "ciliary body infiltration",  "TIL density",  "sex")))
  data
}

importance_labels <- c("8th", "7th", "6th", "5th", "4th", "3rd", "2nd", "1st")      
       

exp3_rsf_orderings_lime <- read.csv("results/exp3_survlime_orderings_rsf.csv")
exp3_rsf_orderings_lime <- make_factors_rsf(exp3_rsf_orderings_lime)
exp3_rsf_orderings_lime$value_plot <- ifelse(exp3_rsf_orderings_lime$value >= plot_label_count_threshold, exp3_rsf_orderings_lime$value, "")

p1 <- ggplot(exp3_rsf_orderings_lime, aes(fill=variable, y=value, x=importance_ranking)) +
  geom_bar(position="stack", stat="identity", color="white", size=0.2, width=0.8, 
           orientation="x") +
  theme_minimal() +
  coord_flip() +
  scale_fill_manual("Variable", values=c("#ae2c87", "#F05A71", "#ffa58c", "#c7f5bf", "#8bdcbe",   "#46BAC2", "#4378bf", "#3d42af"),
                    limits=c("nucleoli size",  "BAP1 mutation",   "age at diagnosis", "mitotic rate per 1mm2",
                             "largest basal tumor diameter",  "ciliary body infiltration",  "TIL density",  "sex")) + 
  geom_text(aes(label = value_plot), 
            position = position_stack(vjust = 0.5), size = 3) +
  labs(x="Importance ranking", y="number of observations", title="SurvLIME") +
  theme(plot.title = element_text(hjust = 0.5), axis.title.x = element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) + 
  scale_y_continuous(expand = c(0, 0), 
                     breaks=c(seq(0, 150, 10))) +
  scale_x_discrete(labels = importance_labels) 



exp3_rsf_orderings_shap <- read.csv("results/exp3_survshap_orderings_rsf.csv")
exp3_rsf_orderings_shap <- make_factors_rsf(exp3_rsf_orderings_shap)
exp3_rsf_orderings_shap$value_plot <- ifelse(exp3_rsf_orderings_shap$value >= plot_label_count_threshold, exp3_rsf_orderings_shap$value, "")

p2 <- ggplot(exp3_rsf_orderings_shap, aes(fill=variable, y=value, x=importance_ranking)) +
  geom_bar(position="stack", stat="identity", color="white", size=0.2, width=0.8, 
           orientation="x") +
  theme_minimal() +
  coord_flip() +
  scale_fill_manual("Variable", values=c("#ae2c87", "#F05A71", "#ffa58c", "#c7f5bf", "#8bdcbe",   "#46BAC2", "#4378bf", "#3d42af"),
                    limits=c("nucleoli size",  "BAP1 mutation",   "age at diagnosis", "mitotic rate per 1mm2",
                             "largest basal tumor diameter",  "ciliary body infiltration",  "TIL density",  "sex")) + 
  geom_text(aes(label = value_plot), 
            position = position_stack(vjust = 0.5), size = 3) +
  labs(x="", y="number of observations", title="SurvSHAP(t)") +
  theme(plot.title = element_text(hjust = 0.5), axis.title.x = element_blank()) +
  guides(colour = guide_legend(title.position = "top", title.hjust = 0.5)) + 
  scale_y_continuous(expand = c(0, 0), 
                     breaks=c(seq(0, 150, 10))) +
  scale_x_discrete(labels = importance_labels) 

p <- ggarrange(p1, p2, ncol=2, nrow=1, common.legend = TRUE, legend="bottom") +
  theme(plot.margin = margin(0.1,0.2,0.1,0.1, "cm")) 
annotate_figure(p, top = text_grob("Random Survival Forest", 
                                   size = 14))

ggsave("plots/exp3_rsf_orderings.pdf", device="pdf", width=2600, height=1000, units="px")
