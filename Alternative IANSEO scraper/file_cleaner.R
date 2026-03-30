library(readxl)
library(openxlsx)
library(dplyr)
library(tidyr)

directory <- "Alternative IANSEO scraper/results"

files <- list.files(directory, full.names = TRUE)

column_dict <- list(
    "Year Competition ...3 ...4 ...5 .1. .2. Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 .1. .2. Total Hits Gold" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Gold"),
    "Year Competition ...3 ...4 ...5 .1. .2. Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Gold"),
    "Year Competition ...3 ...4 ...5 18m-1 18m-2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "18m-1", "18m-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 18M-1 18M-2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "18m-1", "18m-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 18m-1 18m-2 Total 10 Hits" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "Hits"),
    "Year Competition ...3 ...4 ...5 18m-1 18m-2 Total 10 X" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "X"),
    "Year Competition ...3 ...4 ...5 18m-1 18m-2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "18m-1", "18m-2", "Tot.", "Hits", "Golds"),
    "Year Competition ...3 ...4 ...5 20 yards...6 20 yards...7 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 20y-1 20y-2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 20y-1 20y-2 Total Hits 10" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "X10"),
    "Year Competition ...3 ...4 ...5 20y-1 20y-2 Total Hits 10s" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "X10"),
    "Year Competition ...3 ...4 ...5 20y-1 20y-2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition ...3 ...4 ...5 20y-1 20y-2 Total Hits Tens" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "X10"),
    "Year Competition ...3 ...4 ...5 20y - 1 20y - 2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition ...3 ...4 ...5 20y ...7 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition ...3 ...4 ...5 20y / 1 20y / 2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition ...3 ...4 ...5 20y /1 20y /2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition ...3 ...4 ...5 20y 1-10 20y 11-20 Total Hits 10s" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "X10"),
    "Year Competition ...3 ...4 ...5 20y 1-10 20y 11-20 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition ...3 ...4 ...5 20y...6 20y...7 Total Hits 10s" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "X10"),
    "Year Competition ...3 ...4 ...5 20y...6 20y...7 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition ...3 ...4 ...5 20yd-1 20yd-2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 20Yd-1 20Yd-2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 20yd -1 20yd -2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 20Yd...6 20Yd...7 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 20yds-1 20yds-2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9"),
    "Year Competition ...3 ...4 ...5 20yds - 1 20yds - 2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition Pos. Athlete Country 18m-1 18m-2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "18m-1", "18m-2", "Tot.", "X10", "X9"),
    "Year Competition Pos. Athlete Country 18m-1 18m-2 Total 10 Hits" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "18m-1", "18m-2", "Tot.", "X10", "Hits"),
    "Year Competition Pos. Athlete Country 18m 18m Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "18m-1", "18m-2", "Tot.", "X10", "X9"),
    "Year Competition Pos. Athlete Country 1st half 2nd half Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "18m-1", "18m-2", "Tot.", "X10", "X9"),
    "Year Competition Pos. Athlete Country 20y-1 20y-2 Total 10 Hits" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "20y-1", "20y-2", "Tot.", "X10", "Hits"),
    "Year Competition Pos. Athlete Country 20y-1 20y-2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition Pos. Athlete Country 20Y 20Y Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9"),
    "Year Competition Pos. Athlete Country 20yds-1 20yds-2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition Pos. Athlete Country or State Code 18m-1 18m-2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "18m-1", "18m-2", "Tot.", "X10", "X9"),
    "Year Competition Pos. Athlete Country or State Code 18m-1 18m-2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "18m-1", "18m-2", "Tot.", "Hits", "Golds"),
    "Year Competition Pos. Athlete Country or State Code 20y-1 20y-2 Total Hits Golds" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "20y-1", "20y-2", "Tot.", "Hits", "Golds"),
    "Year Competition Pos. Athlete Country or State Code 20yds-1 20yds-2 Total 10 9" = c("Year", "Competition", "Pos.", "Athlete", "Remove", "Remove2", "Country", "20y-1", "20y-2", "Tot.", "X10", "X9")
)

correct_colnames <- function(file_path)
{
    # Read column names of first sheet
    df_first <- read_excel(file_path, sheet = 1, n_max = 0)
    current_colnames <- paste(colnames(df_first), collapse = " ")
    new_colnames <- column_dict[[current_colnames]]

    # Load the full workbook
    wb <- loadWorkbook(file_path)
    sheet_names <- names(wb)

    for (sheet in sheet_names) {
        df <- read_excel(file_path, sheet = sheet)
        colnames(df) <- new_colnames
        if ("18m-1" %in% colnames(df))
        {
            df <- df %>%
                separate(`18m-1`, into = c("18m-1", "X.1"), sep = "/", convert = TRUE) %>%
                separate(`18m-2`, into = c("18m-2", "X.2"), sep = "/", convert = TRUE)
        }
        if ("20y-1" %in% colnames(df))
        {
            df <- df %>%
                separate(`20y-1`, into = c("20y-1", "X.1"), sep = "/", convert = TRUE) %>%
                separate(`20y-2`, into = c("20y-2", "X.2"), sep = "/", convert = TRUE)
        }
        
        cols_to_remove <- c("Remove", "Remove2")
        df <- df %>%
            select(-any_of(cols_to_remove))
        
        writeData(wb, sheet, df, startRow = 1, startCol = 1)
    }

    saveWorkbook(wb, file_path, overwrite = TRUE)
}

sapply(files, correct_colnames)