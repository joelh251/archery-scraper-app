The scraper requires BeautifulSoup package (available at https://www.crummy.com/software/BeautifulSoup/).  
The scraper also requires the "ianseo_urls.xlsx" workbook.  

The scraper takes an excel sheet of urls, downloads the page as a .php, then scans for urls for data.  
Data is downloaded as a .php, then parsed into a panda dataframe.
Formatting errors are corrected differently for years before and after 2020, then saved as an excel workbook.  
Excel workbooks are then compiled as sheets into 1 book per year.  

Within the parent directory, 3 directories will be created:  
  "ianseo_pages" stores the full ianseo web pages as .php files.  
  "raw_data" stores the data source files as .php files, sub subdirectories for each year will also be created.  
  "excel_data" stores the data after it has been parsed into excel workbooks, subdirectories for each year will also be created.  
  "indoor_nationals_data" stores the final workbooks. 
  
