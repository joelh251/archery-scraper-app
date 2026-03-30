library(tidyverse)

ianseo <- read.csv("data_compiler/ianseo_results.csv")
ianseo2 <- read.csv("data_compiler/extra_ianseo_results.csv")
tamlyn <- read.csv("data_compiler/tamlyn_results.csv")

tamlyn <- tamlyn[tamlyn$Style %in% c("B", "R", "C", "L"), ]
ianseo <- ianseo[ianseo$Style %in% c("B", "R", "C", "L"), ]
ianseo2 <- ianseo2[ianseo2$Style %in% c("B", "R", "C", "L"), ]

tamlyn <- tamlyn[!tamlyn$Tot. %in% c(NA, "", "DNS", "DNF", "DSQ"), ]
ianseo <- ianseo[!ianseo$Tot. %in% c(NA, "", "DNS", "DNF", "DSQ"), ]
ianseo2 <- ianseo2[!ianseo2$Tot. %in% c(NA, "", "DNS", "DNF", "DSQ"), ]

colnames(tamlyn)
colnames(ianseo)
colnames(ianseo2)

common_cols <- intersect(colnames(tamlyn), colnames(ianseo))

tamlyn <- tamlyn %>%
  mutate(across(everything(), as.character))

ianseo <- ianseo %>%
  mutate(across(everything(), as.character))

ianseo2 <- ianseo2 %>%
  mutate(across(everything(), as.character))

total_data <- bind_rows(
  tamlyn[, common_cols],
  ianseo[, common_cols],
  ianseo2[, common_cols]
)

total_data <- total_data %>% distinct()

write.csv(total_data, "total_data.csv")