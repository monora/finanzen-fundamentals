# Finanzen-Fundamentals
Finanzen-Fundamentals is a Python package that can be used to retrieve fundamentals of stocks. The data is fetched from [finanzen.net](https://www.finanzen.net), a German language financial news site. Note that the api is English but all data will be returned in German.

# Installation
You can easily install finanzen-fundamentals via pip: `pip install finanzen-fundamentals`

If you choose to download the source code, make sure that you have the following dependencies installed:
* requests
* BeautifulSoup
* lxml
You can install all of them by running: `pip install requests BeautifulSoup lxml`.

# Usage
## Import
After you successfully installed the package, you can include it in your projects by importing it.

```import finanzen_fundamentals.stocks as ff```

## Retrieve Fundamentals
You can retrieve the fundamentals of a single stock by running: 

```bmw_fundamentals = ff.get_fundamentals("bmw")```

This will fetch the fundamentals of BMW and save it into a dictionary called bmw_fundamentals.
bmw_fundamentals will have the following keys:
* Quotes
* Key Ratios
* Income Statement
* Balance Sheet
* Other

The values for those keys will be variables, holding a year:value dictionary. If no data can be found, the value will be None.
You can also fetch estimates for expected values by using:

```bmw_estimates = ff.get_estimates("bmw")```

This will save estimates for the most important key metrics if available. The resulting dictionary will hold variable names as keys and a year:value dictionary as values.

Note that we use stock names not stock symbols when fetching data. You can search for stock names by using

```ff.search_stock("bmw", limit = 3)```

This will print the three most matching stock names for your search. You can increase the limit to 30. If you don't give a parameter, all available data will be printed (up to 30).
