# -*- coding: utf-8 -*-

# Make Imports
import re
from finanzen_fundamentals.scraper import _make_soup


# Define Function to Make General Search
def search(term: str, category: str, limit: int = -1):
    
    # Convert Arguments to Lower Case
    term = term.lower()
    category = category.lower()
    
    # Check Category Argument
    cat_allowed = ["stock", "index", "fund", "etf", "certificate", "bond", "fx"]
    if category not in cat_allowed:
        raise ValueError("Category must bei either one of: {}".format(", ".join(cat_allowed)))
    
    # Map Category Argument
    cat_map = {
        "stock": "aktien",
        "index": "indizes",
        "fund": "fonds",
        "etf": "etfs",
        "certificate": "zertifikate",
        "bond": "anleihen",
        "fx": "devisen"
        }
    category_mapped = cat_map[category]
    
    # Create Search URL
    url = f"https://www.finanzen.net/suchergebnis.asp?strSuchString={term}&strKat={category_mapped}"

    # Make Request
    soup = _make_soup(url)

    # Check for Error
    if soup.find("div", {"class": "red"}) is not None:
        if "kein Ergebnis geliefert" in soup.find("div", {"class": "red"}).get_text():
            return list()
        
    # Define Function to Extract Cell
    def _get_cell(cells, ix: int):
        result = cells[ix].get_text()
        if result == "":
            result = None
        return result

    # Extract Results from Table
    ## Get Table
    result_list = []
    table_outer_div = soup.find("div", {"class": "table-responsive"})
    table = table_outer_div.find("table", {"class": "table"})
    rows = table.find_all("tr")
    
    ## Parse Single Rows in Table
    for row in rows[1:]:
        
        ### Get Cells
        cells = row.find_all("td")
        
        ### Get Name, Short Name, and Link
        name = cells[0].get_text()
        link = cells[0].find("a")["href"]
        link = "https://www.finanzen.net" + link
        short_name = cells[0].find("a")["href"]
        short_name = re.search("/.+/(.+)$", short_name).group(1)
        
        ### Extract Special Data for Stocks
        if category == "stock":
            isin = _get_cell(cells, 1)
            wkn = _get_cell(cells, 2)
            result_list.append({"name": name, "short_name": short_name,
                                "link": link, "isin": isin, "wkn": wkn})
            
        ### Extract Special Data for Index Data
        elif category == "index":
            symbol = _get_cell(cells, 1)
            wkn = _get_cell(cells, 2)
            result_list.append({"name": name, "short_name": short_name,
                                "link": link, "symbol": symbol, "wkn": wkn})
            
        ### Extract Special Data for Funds
        elif category == "fund":
            manager = _get_cell(cells, 1)
            instrument = _get_cell(cells, 2)
            isin = _get_cell(cells, 3)
            wkn = _get_cell(cells, 4)
            result_list.append({"name": name, "short_name": short_name,
                                "link": link, "manager": manager, 
                                "instrument": instrument, "isin": isin,
                                "wkn": wkn})
            
        ### Extract Special Data for ETFs
        elif category == "etf":
            isin = _get_cell(cells, 1)
            wkn = _get_cell(cells, 2)
            result_list.append({"name": name, "short_name": short_name,
                                "link": link, "isin": isin, "wkn": wkn})
            
        ### Extract Special Data for Certificates
        elif category == "certificate":
            issuer = _get_cell(cells, 1)
            product = _get_cell(cells, 2)
            runtime = _get_cell(cells, 3)
            isin = _get_cell(cells, 4)
            wkn = _get_cell(cells, 5)
            result_list.append({"name": name, "short_name": short_name,
                                "link": link, "issuer": issuer, 
                                "product": product, "runtime": runtime, 
                                "isin": isin, "wkn": wkn})
            
        ### Extract Special Data for Bonds
        elif category == "bond":
            issuer = _get_cell(cells, 1)
            instrument = _get_cell(cells, 2)
            isin = _get_cell(cells, 3)
            wkn = _get_cell(cells, 4)
            result_list.append({"name": name, "short_name": short_name,
                               "link": link, "issuer": issuer,
                               "isin": isin, "wkn": wkn})

    # Filter Result if limit was given
    if limit > 0:
        # Decrease limit if bigger than result
        result_len = len(result_list)
        if limit > result_len:
            limit = result_len
        result_list = result_list[0:limit]
        
    # Return Results
    return result_list