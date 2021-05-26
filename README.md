# Automatic Trader
This is an automatic trader created on Python 2.7 conected to Bitso® which buy/sell in virtue of the last tendencies and consults to the
Yahoo Finance API for trading information. By default runs on background and sleeps every 10 minutes.

## Books
the cross and charts information is are retrived from the Yahoo Finance API by their Python's library (yfinance).
Which is tide to the USD currency pair. That is, is only going to retrieve books with the USD currency, ex; USD-ETH. 

## Graphics
By the default the charts are turned off but can be turn on by erasing the default parameters ´show´in the ´make_calculus´function
ir setting it to True 

## Requester
Performs requests to the Bitso's API which can be consulted at ´https://bitso.com/developers´.

In order to make it work you most create a .env file with ´bitso_secret´ and ´bitso_key´ variables 
which has to be created by registering on the Bitso's developer platform.