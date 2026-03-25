# IANSEO scraper v2

This script scrapes individual qualifier data from the Ianseo website (https://www.ianseo.net/) and saves it as an excel file.  

The scraper works for any WA18 or single Portsmouth competition where individual qualifiers are stored as separate files.

## Authorship

All code written by Joel Harris (joelharris251@gmail.com)  
Inspired by Lucas Low's original IANSEO scraper


## Features
- Scrapes all individual qualifier data for any WA18 or single Portsmouth competition on IANSEO.  
- Almost no hardcoded aspects - works on all webpage structures and filenames.  
- Saves each year of a competition as a separate Excel worksheet.  
- Works for all IANSEO file formats.  
- Provides progress updates while the scraper runs.  


## Running the scraper

Clone the "IANSEO scraper v2" directory.  

The input for the scraper is "urls.xlsx" - an Excel sheet of Ianseo urls.  

The scraper requires the BeautifulSoup package (https://www.crummy.com/software/BeautifulSoup/).  
 
Run in the terminal using ```python3 .\ianseo_scraper.py```  

1 temporary directory, "excel_data", will be created and removed as the scraper runs.  

The scraper will output a "results" directory containing an Excel workbook for each competition with sheets for each category in the competition.

## How it works 

The scraper pulls the webpage for each url supplied, searches for urls to data, parses this data into excel sheets, then compiles every sheet into a single excel workbook. 

Formatting errors are corrected differently for years before and after 2021 due to a change in IANSEO's formatting. 

Full documentation is available in "ianseo_scraper.py".


