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
RESULTS_DIR = Path("tamlyn_score_scraper/results")
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

    Returns
    -------
    None
    """

    try:
        r = session.get(csvURL)
        r.raise_for_status() 
    except requests.exceptions.HTTPError:
        return False

    if not r.text.strip():
        return False
    
    if "<html" in r.text.lower():
        return False

    df = pd.read_csv(StringIO(r.text), on_bad_lines='skip', header = None)
    mask = df.iloc[:, 0].isin(ROUND_TYPES)
    df   = df.loc[mask]

    if df.empty:
        return False

    df.insert(0, "Competition", compName)
    df.insert(0, "Year", year)

    df.to_csv(savePath, index=False)
    
    return True


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    r = session.get(TOURNAMENTS)
    page = r.content

    soup = BeautifulSoup(page, 'html.parser')
    divs = soup.find_all("div", class_ = "col3")
    div = divs[1]
    totalUrls = len(div.find_all("a", href = True))
    counter = 1

    all_years = div.find_all("div", class_ = "year-accordion")
    all_comps = div.find_all("ul", class_ = "link-list")

    progress = 0
    print("Working on: ")
    print(f"Checked 0 of {totalUrls} competitions")
    for comp, years in zip(all_comps, all_years):
        counter = 1
        year = years.find("h4", class_ = "year-accordion__header").get_text(strip = True)
        hrefs = comp.find_all("a", href = True)
        links = [a["href"] for a in hrefs]
        names = ["".join(a.find_all(string=True, recursive=False)).strip() for a in hrefs]
        for link, name in zip(links, names):
            sys.stdout.write("\033[2F")
            sys.stdout.write(f"\rWorking on: {name}\033[K\n")

            csvLink = f"{BASE_URL}{link}results/by-round/csv/"
            savePath = RESULTS_DIR / f"{year}_{counter}.csv" 
            if DL_csv(csvLink, savePath, name, year):
                counter +=1
            progress += 1
            sys.stdout.write(f"\rChecked {progress} of {totalUrls} competitions\033[K\n")
            sys.stdout.flush()

    print("\nComplete")


if __name__ == "__main__":
    main()