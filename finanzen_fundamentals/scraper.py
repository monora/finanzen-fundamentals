#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
# Import Modules
from bs4 import BeautifulSoup


useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "

# Define Function to load Site and convert to BeautifulSoup
def _make_soup(url: str):
    src = requests.get(url, headers={'User-Agent': useragent}).content
    soup = BeautifulSoup(src, "lxml")
    return soup
