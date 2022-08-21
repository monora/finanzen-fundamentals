# -*- coding: utf-8 -*-

# Make Imports
import re
from finanzen_fundamentals.scraper import _make_soup
from typing import Iterable, Dict, Any


# Define Function to Make General Search
def search(term: str, category: str, limit: int = -1)->list[dict]:
    # Convert Arguments to Lower Case
    term = term.lower()
    page = 1
    category_mapped = _map_category(category)
    result_list = []
    while True:
        # Create Search URL
        url = f"https://www.finanzen.net/suchergebnis.asp?intpagenr={page}&strSuchString={term}&strKat={category_mapped}"
        rows = _fetch_table(url)
        if not rows:
            break
        else:
            page += 1
        for row in rows[1:]:
            result_row = parse_row(category, row)
            result_list.append(result_row)
            # Filter Result if limit was given
            if limit > 0 and len(result_list) >= limit:
                return result_list  
    # Return Results
    return result_list


def parse_row(category: str, row)->Dict[str, Any]:
    "Parse Single Rows in Table"
    ### Get Cells
    cells = row.find_all("td")
    
    ### Get Name, Short Name, and Link
    name = cells[0].get_text()
    link = cells[0].find("a")["href"]
    link = "https://www.finanzen.net" + link
    short_name = cells[0].find("a")["href"]
    short_name = re.search("/.+/(.+)$", short_name).group(1)
    
    ### Extract Stock Data
    if category == "stock":
        isin = _get_cell(cells, 1)
        wkn = _get_cell(cells, 2)
        return {"Name": name, "Stock": short_name,
                "Link": link, "ISIN": isin, "WKN": wkn}
        
    ### Extract Index Data
    elif category == "index":
        symbol = _get_cell(cells, 1)
        wkn = _get_cell(cells, 2)
        return {"Name": name, "Index": short_name,
                "Link": link, "Symbol": symbol, "WKN": wkn}
        
    ### Extract Fund Data
    elif category == "fund":
        manager = _get_cell(cells, 1)
        instrument = _get_cell(cells, 2)
        isin = _get_cell(cells, 3)
        wkn = _get_cell(cells, 4)
        return {"Name": name, "Fund": short_name,
                "Link": link, "Manager": manager, 
                "Instrument": instrument, "ISIN": isin,
                "WKN": wkn}
        
    ### Extract ETF Data
    elif category == "etf":
        isin = _get_cell(cells, 1)
        wkn = _get_cell(cells, 2)
        return {"Name": name, "ETF": short_name,
                "Link": link, "ISIN": isin, "WKN": wkn}
        
    ### Extract Certificate Data
    elif category == "certificate":
        issuer = _get_cell(cells, 1)
        product = _get_cell(cells, 2)
        runtime = _get_cell(cells, 3)
        isin = _get_cell(cells, 4)
        wkn = _get_cell(cells, 5)
        return {"Name": name, "Certificate": short_name,
                "Link": link, "Issuer": issuer, 
                "Product": product, "Run Time": runtime, 
                "ISIN": isin, "WKN": wkn}
        
    ### Extract Bond Data
    elif category == "bond":
        issuer = _get_cell(cells, 1)
        instrument = _get_cell(cells, 2)
        isin = _get_cell(cells, 3)
        wkn = _get_cell(cells, 4)
        return {"Name": name, "Bond": short_name,
                "Link": link, "Issuer": issuer,
                "ISIN": isin, "WKN": wkn}

    ### Extrac Commodity Data
    elif category == "commodity":
        return {"Name": name, "Commodity": short_name,
                "Link": link}


def _get_cell(cells, ix: int):
    "Function to Extract Cell"
    result = cells[ix].get_text()
    if result == "":
        result = None
    return result


def _map_category(category: str)->str:
    "Map Category Argument"
    category = category.lower()
    # Check Category Argument
    cat_map = {
        "stock": "aktien",
        "index": "indizes",
        "fund": "fonds",
        "etf": "etfs",
        "certificate": "zertifikate",
        "bond": "anleihen",
        "fx": "devisen",
        "commodity": "Rohstoffe"
    }
    if category not in cat_map:
        raise ValueError("Category must bei either one of: {}".format(", ".join(cat_map.keys())))
    return cat_map[category]


def _fetch_table(url: str)->Iterable:
     # Make Request
    soup = _make_soup(url)

    # Check for Error
    if soup.find("div", {"class": "red"}) is not None:
        if "kein Ergebnis geliefert" in soup.find("div", {"class": "red"}).get_text():
            return list()
    
    # Extract Results from Table
    ## Get Table
    result_list = []
    table_outer_div = soup.find("div", {"class": "table-responsive"})
    if not table_outer_div:
        return list()
    table = table_outer_div.find("table", {"class": "table"})
    if not table:
        return list()
    rows = table.find_all("tr")
    return rows
