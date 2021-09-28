#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Import Modules
from finanzen_fundamentals.scraper import _make_soup


# Define Function to Extract ETF Data
def get_etf_info(etf: str, output="dict"):
    
    # Parse User Input
    if output not in ["dict"]:
        raise ValueError("Only 'dict' supportet for now")
    
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
    
    # Return Result
    if output == "dict":
        return info
