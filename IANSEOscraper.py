# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 23:26:21 2025

@author: Lucas Low ll6115@ic.ac.uk
"""

import numpy as np
import os
import pandas as pd
import requests

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
"""Functions"""
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
"""Functions to math it out OUR MATH"""
#-----------------------------------------------------------------------------#

# Functions to download and save .php file from ianseo

def ReadExcel(filePath_xlsx, sheetName):
    """Read table to be plotted, from an excel file. Output as list"""
    
    # Read excel file    
    data_df = pd.read_excel(filePath_xlsx, sheet_name = sheetName, header = 0, usecols = "A:D")

    # Convert from dataframe to list
    data_list = data_df.values.tolist()
    # By default each row is a list
    # Transpose so each column is a list
    data_list = np.array(data_list).T.tolist() 
    
    # Convert some cols to int
    for i in range(2, len(data_list), 1):
        data_list[i] = np.array(data_list[i], dtype=int)
    
    return data_list

def DL_php(phpURL, savePath):
    """
    Download .php file from ianseo web url
    """
    
    r = requests.get(phpURL)
    with open(savePath, "wb") as f:
        f.write(r.content)
    f.close()
    
    return 

def Get_phpName(phpURL):

    # Work backwards to find index of "/" just before php name
    # e.g. "https://www.ianseo.net/TourData/2025/21148/IQRM.php"
    foundName = 0
    i = len(phpURL)-1
    while(foundName == 0):
        if(phpURL[i] == "/"):
            foundName = 1
            phpName = phpURL[i+1::]
        else:
            i = i - 1
    
    return phpName

# Functions to get archer data and scores from .php file
# IMPORTANT: Due to handling of data formats being hardcoded, each function only works for it's own category!

def ParseTextAngleBrackets(text2Parse, startBracket1, startBracket2, endBracket):
    
    dataParsed = []
    
    parseSuccess = 1 # If the relevant str are found
    
    while(parseSuccess == 1):
        i_start_bracket = text2Parse.find(startBracket1)
        if(i_start_bracket == -1):
            parseSuccess = 0 # If no relevant str are found
        else:
            i_start_data = text2Parse[i_start_bracket::].find(startBracket2) + i_start_bracket + 1
            i_end_data = text2Parse[i_start_data::].find(endBracket) + i_start_data
            
            # NB. Often there is a last column. Usually it is empty. Sometime a few rows have data. So always keep it. ianseo is a bitch.
            dataParsed.append(text2Parse[i_start_data:i_end_data]) 
                
            text2Parse = text2Parse[i_end_data::] # Minimise text to parse in next iteration
            
    return dataParsed, text2Parse

def Get_qualiData_2021(dataText, compType=0):
    """ 
    Data from qualification round
    ianseo format from 2021-present
    comp:
        0 - indoors 60 arrows
        1 - outdoors 72 arrows
        2 - outdoors 90 arrows (Did not exist pre-2020)
        3 - outdoors 144 arrows (Did not exist post-2020)
    """
    
    # Get headers
    # Example header: <th class="text-right">Pos.</th>
    # 0. Find <thead> and </thead> for bounds of search area
    # 1. Find "<th class=" in <th class="text-right">
    # 2. Find </th>
    # 3. Record the data between "...>" and "</th>"
    # 4. Repeat 1-3 to find all headers/"<th class="
    
    startBracket1 = "<th class=" # str to identify preamble before relevant text
    startBracket2 = ">" # 1 element str to identify end of preamble
    endBracket = "</th>" # str to identify end of relevant text
    
    i_start_section = dataText.find("<thead>")
    i_end_section = dataText.find("</thead>")
    
    text2Parse = dataText[i_start_section:i_end_section] # Minimise searched text for speed
    
    headers, text2Parse = ParseTextAngleBrackets(text2Parse, startBracket1, startBracket2, endBracket)
    
    #--------------------
    # WARNING: Extra hardcoded!
    # Add a extra col after e.g. 18m-1 and 18m-2, to harmonise with extracted 2017 format
    if(compType == 0 or compType == 1):
        headers.insert(5, "")
        headers.insert(4, "")
    elif(compType == 2):
        headers.insert(6, "")
        headers.insert(5, "")
        headers.insert(4, "")
    elif(compType == 3):
        print("Warning: WA1440 input for post 2020 which does not exist")  
    #--------------------

    # Get data, similar process as headers
    # Example data: <td class="text-right">571</td>
    # 0. "<tr class="compressed-group" and "</tr>" define the search boundary
    # 1,2,3,4 similar to headers but "td" instead of "th"
    # 5. Repeat to find all rows/"<tr class="compressed-group"
        
    startBracket1 = "<tr class=\"compressed-group" # str to identify preamble before relevant text
    startBracket2 = ">" # 1 element str to identify end of preamble
    endBracket = "</tr>" # str to identify end of relevant text
    
    section_list, _ = ParseTextAngleBrackets(dataText, startBracket1, startBracket2, endBracket)
    
    startBracket1 = "<td class=" # str to identify preamble before relevant text
    startBracket2 = ">" # 1 element str to identify end of preamble
    endBracket = "</td>" # str to identify end of relevant text

    dataRows = []
    
    for i in range(0, len(section_list), 1):
        dataRow, _ = ParseTextAngleBrackets(section_list[i], startBracket1, startBracket2, endBracket)
        
        #--------------------
        # WARNING: Extra hardcoded!
        
        # Extract uni name - as the .php file bundles the uni with a flag and uni code
        i_start_Uni = dataRow[2].find("-&nbsp;") + len("&nbsp;") + 1
        dataRow[2] = dataRow[2][i_start_Uni::]
        
        # Turn e.g. 18m-1 and 18m-2 into two columns, to harmonise with extracted 2017 format
        if(compType == 0 or compType == 1):
            i_temp = dataRow[3].find("/")
            extraRow1 = dataRow[3][i_temp+1::]
            dataRow[3] = dataRow[3][0:i_temp]
            
            i_temp = dataRow[4].find("/")
            extraRow2 = dataRow[4][i_temp+1::]
            dataRow[4] = dataRow[4][0:i_temp]
            
            dataRow.insert(5, extraRow2)
            dataRow.insert(4, extraRow1)
        elif(compType == 2):
            i_temp = dataRow[3].find("/")
            extraRow1 = dataRow[3][i_temp+1::]
            dataRow[3] = dataRow[3][0:i_temp]
            
            i_temp = dataRow[4].find("/")
            extraRow2 = dataRow[4][i_temp+1::]
            dataRow[4] = dataRow[4][0:i_temp]
            
            i_temp = dataRow[5].find("/")
            extraRow3 = dataRow[5][i_temp+1::]
            dataRow[5] = dataRow[5][0:i_temp]
            
            dataRow.insert(6, extraRow3)
            dataRow.insert(5, extraRow2)
            dataRow.insert(4, extraRow1)
        elif(compType == 3):
            print("Warning: WA1440 input for post 2020 which does not exist")   
        #--------------------
        
        dataRows.append(dataRow)
    
    return headers, dataRows

def Get_qualiData_2017(dataText, compType=0):
    """ 
    Data from qualification round
    ianseo format from 2017-2020 
    comp:
        0 - indoors 60 arrows
        1 - outdoors 72 arrows
        2 - outdoors 90 arrows (Did not exist pre-2020)
        3 - outdoors 144 arrows (Did not exist post-2020)
    """
    
    # Get headers
    # Example header: <th class="text-right">Pos.</th>
    # 0. Find <thead> and </thead> for bounds of search area
    # 1. Find "<th class=" in <th class="text-right">
    # 2. Find </th>
    # 3. Record the data between "...>" and "</th>"
    # 4. Repeat 1-3 to find all headers/"<th class="
    
    i_start_section = dataText.find("<tr>")
    i_end_section = dataText.find("</tr>")
    
    text2Parse = dataText[i_start_section:i_end_section] # Minimise searched text for speed
    
    startBracket1 = "<div" # str to identify preamble before relevant text
    startBracket2 = ">" # 1 element str to identify end of preamble
    endBracket = "</div>" # str to identify end of relevant text
    
    headers, text2Parse = ParseTextAngleBrackets(text2Parse, startBracket1, startBracket2, endBracket)
    
    #--------------------
    # WARNING: Extra hardcoded!
    # Add a extra col after e.g. 18m-1 and 18m-2, as the data rows have two cols for each of them
    if(compType == 0 or compType == 1):
        headers.insert(6, "")
        headers.insert(5, "")
    elif(compType == 2):
        print("Warning: WA900 input for pre 2020 which does not exist")  
    elif(compType == 3):
        headers.insert(7, "")
        headers.insert(6, "")
        headers.insert(5, "")
        headers.insert(4, "")
    #--------------------

    # Get data, similar process as headers
    # Example data: <td class="text-right">571</td>
    # 0. "<tr class="compressed-group" and "</tr>" define the search boundary
    # 1,2,3,4 similar to headers but "td" instead of "th"
    # 5. Repeat to find all rows/"<tr class="compressed-group"
        
    startBracket1 = "<tr class=" # str to identify preamble before relevant text
    startBracket2 = ">" # 1 element str to identify end of preamble
    endBracket = "</tr>" # str to identify end of relevant text
    
    section_list, _ = ParseTextAngleBrackets(dataText, startBracket1, startBracket2, endBracket)
    
    startBracket1 = "<td class=" # str to identify preamble before relevant text
    startBracket2 = ">" # 1 element str to identify end of preamble
    endBracket = "</td>" # str to identify end of relevant text

    dataRows = []
    
    for i in range(0, len(section_list), 1):
        dataRow, _ = ParseTextAngleBrackets(section_list[i], startBracket1, startBracket2, endBracket)
        
        #--------------------
        # WARNING: Extra hardcoded!
        # Remove flag col, which is empty and does not have a header
        dataRow.pop(2)
        #--------------------
        
        dataRows.append(dataRow)
    
    return headers, dataRows

def SaveResults(data_header_list, data_list, filePath_saveResults, sheetName):
    """Can save multiple datasets to their own sheets in one xlsx"""
    
    # To save data in its own sheet
    data_df = pd.DataFrame(data_list, columns=data_header_list)        
    
    # To save multiple datasets to one sheet
    if os.path.isfile(filePath_saveResults) == False:
        data_df.to_excel(filePath_saveResults, sheet_name=sheetName, index=False)
    else:
        # If xlsx exists, only replace the required sheet, rather than overwiting the entire xlsx
        with pd.ExcelWriter(filePath_saveResults, mode='a', if_sheet_exists='replace') as writer:  
            data_df.to_excel(writer, sheet_name=sheetName, index=False)

    
    return
    
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
"""Main"""
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

saveResults = 0

year_list = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]


for i_year in range(0, len(year_list), 1):
    
    # Read list of ianseo urls from excel sheet
    filePath_xlsx = "C:/Users/June_/Downloads/Archery/urlList.xlsx"
    phpURL = ReadExcel(filePath_xlsx, str(year_list[i_year]))
    
    phpDirectory = "C:/Users/June_/Downloads/Archery/php files"
    
    fileDirectory_saveResults = "C:/Users/June_/Downloads/Archery"
    filePath_saveResults = "C:/Users/June_/Downloads/Archery/BUCS data " + str(year_list[i_year]) + ".xlsx"
    
    for i in range(0, len(phpURL[0]), 1):
        
        # DEBUGGING------------------------------------------------------------
        i_start_find = phpURL[0][i].find(str(year_list[i_year])) + len(str(year_list[i_year])) + 1
        i_end_find = phpURL[0][i][i_start_find::].find("/") + i_start_find 
        tourID = phpURL[0][i][i_start_find:i_end_find]
        
        if(i == 0):
            tourID_old = tourID
            confirmTourData = 0
        elif(tourID_old != tourID):
            
            if(confirmTourData == 0):
                print("1. No data at all in tournament ID:", tourID_old, " ", str(year_list[i_year]))
                
            tourID_old = tourID
            confirmTourData = 0
        # ENG DEBUGGING------------------------------------------------------------

        
        # Download the .php file from IANSEO
        phpName = Get_phpName(phpURL[0][i])
        phpPath = phpDirectory + "/" + phpName
        DL_php(phpURL[0][i], phpPath)
        
        # Details that tell use what format ianseo used
        tourName = phpURL[1][i]
        compType = phpURL[2][i]
        year = phpURL[3][i]
        
        # Read the .php file as a list, where each newline creates a new str
        with open(phpPath, 'r') as f:
            ftext = f.readlines()
        f.close()
        
        # If url does not exist then ianseo produces a webpage with 1 line: "File not found.\n"
        # Or 404 text, where the 404 is in hardcoded location
        urlValid = 1
        if(len(ftext) == 1):
            urlValid = 0
        elif(ftext[2] == "<title>404 Not Found</title>\n"):
            urlValid = 0
            
        
        if(urlValid == 1):
            
            
            
            # DEBUGGING------------------------------------------------------------
            confirmTourData = 1
            # ENG DEBUGGING------------------------------------------------------------
            
            
            # Rank, name, scores, etc. are stored in the longest str (it's all on one massive line in the .php)
            # So just isolate this str
            dataText = max(ftext, key=len)
        
            if(year <= 2020):
                qualiHeaders, qualiData = Get_qualiData_2017(dataText, compType=compType)
            elif(year >= 2021):
                qualiHeaders, qualiData = Get_qualiData_2021(dataText, compType=compType)
        
                
            if(saveResults == 1):
                
                # Failsafe: ianseo's shit formatting means some data rows may have additional columns
                qualiDataMaxLen = len(max(qualiData, key=len))
                # Add additional empty cols to both headers
                if(len(qualiHeaders) < qualiDataMaxLen):
                    cols2Add = qualiDataMaxLen - len(qualiHeaders)
                    for i in range(0, cols2Add, 1):
                        qualiHeaders.append("")
                # Add additional empty cols to other data rows
                for j in range(0, len(qualiData), 1):  
                    if(len(qualiData[j]) < qualiDataMaxLen):
                        cols2Add = qualiDataMaxLen - len(qualiData[j])
                        for i in range(0, cols2Add, 1):
                            qualiData[j].append("")
                
                
                sheetName = str(year)+tourName+phpName[0:-4]
                SaveResults(qualiHeaders, qualiData, filePath_saveResults, sheetName)
        
        
        # DEBUGGING------------------------------------------------------------
        if(confirmTourData == 0 and i == len(phpURL[0])-1):
            print("2. No data at all in tournament ID:", tourID, " ", str(year_list[i_year]))
        # ENG DEBUGGING------------------------------------------------------------