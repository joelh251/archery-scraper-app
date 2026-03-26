library(tidyerse)

ianseo <- read.csv("ianseo_results.csv")
tamlyn <- read.csv("tamlyn_results.csv")

tamlyn <- tamlyn[tamlyn$Style %in% c("B", "R", "C", "L"), ]
ianseo <- ianseo[ianseo$Style %in% c("B", "R", "C", "L"), ]

tamlyn <- tamlyn[!tamlyn$Tot. %in% c(NA, "", "DNS", "DNF", "DSQ"), ]
ianseo <- ianseo[!ianseo$Tot. %in% c(NA, "", "DNS", "DNF", "DSQ"), ]


common_cols <- intersect(colnames(tamlyn), colnames(ianseo))

total_data <- bind_rows(
  tamlyn[, common_cols],
  ianseo[, common_cols]
)

total_data <- total_data %>% distinct()

write.csv(total_data, "total_data.csv")


