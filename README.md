# ArchersAgainstBigotry
Systems to extract and analyse archery data.

Python code to scrap IANSEO for BUCS data prepared by Lucas

R code that compiled BUCS data prepared by Joel


Tha IANSEO scraper works by downloading the IANSEO webpage (the .php file). 
For BUCS, each category in each tournament (e.g. Men Experienced Recurve, Women Experienced Longbow, etc.) is stored in it's own .php file.  The scraper will specifically download the qualifier rounds (i.e. the Portsmouth, WA1440, WA900, WA70).
It then finds the line that defines the table of tournament results, where the archer's rank, name, score at each distance, etc. are stored.
From there it uses the html brackets <></> to extract the data, and puts it into excel sheets.
