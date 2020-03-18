#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re

# Import Modules
from finanzen_fundamentals.scraper import _make_soup


# Define Function to Check for Error
def _check_site(soup):
    message = soup.find("div", {"class": "special_info_box"})
    if message is not None:
        message_text = message.get_text()
        load_error = "Die gewünschte Seite konnte nicht angezeigt werden"
        if load_error in message_text:
            raise ValueError("Could not find Stock")


# Define Function to Extract GuV/Bilanz from finanzen.net
def get_fundamentals(stock: str):
    # Convert name to lowercase
    stock = stock.lower()

    # Load Data
    soup = _make_soup("https://www.finanzen.net/bilanz_guv/" + stock)

    # Check for Error
    _check_site(soup)

    # Define Function to Parse Table
    def _parse_table(soup, signaler: str):
        table_dict = {}
        table = soup.find("h2", text=re.compile(signaler)).parent
        years = [x.get_text() for x in table.find_all("th")[2:]]
        rows = table.find_all("tr")[1:]
        for row in rows:
            name = row.find("td", {"class": "font-bold"}).get_text()
            row_data = row.find_all("td")
            row_data = row_data[2:]
            row_data = [x.get_text() for x in row_data]
            row_data = [re.sub(r"\.", "", x) for x in row_data]
            row_data = [re.sub(",", ".", x) for x in row_data]
            row_data = [float(x) if x != "-" else None for x in row_data]
            table_dict[name] = dict(zip(years, row_data))
        return table_dict

    # Extract Stock Quote Info+
    try:
        quote_info = _parse_table(soup, "Die Aktie")
    except Exception:
        quote_info = None

    # Extract Key Ratios
    try:
        key_ratios = _parse_table(soup, "Unternehmenskennzahlen")
    except Exception:
        key_ratios = None

    # Extract Income Statement
    try:
        income_info = _parse_table(soup, "GuV")
    except Exception:
        income_info = None

    # Extract Balance Sheet
    try:
        balance_sheet = _parse_table(soup, "Bilanz")
    except Exception:
        balance_sheet = None

    # Extract Other Information
    try:
        other_info = _parse_table(soup, "sonstige Angaben")
    except Exception:
        other_info = None

    # Collect Fundamentals into single Directory
    fundamentals = {
        "Quotes": quote_info,
        "Key Ratios": key_ratios,
        "Income Statement": income_info,
        "Balance Sheet": balance_sheet,
        "Other": other_info
    }

    # Return Fundamentals
    return fundamentals


# Define Function to Extract Estimates
def get_estimates(stock: str):
    # Convert Stock Name to Lowercase
    stock = stock.lower()

    # Load Data
    soup = _make_soup("https://www.finanzen.net/schaetzungen/" + stock)

    # Check for Error
    _check_site(soup)

    # Parse Table containing Yearly Estimates
    table_dict = {}
    table = soup.find("h1", text=re.compile("^Schätzungen")).parent
    years = table.find_all("th")[1:]
    years = [x.get_text() for x in years]
    rows = table.find_all("tr")[1:]
    for row in rows:
        fields = row.find_all("td")
        fields = [x.get_text() for x in fields]
        name = fields[0]
        row_data = fields[1:]
        row_data = [x if x != "-" else None for x in row_data]
        row_data = [re.sub("[^\d,]", "", x) if x is not None else x for x in row_data]
        row_data = [re.sub(",", ".", x) if x is not None else x for x in row_data]
        row_data = [float(x) if x is not None else x for x in row_data]
        table_dict[name] = dict(zip(years, row_data))

    # Return Estimates in Dict
    return table_dict


# Define Function to Search for Stocks
def search_stock(stock: str, limit: int = -1):
    # Convert Stock Name to Lowercase
    stock = stock.lower()

    # Make Request
    soup = _make_soup("https://www.finanzen.net/suchergebnis.asp?_search=" + stock)

    # Check for Error
    if soup.find("div", {"class": "red"}) is not None:
        if "kein Ergebnis geliefert" in soup.find("div", {"class": "red"}).get_text():
            return list()

    # Define Function to Extract Results
    result_list = []
    table = soup.find("table", {"class": "table"})
    rows = table.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        name = cells[0].get_text()
        link = cells[0].find("a")["href"]
        link = "https://www.finanzen.net" + link
        result_list.append((name, link))

    # Filter Result if limit was given
    if limit > 0:
        # Decrease limit if bigger than result
        result_len = len(result_list)
        if limit > result_len:
            limit = result_len
        result_list = result_list[0:limit]

    # Return Result List as formatted String
    for result in result_list:
        result_name = result[0]
        result_short = re.search("aktien/(.+)-aktie", result[1]).group(1)
        print("{}: {}".format(result_name, result_short))
