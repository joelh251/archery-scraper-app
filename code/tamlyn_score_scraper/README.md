# Tamlyn Score Scraper
Scrapes single Portsmouth and WA18 competition records from Tamlyn Score (https://tamlynscore.co.uk/).

## Authorship

All code written by Joel Harris (joelharris251@gmail.com)  

## Running the Scraper

Clone the "tamlyn_score_scraper" repository.

Run the script in the terminal `python3 .\tamlyn_score_scraper\tamlyn_scraper.py`

The scraper will create a directory called "results" containing a separate .csv file for each competition. 

## How it Works

Tamlyn Score has a super consistent structure so is very simple to scrape. 

If you have the name of a competition, sandwiching that between a standard url prefix and suffix will get you a .csv of that competition's results.