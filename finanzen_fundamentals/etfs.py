#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Modules
import re
import requests
import warnings
from finanzen_fundamentals.scraper import _make_soup

# Define Function to Extract ETF Data from finanzen.net
# Just past URL into Stock-String
def get_etf_info(stock, output = "dict"):
    
    # Parse User Input
    if output not in ["dict"]:
        raise ValueError("Only 'dict' supportet for now")
    
    # Load Data
    soup = _make_soup("https://www.finanzen.net/etf/" + stock)

    WKN     = soup.find("span", text="WKN:").next_sibling.strip()
    ISIN    = soup.find("span", text="ISIN:").next_sibling.strip()

    currentStockTable = soup.find("div", class_="table-responsive quotebox").table
    currentStockPrice = float(currentStockTable.tr.td.contents[0].replace(",","."))
    currentStockCurrency = currentStockTable.tr.td.span.contents[0]
    currentStockExchange = currentStockTable.find("div", class_="quotebox-time").find_next_sibling("div").next_element.strip()

    baseDataTable = soup.find("h2", text="Wichtige Stammdaten").parent
    baseDataIssuer = baseDataTable.find("div", text="Emittent").parent.a.text
    baseDataBenchmark = baseDataTable.find("div", text="Benchmark").parent.find("div", {"title": True}).text
    baseDataFondsSize = float(baseDataTable.find("div", text="Fondsgröße").parent.find("div", {"title": True}).text.replace(".","").replace(",","."))

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

    if output == "dict":
        return info

if __name__ == "__main__":
    print(get_etf_info("deka-msci-world-etf-de000etfl508"))