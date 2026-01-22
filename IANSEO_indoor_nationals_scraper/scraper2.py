from bs4 import BeautifulSoup
import re
import requests
import os
import pandas as pd


def DL_php(phpURL, savePath):
    """
    Download .php file from ianseo web url (taken from Lucas)
    """
    
    r = requests.get(phpURL)
    with open(savePath, "wb") as f:
        f.write(r.content)
    f.close()
    
    return 

def find_data_urls(filepath):
    file = open(filepath, "r")
    document = file.read()
    file.close()

    document = BeautifulSoup(document, 'html.parser')
    div = document.find(
        "div",
        class_="results-panel-head",
        string="Qualification Round"
    )
    results_panel_body = div.find_next("div", class_= "results-panel-body")

    hrefs = results_panel_body.find_all("a", href=True)
    links = [a["href"] for a in hrefs]

    pattern = re.compile(r"\.php")

    filtered_links = [item for item in links if pattern.search(item)]

    return filtered_links


def DL_data(file_path):
    global year_pattern
    global name_pattern
    urls = find_data_urls(file_path)
    year = re.search(year_pattern, urls[0]).group(1)
    directory_name = "".join(("raw_data/", year))
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    for url in urls:
        url = "".join(("https://www.ianseo.net", url))
        name = re.search(name_pattern, url).group(1)
        save_path = "".join((directory_name, "/Indoor_Nationals_", year, "_", name, ".php"))
        DL_php(url, save_path)
    
    return 



def Parse_html_to_excel(filepath):
    global year_pattern
    global name
    year = re.search(year_pattern, filepath).group(1)
    name = re.search(name_pattern, filepath).group(1)
    save_path = "".join(("excel_data/", year, "/", name, ".xlsx"))
    with open(filepath, "r", encoding="utf-8") as file:
        document = file.read()
    
    directory_name = "".join(("excel_data/", year))
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    soup = BeautifulSoup(document, "html.parser")
    
    div = soup.find("div", id="Accordion")
    if div is None:
        div = soup.find("div", class_ = "container-table100")
        
    table = div.find("table")
    if table is None:
        raise ValueError("No table found inside the 'Accordion' div.")
    
    header_row = table.find("tr")
    if header_row is None:
        raise ValueError("No header row <tr> found in the table.")
    
    list_header = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
    max_cols = len(list_header)
    
    data_rows = table.find_all("tr")[1:]
    data = []

    for row in data_rows:
        cells = [cell.get_text(strip=True).replace("\xa0", "") for cell in row.find_all(["td", "th"])]
        cells = [c for c in cells if c != ""]
        
        if cells:
            if len(cells) > max_cols:
                max_cols = len(cells)
            data.append(cells)
    
    if len(list_header) < max_cols:
        list_header += [""] * (max_cols - len(list_header))
    
    normalized_data = []
    for row in data:
        if len(row) < max_cols:
            row += [""] * (max_cols - len(row))
        normalized_data.append(row)
    
    df = pd.DataFrame(data=normalized_data, columns=list_header)
    df = df.loc[:, (df != "").any(axis=0)]

    if int(year) < 2020:
        df = df.iloc[:, :11]
        columns_list = list(df.columns)
        df.columns = [columns_list[0], columns_list[1], 
        columns_list[2], columns_list[3], 
        columns_list[4], "X.1", columns_list[5], "X.2", 
        columns_list[6], columns_list[7], columns_list[8]]
    if int(year) > 2019:
        df.columns = df.iloc[0]
        df = df.iloc[1::3].reset_index(drop=True)
        temp = [element.strip().split("/") for element in df["18m-1"].tolist()]

        df["18m-1"] = [t[0] if len(t) > 0 else "" for t in temp]
        position = df.columns.get_loc("18m-1")
        df.insert(position + 1, "X.1", [t[1] if len(t) > 1 else "" for t in temp])

        temp = [element.strip().split("/") for element in df["18m-2"].tolist()]
        df["18m-2"] = [t[0] if len(t) > 0 else "" for t in temp]
        position = df.columns.get_loc("18m-2")
        df.insert(position + 1, "X.2", [t[1] if len(t) > 1 else "" for t in temp])

    df.to_excel(save_path)
    
    return df


year_pattern = re.compile(r"/(\d{4})/")
name_pattern = re.compile(r"/([^/]+)\.[^/]+$")

urls = pd.read_excel("ianseo_urls.xlsx", header=None)
urls = urls.iloc[:, 0]

directory_name = "ianseo_pages"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

directory_name = "ianseo_pages"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

directory_name = "raw_data"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

directory_name = "excel_data"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

directory_name = "indoor_nationals_data"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

counter = 1
for url in urls:
    path = ("ianseo_pages\\page", str(counter), ".php")
    save_path = "".join(path)
    DL_php(url, save_path)
    DL_data(save_path)
    counter += 1

for root, dirs, files in os.walk("raw_data"):
    for file in files:
        full_path = os.path.join(root, file).replace("\\", "/")
        Parse_html_to_excel(full_path)

parent_dir = "excel_data"

with os.scandir(parent_dir) as entries:
    directories = [entry.name for entry in entries if entry.is_dir()]

for directory in directories:
    folder_path = "/".join(("excel_data", directory))
    with os.scandir(folder_path) as entries:
        files = [entry.name for entry in entries if entry.is_file()]
        with pd.ExcelWriter("".join(("indoor_nationals_data/indoor_nationals_", directory, ".xlsx"))) as writer:
            for file in files:
                file_path = "/".join((folder_path, file))
                df = pd.read_excel(file_path)
                sheet_name = file.replace(".xlsx", "").replace("Indoor_Nationals_", "")
                df.to_excel(writer, sheet_name=sheet_name, index=False)      