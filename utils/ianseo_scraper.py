# -*- coding: utf-8 -*-
"""
Filename: ianseo_scraper.py
Author: Joel Harris joelharris251@gmail.com
Date: 22-01-2026
Version: 2.0
Dependencies: bs4, re, requests, os, pandas, shutil, sys, pathlib
Python version: 3.11.9
License: GNU GENERAL PUBLIC LICENSE v.3

Description: 
    This script scrapes archery competition data from ianseo. 
    For each url supplied, it will create an excel workbook.

Temporary files: 
    "excel_data" directory will be created and removed once the scraper has finished. 

Input: 
    "urls.xlsx" sheet containing urls to ianseo pages.

Output: 
    "results" directory containing multi-sheet excel workbooks for each input url.

Modification history:
    22-01-2026: 
        Created a basic version of the scraper which only worked on data from the Archery GB Indoor Nationals.
    28-01-2026: 
        Generalised the scraper to work on any Ianseo page for a WA18 or single Portsmouth competition which stores each category as a separate .php file. 
        Removed most hardcoded names and numbers to improve generalisability.
        Added documentation for the code
        Added a progress tracker
        Improved overall efficiency.
    01-02-2026:
        Changed parse_html_to_excel() to record competition name and year as columns in each sheet
    03-02-2026:
        Improved handling of broken urls
    24-03-2026:
        Improved speed
        Reduced generation of temporary files
        Changed data saving system - each url saved to an excel sheet with the competition name and year
"""

from bs4 import BeautifulSoup
import re
import requests
import os
import pandas as pd
import shutil
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal

#define constants
session = requests.Session()

year_pattern = re.compile(r"/(\d{4})/")
name_pattern = re.compile(r"/([^/]+)\.[^/]+$")
php_pattern = re.compile(r"\.php")
forbidden_chars = re.compile(r'[\\/:*?"<>|\x00]')


def get_comp_name(competition_page):
    """
    Get competition name from a given Ianseo page and sanitises it (removes forbidden characters). 

    Parameters
    ----------
    competition_page : str
        String containing html of an Ianseo webpage

    Returns
    -------
    competition_name : str
        Sanitised competition name
    """
        
    #Parse document with bs4 to make navigation easier
    soup = BeautifulSoup(competition_page, 'html.parser')

    #It's Ianseo so of course the competition name is saved in 2 different ways
    center = soup.select_one(".results-header-center")
    if center is not None:
        raw_name = center.find("div").get_text(strip=True)
    else:
        header = soup.find("table", id="TourHeader")
        th = header.find("th") if header else None
        raw_name = th.get_text(separator="\n", strip=True).split("\n")[0]

    #Sanitise compeition name
    competition_name = raw_name.replace(" ", "_")
    competition_name = re.sub(forbidden_chars, "_", competition_name)

    return competition_name

def find_data_urls(competition_page):
    """
    Searches for urls to data for a given Ianseo webpage.

    Parameters
    ----------
    competition_page : str
        String containing html of a given Ianseo webpage.

    Returns
    -------
    full_links : list
        List of urls to data for a given Ianseo webpage.
    """

    soup = BeautifulSoup(competition_page, 'html.parser')
    div = soup.find("div",class_="results-panel-head",string="Qualification Round") #Data links are always stored in the "Qualification Round" div
    
    #Competitions may have team scores and individual scores. We are only interested in the individual scores.
    results_panel_body = div.find_next("div", class_= "results-panel-body") #Individual scores are always stored in the first "results-panel-body" div

    hrefs = results_panel_body.find_all("a", href=True) #Looking for all links (hrefs) in the "results-panel-body"
    links = [a["href"] for a in hrefs] #Extracting the actual links as a list of strings

    #Filter for links which contain ".php" as only these link to the data
    filtered_links = [item for item in links if php_pattern.search(item)]

    #Filter out broken urls which contain whitespace
    filtered_links = [s for s in filtered_links if not any(c.isspace() for c in s)]

    #Add standard url prefix
    full_links = [f"https://www.ianseo.net{link}" for link in filtered_links]

    return full_links


def Parse_html_to_excel(data_page, url, competition_name):
    """
    Parses ianseo competition data into a pandas dataframe, then saves it as an excel sheet in the "excel_data" directory.

    Parameters
    ----------
    data_page : str
        String containing html of a given Ianseo data webpage.
    
    url : str
        Url of Ianseo data webpage

    competition_name : str
        Name of competition

    Returns
    -------
    None
    """
    #TODO: Add ability to process data when all categories are stored on a single sheet
    
    global year_pattern #Regex compiled externally for better efficiency
    global name_pattern #Regex compiled externally for better efficiency

    #Identify year and name of competition
    year = re.search(year_pattern, url).group(1)
    name = re.search(name_pattern, url).group(1)

    save_path = Path("temp/ianseo/excel_data") / f"{name}.xlsx"

    #Use bs4 to parse html to make navigating the document easier
    soup = BeautifulSoup(data_page, "html.parser")
    div = soup.find("div", id="Accordion")
    if div is None:
        div = soup.find("div", class_ = "container-table100")#Different years encode files slightly differently because why not
    
    #Search for data table
    table = div.find("table")
    if table is None:
        raise ValueError("No table found inside the 'Accordion' div.")
    
    header_row = table.find("tr")
    if header_row is None:
        raise ValueError("No header row <tr> found in the table.")
    
    #Look for headers under different encoding options (because ianseo)
    list_header = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
    max_cols = len(list_header)
    
    data_rows = table.find_all("tr")[1:]
    data = []

    for row in data_rows:
        cells = [cell.get_text(strip=True).replace("\xa0", "") for cell in row.find_all(["td", "th"])] #Encode blank cells more sensibly
        cells = [c for c in cells if c != ""] #Remove blank cells
        
        #Increase size of data if there are more cells than columns
        if cells:
            if len(cells) > max_cols:
                max_cols = len(cells)
            data.append(cells)
    
    #Add blank header names if there is more columns than headers
    if len(list_header) < max_cols:
        list_header += [""] * (max_cols - len(list_header))
    
    #Add blank cells to rows where data may be missing (or else pandas throws a hissyfit)
    normalized_data = []
    for row in data:
        if len(row) < max_cols:
            row += [""] * (max_cols - len(row))
        normalized_data.append(row)
    
    df = pd.DataFrame(data=normalized_data, columns=list_header) #Store data as pandas dataframe
    df = df.loc[:, (df != "").any(axis=0)] #Remove blank columns and rows

    #Ianseo changed their file encoding in 2021 to be extra annoying.
    #Headers before 2021 are defined once, but the headers are misaligned with the data
    #Data is stored in a relatively normal way, thank god. 
    if int(year) < 2021:
        df = df.iloc[:, :11] #Only the first 11 columns matter.
        columns_list = list(df.columns)

        #Once again, Ianseo is unhelpful. They vary between storing location data as 1 or 2 columns, and the names of those columns vary.
        if "Country Code" in df.columns and "Country" in df.columns:
            data_start_idx = df.columns.get_loc("Country") + 1
        elif "Country or State Code" in df.columns:
            data_start_idx = df.columns.get_loc("Country or State Code") + 1
        elif "Code" in df.columns:
            data_start_idx = df.columns.get_loc("Code") + 1
        elif "Country" in df.columns:
            data_start_idx = df.columns.get_loc("Country") + 1
        else:
            raise ValueError("Expected country columns not found")
        
        #The columns are misaligned with the data because of course they are. Adding columns to store the number of 10s.
        columns_list.insert(data_start_idx + 1, "X.1")
        columns_list.insert(data_start_idx + 3, "X.2")

        #To quote the great Lucas Low, "ianseo is a bitch". Ianseo will add some blank columns for no reason that fuck things up.
        df.columns = columns_list[0:11]
    
    #Ianseo changed their file encoding in 2021 to be extra annoying. Headers are repeatedly redefined in the document.
    #The real header is in the first column. Afer that, data is stored in every third column.
    #Also, Ianseo changed to store the number of 10s and scores in the same column, i.e. "score/no.10s". This must be dealt with.
    if int(year) > 2020:
        df.columns = df.iloc[0]
        df = df.iloc[1::3].reset_index(drop=True) #Taking every third row.

        if "Country Code" in df.columns and "Country" in df.columns:
            data_start_idx = df.columns.get_loc("Country") + 1
        elif "Country or State Code" in df.columns:
            data_start_idx = df.columns.get_loc("Country or State Code") + 1
        elif "Code" in df.columns:
            data_start_idx = df.columns.get_loc("Code") + 1
        elif "Country" in df.columns:
            data_start_idx = df.columns.get_loc("Country") + 1
        else:
            raise ValueError("Expected country columns not found")

        # First column split
        temp = [str(element).strip().split("/") for element in df.iloc[:, data_start_idx]] #split column and store as a nested list, i.e. [[score, 10s], [score, 10s]]

        df.iloc[:, data_start_idx] = [t[0] if len(t) > 0 else "" for t in temp] #store score in correct column if it exists.
        df.insert(data_start_idx + 1, "X.1", [t[1] if len(t) > 1 else "" for t in temp]) #store no. 10s in correct column if they exist. 

        # Second column split - same logic as above
        temp = [str(element).strip().split("/")for element in df.iloc[:, data_start_idx + 2]]

        df.iloc[:, data_start_idx + 2] = [t[0] if len(t) > 0 else "" for t in temp]
        df.insert(data_start_idx + 3,"X.2",[t[1] if len(t) > 1 else "" for t in temp])
    
    #Save competition name and year to columns

    df.insert(0, "Competition", competition_name)
    df.insert(0, "Year", year)

    #Save extracted data as an excel sheet in "excel_data" directory.
    df = df.reset_index(drop=True)
    df.to_excel(save_path, index=False)
    
    return


def compile_excel_sheets(save_directory, competition_name, year):
    """
    Compile all excel sheets in a given directory into a single multi-sheet workbook named after the competition and year.

    Parameters
    ----------
    save_directory : str
        Path to desired directory to save compiled data.
    
    competition_name : str
        Name of competition
    
    year : str
        Year of competition

    Returns
    -------
    None
    """

    save_directory = Path(save_directory)

    file_name = f"{competition_name[:26]}_{year}.xlsx" #Excel file names have a 31 character limit

    files = os.listdir(save_directory)

    if file_name in files:
        file_name = "1" + file_name[1:]

    compiled_data = save_directory / file_name 
    #print(f"{competition_name[:26]}_{year}.xlsx")
    directory = Path("temp/ianseo/excel_data") #Location of files to compile

    with pd.ExcelWriter(compiled_data) as writer:

        for file in directory.iterdir():
            sheet = pd.read_excel(file)
            sheet_name = file.stem
            sheet.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return


def DL_competition(url):
    """
    Creates a single multi-sheet excel workbook of all the competition records of a given Ianseo page.

    Stores Ianseo page as a variable in RAM instead of downloading, grabs competion name, year, and data urls. 
    Parses data from data urls into Excel sheets in "excel_data" directory, then compiles data into "results" directory.
    Deletes "excel_data" directory after compiling.

    Parameters
    ----------
    url : str
        Url to desired Ianseo page

    Returns
    -------
    None
    """

    #Raise webpage for a given Ianseo url
    response = session.get(url)
    response.raise_for_status()
    competition_page = response.text

    competition_name = get_comp_name(competition_page)

    data_urls = find_data_urls(competition_page)

    os.makedirs("temp/ianseo/excel_data", exist_ok=True)

    if data_urls:
        for url in data_urls:
            response = session.get(url)
            year = re.search(year_pattern, url).group(1)
            response.raise_for_status()
            data_page = response.text
            Parse_html_to_excel(data_page, url, competition_name)
    
    del data_urls

    if any(Path("temp/ianseo/excel_data").iterdir()):
        compile_excel_sheets("temp/ianseo/", competition_name, year)
    
    shutil.rmtree("temp/ianseo/excel_data")

    return


class IanseoScraper(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(int)

    def __init__(self, urls, parent=None):
        super(IanseoScraper, self).__init__(parent)
        self.urls = urls

    def run(self):
        i = 0
        self.progress.emit(i)
        self.totalUrls = len(self.urls)
        for url in self.urls:
            DL_competition(url)
            i += 1
            self.progress.emit(i)

        
