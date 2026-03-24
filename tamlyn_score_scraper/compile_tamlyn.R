#Filename: compile_tamlyn.R
#Author: Joel Harris joelharris251@gmail.com
#Date: 24-03-2026
#Version: 1.0
#Dependencies: tidyverse, readxl, stringr, purrr, dplyr
#R version: 4.5.1
#License: GNU GENERAL PUBLIC LICENSE v.3
#
#Description: 
#    Compiles n .csv files into a single file names 'tamlyn_results.csv'.
#    Standardises formatting of scores and records bowstyle, age, and sex.  
#
#
#
#Input: 
#    'results' directory containing .csv files.
#
#Output: 
#    'tamlyn_results.csv' - merged csv of all input files.


library(tidyverse)
library(readxl)
library(stringr)
library(purrr)
library(dplyr)

data_dir <- "tamlyn_score_scraper/results/"
files <- list.files(data_dir)

import_data <- function(file)
{
  df <- read.csv(paste0(data_dir, file), header = TRUE)
  df[] <- lapply(df, as.character)

  #Some Tamlyn files have different numbers of columns, this handles that
  if (ncol(df) == 12)
  {
    colnames(df) <- c("Year", "Competition", "Round_type", "Category", "Athlete", "Team", "Age", "Round1", "Round2", "Tot.", "Hits", "Golds")
    df$Age[df$Age == "Unnamed: 4"] <- ""
  }
  if (ncol(df) == 11)
  {
    colnames(df) <- c("Year", "Competition", "Round_type", "Category", "Athlete", "Team", "Round1", "Round2", "Tot.", "Hits", "Golds")
    df$Age <- ""
  }
  
  if (ncol(df) == 10)
  {
    colnames(df) <- c("Year", "Competition", "Round_type", "Category", "Athlete", "Team", "Round1", "Round2", "Tot.", "X10")
    df$Age <- ""
    df$Hits <- ""
  }
  return(df)
}

data <- bind_rows(lapply(files, import_data))

#Create blank columns
data$Sex <- NA
data$Style <- NA

#Set up constants for figuring out categories 
dict <- list2env(list(Men = "M", 
                      Women = "W",
                      Compound = "C",
                      Recurve = "R",
                      Barebow = "B",
                      Longbow = "L",
                      Portsmouth = "Single Portsmouth",
                      `WA 18m` = "WA18"), parent = emptyenv())

age_pattern <- regex("U10|U11|U12|U13|U14|U15|U16|U17|U18|U19|U20|U21|50\\+|Junior")
sex_pattern <- regex("Men|Women")
style_pattern <- regex("Compound|Barebow|Recurve|Longbow")
remove_pattern <- regex("Flatbow|Traditional")

category_finder <- function(row)
{
  if (row[["Age"]] %in% c("", NA, "Novice"))
  {
    row[["Age"]] = str_extract(row[["Category"]], age_pattern)
  }
  row[["Style"]] = str_extract(row[["Category"]], style_pattern)
  row[["Sex"]] = str_extract(row[["Category"]], sex_pattern)
  
  if (str_detect(row[["Category"]], remove_pattern))
  {
    row[["Category"]] <- "remove"
  }
  
  if (!is.na(row[["Sex"]]) && exists(row[["Sex"]], envir = dict)) {
    row[["Sex"]] <- dict[[row[["Sex"]]]]
  }
  
  if (!is.na(row[["Style"]]) && exists(row[["Style"]], envir = dict)) {
    row[["Style"]] <- dict[[row[["Style"]]]]
  }
  if (!is.na(row[["Round_type"]]) && exists(row[["Round_type"]], envir = dict)) {
    row[["Round_type"]] <- dict[[row[["Round_type"]]]]
  }
  
  return(row)
}

#apply the category finder function
data <- dplyr::bind_rows(
  apply(data, 1, category_finder, simplify = FALSE)
)

#filter out incomplete records
data <- data %>%
  filter(!if_any(everything(), ~ . %in% c("DNS", "DSQ", "Retired", "remove")))

#save final dataframe
write.csv(data, "tamlyn_score_scraper/tamlyn_results.csv", row.names = FALSE)