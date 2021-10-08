# Finanzen-Fundamentals
Finanzen-Fundamentals is a Python package that can be used to retrieve fundamentals of stocks and ETFs. The data is fetched from [finanzen.net](https://www.finanzen.net), a German language financial news site. Note that the api is English but all data will be returned in German.

# Installation
You can easily install finanzen-fundamentals via pip: `pip install finanzen-fundamentals`

If you decide to build from the source code, make sure that you have the following dependencies installed:
* requests
* bs4
* lxml
* pandas
* numpy

You can install all of them by running: `pip install requests bs4 lxml pandas numpy`.

# Usage
## Import
After you successfully installed the package, you can include it in your projects by importing it. All modules are divided by instrument. For example, if you wan to interact with stocks, you could import all functionality related to stocks like so:

```
import finanzen_fundamentals.stocks as stocks
import finanzen_fundamentals.etfs as etfs
```

## Retrieve Fundamentals
You can retrieve the fundamentals of a single stock by running: 

```bmw_fundamentals = stocks.get_fundamentals("bmw-aktie")```

This will fetch the fundamentals of BMW and save it into a Pandas DataFrame called bmw_fundamentals.
The data is split into the following categories:
* Quotes
* Key Ratios
* Income Statement
* Balance Sheet
* Other

Optionally, you can add the argument `output="dict"`. Instead of a Pandas DataFrame, you will receive a dictionary. Every category will hold another dictionary.

```bmw_fundamentals = stocks.get_fundamentals("bmw-aktie", output="dict")```

You can also fetch estimates for expected values by using:

```bmw_estimates = stocks.get_estimates("bmw-aktie")```

Again, the data will be saved as a Pandas DataFrame. If you want to receive the data as a dictionary, you could use `output="dict"` again.

```bmw_estimates = stocks.get_estimates("bmw-aktie", output="dict")```

Note that we use stock names not stock symbols when fetching data. You can search for stock names by using

```stocks.search_stock("bmw", limit=3)```

This will return the three most matching stock names for your search. You can increase the limit to 30. If you don't give a parameter, all available data will be returned (up to 30). The key "short_name" will contain the name that can be used to query finanzen.net.

## Retrive ETF Information
You can get ETF infos as a Pandas DataFrame or a Python dictionary by first importing the etfs module:

```import finanzen_fundamentals.etfs as etfs```

Afterwards, you can get ETF data by giving the name of the ETF to the get_info function. Note that you could also use "dict" as a value for the output argument. This would return the result as a dictionary.

```msci_world = etfs.get_info("ishares-msci-world-etf-ie00b0m62q58")```

Again, we use internal short names for ETFs. You can search these names by running:

```etfs.search_etf("iShares", limit=3)```

## Retrieve Prices
You can also choose to get current stock prices. For this, you can import the stocks module.
```
import finanzen_fundamentals.stocks as stocks
```

There, you will find the get_price function. It takes two arguments: the stock name and the exchange you would like to get a price for. Assuming that you want to get the current price of a BMW stock on the Frankfurt Stock Exchange, you can do the following.
```
bmw_price = stocks.get_price(stock="bmw-aktie", exchange="FSE")
```

bmw_price will be a Pandas dataframe containing the following columns: "price" (The current price), "currency" (The currency for the latest quotation), "timestamp" (A datetime object representing the point in time the quote was created), "stock" (The name of the stock. Note that this is the system's name), and "exchange" (The name of the exchange you requested the price on.).
Please notice that the "timestamp" key might only have daily resolution. For some stocks there is only a single price for a single day.
As of now, the following exchanges are supported:
* "BER": Berlin
* "BMN": gettex
* "DUS": Düsseldorf
* "FSE": Frankfurt
* "HAM": Hamburg
* "HAN": Hannover
* "MUN": Munich
* "XETRA": Xetra
* "STU": Stuttgart
* "TGT": Tradegate
* "XQTX": Quotrix
* "BAE": Baader Bank
* "NASO": NASDAQ OTC

If you don't specify a specific exchange, FSE is choosen for you.

Alternatively, you could get the current price as a dictionary like this:

```
bmw_price = stocks.get_price(stock="bmw-aktie", exchange="FSE", output="dict")
```

If you want to extract prices for ETFs, you can use the get_price function inside the ETF module like so.

```
import finanzen_fundamentals.etfs as etfs
ishare_price = etfs.get_price(etf="ishares-core-msci-world-etf-ie00b4l5y983")
```

Just as with stocks, you can specify the exchange and output format.

## Alternative Implementation
Thanks to the contribution of [backster82](https://github.com/backster82), there is also a xml based alternative to the preceeding functions. All of the following functions will return a Pandas DataFrame. Note that get_fundamentals and get_estimates now incorporates the functionallity of the alternative implementation. Hence, you will receive deprecation warning upon using these functions.

You can obtain fundamentals like so:

```bmw_fundamentals = ff.get_fundamentals_lxml("bmw")```

Estimates can be loaded via:

```bmw_estimates = ff.get_estimates_lxml("bmw")```

Additionally, you can also load the current stock price for a vast selection of stock exchanges. For example, you can retrieve the current stock prices for BMW by using the following line of code:

```bmw_price = ff.get_current_value_lxml("bmw")```

This will give you the current price at Tradegate. However, you can change the stock exchange by entering its symbol for the "exchange" argument. If you want to obtain the current price of BMW stocks at the Frankfurt Stock Exchange, you can use the following command:

```bmw_price_frankfurt = ff.get_current_value_lxml("bmw", exchange = "FSE")```

You can find all available exchanges by inspecting the StockMarkets dictionary in `finanzen_fundamentals.statics`.


