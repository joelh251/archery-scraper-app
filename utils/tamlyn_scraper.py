# -*- coding: utf-8 -*-
"""
Filename: tamlyn_scraper.py
Author: Joel Harris joelharris251@gmail.com
Date: 24-03-2026
Version: 1.0
Dependencies: bs4, requests, os, pandas, io, sys, pathlib
Python version: 3.14.3
License: GNU GENERAL PUBLIC LICENSE v.3

Description: 
    This script scrapes archery competition data from Tamlyn Score. 
    For each valid competition record, it will create an .csv file.

Output: 
    "results" directory containing .csv files for each valid competition.
"""

from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from io import StringIO
import sys
from pathlib import Path

#constants
BASE_URL = "https://www.tamlynscore.co.uk"
TOURNAMENTS = f"{BASE_URL}/tournaments/"
RESULTS_DIR = Path("temp/tamlyn")
ROUND_TYPES = {"Portsmouth", "WA 18m"}

session = requests.Session()


def DL_csv(csvURL, savePath, compName, year):
    """
    Download .csv file from Tamlyn Score

    Parameters
    ----------
    csvURL : str
        Url to .csv file.
    
    savePath : str
        Filepath to desired location to save .csv file.

    compName : str
        Name of competition

    year : str
        Year of competition

    Returns
    -------
    None
    """

    #Pull .csv from Tamlyn Score
    try:
        r = session.get(csvURL)
        r.raise_for_status() 
    except requests.exceptions.HTTPError:
        return False

    if not r.text.strip():
        return False
    
    if "<html" in r.text.lower():
        return False

    #Filter out bad lines and rounds that aren't Single Portsmouth or WA18
    df = pd.read_csv(StringIO(r.text), on_bad_lines='skip', header = None)
    mask = df.iloc[:, 0].isin(ROUND_TYPES)
    df   = df.loc[mask]

    #Ensure df has values
    if df.empty:
        return False

    #Add competition name and year to df
    df.insert(0, "Competition", compName)
    df.insert(0, "Year", year)

    #Save df as .csv
    df.to_csv(savePath, index=False)
    
    return True



class TamlynScraper():

    def __init__(self):
        os.makedirs(RESULTS_DIR, exist_ok=True)

        #Grab the webpage listing all the competition names
        r = session.get(TOURNAMENTS)
        page = r.content

        #Parse page using bs4
        soup = BeautifulSoup(page, 'html.parser')
        divs = soup.find_all("div", class_ = "col3")
        div = divs[1]
        self.totalUrls = len(div.find_all("a", href = True))

        #Find all competition names and years
        self.all_years = div.find_all("div", class_ = "year-accordion")
        self.all_comps = div.find_all("ul", class_ = "link-list")

        self.progress = 0


    def scrape_tamlyn(self):

        for comp, years in zip(self.all_comps, self.all_years):
            counter = 1
            year = years.find("h4", class_ = "year-accordion__header").get_text(strip = True)
            hrefs = comp.find_all("a", href = True)
            links = [a["href"] for a in hrefs]
            names = ["".join(a.find_all(string=True, recursive=False)).strip() for a in hrefs]
            for link, name in zip(links, names):
                #Tamlyn Score has a very consistent data structure (take notes, Ianseo)
                #Whacking a standard url suffix to the competition url accesses the results .csv
                csvLink = f"{BASE_URL}{link}results/by-round/csv/"
                savePath = RESULTS_DIR / f"{year}_{counter}.csv" 
                if DL_csv(csvLink, savePath, name, year):
                    counter +=1
                self.progress += 1
