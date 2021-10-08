#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Import Modules
## Data Structures
import pandas as pd

## Finanzen-Fundamentals
from finanzen_fundamentals.exceptions import NoDataException
from finanzen_fundamentals.scraper import _make_soup
from finanzen_fundamentals.functions import parse_price, parse_timestamp
from finanzen_fundamentals.search import search
import finanzen_fundamentals.statics as statics


# Define Function to Extract ETF Data
def get_info(etf: str, output: str = "dataframe"):
    
    # Transform User Input to Small Letters
    etf = etf.lower()
    output = output.lower()
    
    # Check User Input
    output_allowed = ["dataframe", "dict"]
    if output not in output_allowed:
        raise ValueError("Output must be either one of: {}".format(", ".join(output_allowed)))
    
    # Load Data
    soup = _make_soup("https://www.finanzen.net/etf/" + etf)
    
    # Find WKN and ISIN
    WKN = soup.find("span", text="WKN:").next_sibling.strip()
    ISIN = soup.find("span", text="ISIN:").next_sibling.strip()
    
    # Find Current Prices
    currentStockTable = soup.find("div", class_="table-responsive quotebox").table
    currentStockPrice = float(currentStockTable.tr.td.contents[0].replace(",","."))
    currentStockCurrency = currentStockTable.tr.td.span.contents[0]
    currentStockExchange = currentStockTable.find("div", class_="quotebox-time").find_next_sibling("div").next_element.strip()
    
    # Find Fundamentals
    baseDataTable = soup.find("h2", text="Wichtige Stammdaten").parent
    baseDataIssuer = baseDataTable.find("div", text="Emittent").parent.a.text
    baseDataBenchmark = baseDataTable.find("div", text="Benchmark").parent.find("div", {"title": True}).text
    baseDataFondsSize = float(baseDataTable.find("div", text="Fondsgröße").parent.find("div", {"title": True}).text.replace(".","").replace(",","."))
    
    # Put Result into Dictionary
    info = {
        "currentStockPrice": currentStockPrice,
        "currentStockCurrency": currentStockCurrency,
        "currentStockExchange": currentStockExchange,
        "WKN": WKN,
        "ISIN": ISIN,
        "Issuer": baseDataIssuer,
        "Benchmark": baseDataBenchmark,
        "FondsSize": baseDataFondsSize
    }
    
    # Create Result
    if output == "dataframe":
        for i in info:
            list_tmp = []
            list_tmp.append(info[i])
            info[i] = list_tmp
        result = pd.DataFrame(info)
    elif output == "dict":
        result = info
        
    # Return Result
    return result


# Define Function to Get Current Price
def get_price(etf: str, exchange: str = "FSE", output: str = "dataframe"):
    
    # Transform User Input into Small Letters
    etf = etf.lower()
    exchange = exchange.upper()
    output = output.lower()
    
    # Check User Input
    if output not in ["dataframe", "dict"]:
        raise ValueError("output must either be 'dict' or 'dataframe'")
        
    # Check that Exchange is Valid
    if exchange not in statics.exchanges:
        exchanges_str = ", ".join(statics.exchanges)
        raise ValueError("'exchange' must be either one of: " + exchanges_str)
        
    # Create URL
    url = f"https://www.finanzen.net/etf/{etf}/{exchange}"
    
    # Create Soup
    soup = _make_soup(url)
    
    # Find Quotebox
    quotebox = soup.find("div", {"class": "quotebox"})
    
    # Raise Error if no Price is Available
    if quotebox is None:
        raise NoDataException("No price available")
    else:
        quotebox = quotebox.find("tr")

    # Extract Current Price
    price = quotebox.find("td").get_text()
    price_float, currency = parse_price(price)
    
    # Get Timestamp
    timestamp = quotebox.find("div", {"class": "quotebox-time"}).get_text().strip()
    timestamp = parse_timestamp(timestamp)
    
    # Create Result Dict
    result = {
        "price": price_float,
        "currency": currency,
        "timestamp": timestamp,
        "etf": etf,
        "exchange": exchange
        }
    
    # Convert to Pandas if wanted
    if output == "dataframe":
        result = pd.DataFrame([result])
    
    # Return Result
    return result
    

# Define Function to Search ETF
def search_etf(etf: str, limit: int = -1):
    
    # Get Search Result
    result = search(term=etf, category="etf", limit=limit)
    
    # Return Result
    return result