library(tidyverse)
library(readxl)
library(stringr)
library(purrr)
library(dplyr)

sex_pattern <- regex("[MWOGF]")
nonbinary_pattern <- regex("NE|NN|EN")
style_pattern <- regex("[CRB]")
longbow_or_ladies_pattern <- regex("[L]")
age_pattern <- regex("50|U21|U18|U16|U15|U14|Jun|J|Over")
junior_pattern <- regex("Junior|Juniors|Junior's")
is_open_pattern <- regex("HN|IS|ISA|ISS")
twenty_yards_1_names <- c("20yds", "20y", "20yds-1", "20yds - 1", "20y - 1", ".1.", "20Y-1", "20y-1", "20Yd-1")
twenty_yards_2_names <- c("20yds.1", "20y.1", "20yds-2", "20yds - 2", "20y - 2", ".2.", "20Y-2", "20y-2", "20Yd-2")
remove_cols <- c("Country Code", "Country or State Code", "Country", "&nbsp;", "Società", "NOC", "Avg", "Arrows")
portsmouth_data <- list()
wa18_data <- list()

data_dir <- "IANSEO scraper v2/results"
filepaths <- list.files(data_dir)

get_suffix <- function(filename)
{
  sub(".*_", "", filename)
}


do_the_categories <- function(row)
{
  #Throughout this function, we always coalesce instead of just grabbing a pattern match
  #This is because str_extract() returns NA if not matched instead of quietly failing
  
  #Get suffix of sheet name - this is where the category data is stored (e.g. IQCRW)
  suffix <- get_suffix(row[["Sheet"]])
  
  #Search for comps known to be mixed sex (mostly military competitions)
  if (str_detect(suffix, is_open_pattern) == TRUE)
  {
    row[["Sex"]] <- "O"
    suffix <- str_remove(suffix, is_open_pattern)
  }
  
  #Get age, the simplest logic
  row[["Age"]] <- coalesce(str_extract(suffix, age_pattern), row[["Age"]])
  suffix <- str_remove(suffix, age_pattern)
  
  #Search for styles except for longbow
  #Longbow and Ladies can both be encoded as L, very helpful
  row[["Style"]] <- coalesce(str_extract(suffix, style_pattern), row[["Style"]])
  suffix <- str_remove(suffix, style_pattern)
  
  #If other style categories not picked up, then have to logic out what L means
  if (row[["Style"]] == "")
  {
    Ls <- str_count(suffix, longbow_or_ladies_pattern)
    if (Ls == 2)#If L appears twice, then it must be longbow and ladies
    {
      row[["Style"]] <- "L"
      row[["Sex"]] <- "L"
      suffix <- str_remove(suffix, longbow_or_ladies_pattern)
    }
    #Need more logic if appears once
    if (Ls == 1)
    {
      #Check if sex has been recorded in the other normal patterns
      row[["Sex"]] <- coalesce(str_extract(suffix, sex_pattern), row[["Sex"]])
      suffix <- str_remove(suffix, sex_pattern)
      
      #Sex is not encoded otherwise and L only appears once, need manual review
      if (row[["Sex"]] == "" & !get_suffix(row[["Sheet"]]) %in% c("IQL", "IQOverL"))
      {
        print(get_suffix(row[["Sheet"]]))
      }
      #Sex is encoded otherwise, therefore L must mean longbow
      else
      {
        row[["Style"]] <- coalesce(str_extract(suffix, longbow_or_ladies_pattern), row[["Style"]])
        suffix <- str_remove(suffix, longbow_or_ladies_pattern)
      }
    }
  }
  
  #If style was captured otherwise and L is still present, must mean ladies so need to capture
  if (row[["Style"]] != "")
  {
    row[["Sex"]] <- coalesce(str_extract(suffix, longbow_or_ladies_pattern), row[["Sex"]])
    suffix <- str_remove(suffix, longbow_or_ladies_pattern)
  }
  
  #Can now check for sex normally
  row[["Sex"]] <- coalesce(str_extract(suffix, sex_pattern), row[["Sex"]])
  suffix <- str_remove(suffix, sex_pattern)
  
  if (str_detect(suffix, nonbinary_pattern) == TRUE)
  {
    row[["Sex"]] <- "NB"
    suffix <- str_remove(suffix, nonbinary_pattern)
  }
  
  #For explicitly junior comps, sometimes they don't bother encoded junior in the file name
  #Checks if junior is recorded in the competition name instead
  if (row[["Age"]] == "")
  {
    row[["Age"]] <- coalesce(str_extract(row[["Competition"]], junior_pattern), row[["Age"]])
  }
  
  #Normalise male categories (because AGB changed male to open in 2025/26)
  suffix <- get_suffix(row[["Sheet"]])
  if (str_detect(suffix, is_open_pattern) == FALSE & row[["Year"]] >= 2025 & row[["Sex"]] == "O")
  {
    row[["Sex"]] <- "M"
  }
  
  #Handle missing sex data
  if (row[["Sex"]] == "")
  {
    row[["Sex"]] <- "O"
  }
  
  #Normalise sex category names
  if (row[["Sex"]] %in% c("F", "L"))
  {
    row[["Sex"]] <- "W"
  }
  if (row[["Sex"]] == "G")
  {
    row[["Sex"]] <- "M"
  }
  
  #Normalise junior category names
  if (row[["Age"]] %in% c("Jun", "J", "Junior"))
  {
    row[["Age"]] <- "Junior"
  }

  #Random exceptions because of shitty category encoding
  if (suffix == "IQL")
  {
    row[["Sex"]] <- "O"
    row[["Style"]] <- "L"
  }
  if (suffix == "IQB")
  {
    row[["Sex"]] <- "O"
    row[["Style"]] <- "B"
  }
  if (suffix == "IQR")
  {
    row[["Sex"]] <- "O"
    row[["Style"]] <- "R"
  }
  if (suffix == "IQC")
  {
    row[["Sex"]] <- "O"
    row[["Style"]] <- "C"
  }
  if (suffix == "IQOverL")
  {
    row[["Sex"]] <- "O"
    row[["Style"]] <- "L"
  }
  return(row)
}


#calculate golds where missing
calculate_golds <- function(row)
{
  if (row[["Golds"]] %in% c(NA, ""))
  {
    row[["Golds"]] <- sum(as.numeric(row[["10"]]), as.numeric(row[["9"]]))
  }
  return(row)
}


for (j in seq_along(filepaths))
{
data_sheets <- excel_sheets(paste0(data_dir, "/", filepaths[j]))

portsmouth_data[[filepaths[j]]] <- list()
wa18_data[[filepaths[j]]] <- list()

  for (k in seq_along(data_sheets))
  {
      sheet <- read_excel(paste0(data_dir, "/", filepaths[j]), sheet = k)
      sheet <- sheet[, colMeans(is.na(sheet)) <= 0.5]
      sheet <- sheet[, !(names(sheet) %in% remove_cols)]
      sheet$Sex <- ""
      sheet$Age <- ""
      sheet$Style <- ""
      sheet[] <- lapply(sheet, as.character)
      
      colnames(sheet)[colnames(sheet) %in% twenty_yards_1_names] <- "20y-1"
      colnames(sheet)[colnames(sheet) %in% twenty_yards_2_names] <- "20y-2"
      if ("Rank" %in% colnames(sheet)) {
      colnames(sheet)[colnames(sheet) == "Rank"] <- "Pos."
      }
      if ("Name" %in% colnames(sheet)) {
      colnames(sheet)[colnames(sheet) == "Name"] <- "Athlete"
      }
      if ("H" %in% colnames(sheet)) {
      colnames(sheet)[colnames(sheet) == "H"] <- "Hits"
      }
      if ("Rank" %in% colnames(sheet)) {
      colnames(sheet)[colnames(sheet) == "Rank"] <- "Pos."
      }
      if ("Pos." %in% colnames(sheet))
      {
      sheet$Pos. <- as.character(sheet$Pos.)
      }
      else
      {
      sheet$Pos. <- "None"
      }
      
      if ("18m-1" %in% colnames(sheet))
      {
      wa18_data[[filepaths[j]]][[data_sheets[k]]] <- sheet
      }
      else
      {
      portsmouth_data[[filepaths[j]]][[data_sheets[k]]] <- sheet
      }
      
  }
}


WA18_total <- map_dfr(wa18_data, ~ bind_rows(.x, .id = "Sheet"), .id = "File")
WA18_total$Round_type <- "WA18"

portsmouth_total <- map_dfr(portsmouth_data, ~ bind_rows(.x, .id = "Sheet"), .id = "File")
portsmouth_total$Round_type <- "Single Portsmouth"


#Record category data
WA18_total <- dplyr::bind_rows(
  apply(WA18_total, 1, do_the_categories, simplify = FALSE)
)

portsmouth_total <- dplyr::bind_rows(
  apply(portsmouth_total, 1, do_the_categories, simplify = FALSE)
)

portsmouth_total <- portsmouth_total %>%
  select(-any_of(c("18m", "18m.1", "18.1", "18.2"))) %>%
  mutate(`10` = coalesce(`10`, Tens)) %>%
  filter(!Style %in% c("IQA1L", "IQA2L", "IQAFB50M")) %>%
  select(-Tens)

#Bind portsmouth and WA18 dataframes
colnames(WA18_total)[c(7, 9)] <- c("Round1", "Round2")
colnames(portsmouth_total)[c(7, 9)] <- c("Round1", "Round2")
indoors_total <- rbind(WA18_total, portsmouth_total)


indoors_total <- dplyr::bind_rows(
  apply(indoors_total, 1, calculate_golds, simplify = FALSE)
)


write.csv(indoors_total, "IANSEO scraper v2/ianseo_results.csv", row.names = FALSE)
