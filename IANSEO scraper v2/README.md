# IANSEO scraper v2

This script scrapes individual qualifier data from the Ianseo website (https://www.ianseo.net/) and saves it as an excel file.  
The scraper works for any WA18 or single Portsmouth competition where individual qualifiers are stored as separate files.

## Authorship

All code written by Joel Harris (joelharris251@gmail.com)  
Inspired by Lucas Low's original IANSEO scraper


## Features
Scrapes all individual qualifier data for any WA18 or single Portsmouth competition on IANSEO.  
Almost no hardcoded aspects - works on all webpage structures and filenames.  
Saves each year of a competition as a separate Excel worksheet.  
Works for all IANSEO file formats.  
Provides progress updates while the scraper runs.  


## Running the scraper

Download the "IANSEO scraper v2" directory.  

The input for the scraper is a "urls" directory of Excel sheets.  
Each Excel sheet should contain a single column of urls for each year a competition has run.  
Each competion should be stored a separate Excel sheet formatted as "competitionName_urls.xlsx".

The scraper requires BeautifulSoup package (https://www.crummy.com/software/BeautifulSoup/).  
 
Run in the terminal using ```python3 .\ianseo_scraper.py```  

Within the parent directory, 3 temporary directories will be created:  
- "ianseo_pages" stores the full ianseo web pages as .php files.  
- "raw_data" stores the data source files as .php files, sub subdirectories for each year will also be created.  
- "excel_data" stores the data after it has been parsed into excel workbooks, subdirectories for each year will also be created.  

These temporary directories will be automatically deleted once the scraper is complete.  

The scraper will output a "results" directory containing subdirectories for each competition.  
Each subdirectory will contain an Excel workbook for each year with sheets for each category in the competition.

## How it works 

The scraper takes an excel sheet of urls, downloads the page as a .php, then scans for urls for data.  

Data is downloaded as a .php, then parsed into a panda dataframe.

Formatting errors are corrected differently for years before and after 2021 due to a change in IANSEO's formatting, then saved as an excel workbook.

Excel workbooks are then compiled as sheets into 1 workbook per year.  
Each sheet will give the year and category. 

Full documentation is available in "ianseo_scraper.py".


