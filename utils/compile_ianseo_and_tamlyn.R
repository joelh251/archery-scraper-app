#!/usr/bin/env Rscript
library(dplyr)
library(tibble)

args <- commandArgs(trailingOnly=TRUE)
output_path <- paste0(as.character(args[1]), "/total_results.csv")

files <- list.files("temp")

cols_to_keep <- c("Year", "Competition", "Round_type",
                  "Athlete", "Round1", "X.1", "Round2",
                  "X.2", "Tot.", "Hits", "Golds", "X10",
                  "X9", "Age", "Sex", "Style", "Pos.")

data <- list()

if ("ianseo_results.csv" %in% files) {
  ianseo <- read.csv("temp/ianseo_results.csv")
  ianseo <- ianseo %>%
    filter(Style %in% c("B", "R", "C", "L")) %>%
    filter_out(`Tot.` %in% c(NA, "", "DNS", "DNF", "DSQ")) %>%
    mutate(across(everything(), as.character)) %>%
    add_column(!!!setNames(
      lapply(setdiff(cols_to_keep, colnames(ianseo)), function(x) NA),
      setdiff(cols_to_keep, colnames(ianseo))
    )) %>%
    select(all_of(cols_to_keep))

  data[["ianseo"]] <- ianseo

}

if ("alt_ianseo_results.csv" %in% files) {
  ianseo2 <- read.csv("temp/alt_ianseo_results.csv")
  ianseo2 <- ianseo2 %>%
    filter(Style %in% c("B", "R", "C", "L")) %>%
    filter_out(`Tot.` %in% c(NA, "", "DNS", "DNF", "DSQ")) %>%
    mutate(across(everything(), as.character)) %>%
    add_column(!!!setNames(
      lapply(setdiff(cols_to_keep, colnames(ianseo2)), function(x) NA),
      setdiff(cols_to_keep, colnames(ianseo2))
    )) %>%
    select(all_of(cols_to_keep))

  data[["ianseo2"]] <- ianseo2

}

if ("tamlyn_results.csv" %in% files) {
  tamlyn <- read.csv("temp/tamlyn_results.csv")
  tamlyn <- tamlyn %>%
    filter(Style %in% c("B", "R", "C", "L")) %>%
    filter_out(`Tot.` %in% c(NA, "", "DNS", "DNF", "DSQ")) %>%
    mutate(across(everything(), as.character))

  #Fixing misformatted results
  rows_to_fix <- which(!is.na(tamlyn$Hits) &
                         is.na(tamlyn$X10) &
                         tamlyn$Round_type == "WA18" &
                         (grepl("\\D", tamlyn$Round1) | grepl("^\\s*$", tamlyn$Round1))
  )


  tamlyn$X10[rows_to_fix] <- tamlyn$Golds[rows_to_fix]
  tamlyn$Golds[rows_to_fix] <- NA
  tamlyn$Age[rows_to_fix] <- tamlyn$Round1[rows_to_fix]
  tamlyn$Round1[rows_to_fix] <- tamlyn$Round2[rows_to_fix]
  tamlyn$Round2[rows_to_fix] <- tamlyn$`Tot.`[rows_to_fix]
  tamlyn$`Tot.`[rows_to_fix] <- tamlyn$Hits[rows_to_fix]
  tamlyn$Hits[rows_to_fix] <- NA

  tamlyn <- tamlyn %>%
    add_column(!!!setNames(
      lapply(setdiff(cols_to_keep, colnames(tamlyn)), function(x) NA),
      setdiff(cols_to_keep, colnames(tamlyn))
    )) %>%
    select(all_of(cols_to_keep))

  data[["tamlyn"]] <- tamlyn

}

total_data <- do.call(rbind, data)
rownames(total_data) <- NULL
total_data <- total_data %>% distinct()

total_data <- total_data %>%
    mutate(Style = recode(Style,
        "C" = "Compound",
        "B" = "Barebow",
        "L" = "Longbow",
        "R" = "Recurve"
    )) %>%
 mutate(Age = recode(Age,
        "Over" = "50+",
        "50" = "50+"
    ))

total_data <- subset(total_data, `Tot.` != 0)
write.csv(total_data, output_path, row.names = FALSE)
unlink("temp", recursive=TRUE)
