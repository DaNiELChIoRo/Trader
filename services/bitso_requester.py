import time
import hmac
import hashlib
import requests
import json
from decimal import Decimal
from requests.api import request
import os
from dotenv import load_dotenv
# import trader

load_dotenv()

#  Define your request
bitso_key = os.getenv("bitso_key")
bitso_secret = os.getenv("bitso_secret")
request_path="/v3/balance/"

class RequestError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def main():
    # print"Calling requests")    
    print "account balance:", get_account_balance() 
    # get_user_trades()
    # get_available_books()
    # get_tricker()
    # get_last_transactions()
    # print"cancel all orders: ", cancel_order())
    print "\n\n"
    print "\n $$$$$\tuser open orders: ", get_open_orders()
    # print__test_(currency="ltc", action='BUY'))
    print "\n\n"
    print "\n $$$$$\tuser open orders: ", get_open_orders()

def __test_(currency = "eth", action = 'BUY'):
    """
        Internal test for placeing orders!.
    """
    return trader.make_order(currency=currency, action=action)
# Create signature
def __getSignature__(http_method = 'GET', request_path = '/v3/balance/', parameters={}):
    nonce =  str(int(round(time.time() * 1000)))
    message = nonce+http_method+request_path
    if (http_method == "POST"):
        message += json.dumps(parameters)
    return hmac.new(bitso_secret.encode('utf-8'),
                                                message.encode('utf-8'),
                                                hashlib.sha256).hexdigest()

def __make_request__(path, params = {}, type = 'GET'):
    nonce =  str(int(round(time.time() * 1000)))
    request_path = path
    signature = __getSignature__(request_path=request_path)
    # Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)  
    if type == 'GET':
        response = requests.get("https://api.bitso.com" + request_path, headers={"Authorization": auth_header})
    elif type == 'POST':
        response = requests.post("https://api.bitso.com" + request_path, json = params, headers={"Authorization": auth_header})
    elif type == 'DELETE': 
        response = requests.delete("https://api.bitso.com" + request_path, json = params, headers={"Authorization": auth_header})
    result = json.loads(response.content)    
    if result["success"]:
        return result["payload"]   
    else:
        print "rise error : ", result 
        raise RequestError(result)

def get_account_balance():
    r""" 
        Retrieves the user's account NON ZERO balance in the differente assets he/she has.        
    """
    result = __make_request__(path=request_path)
    try:
        payload = result["balances"]
        balance = filter(lambda x: float(x["available"]) > 0, payload)
        return balance
    except Exception as e:
        print "balance payload error "+e        

def get_user_trades():
    """
        Returns the user's trades
    """

    path = '/v3/user_trades/'
    result = __make_request__(path)    
    return result

def get_open_orders(book = 'btc_mxn'):
    r"""
        Retrieves the user's open orders from the given book
    """
    
    path = '/v3/open_orders?book=btc_mxn'
    result = __make_request__(path)
    
    return result

def cancel_order(order_id = "all"):
    """
        Cancels the given order_id's order which coud be one or an array of ids

        @param $order_id: orders?oids=<oid>,<oid>,<oid>

    """
    path = '/v3/orders/' + order_id
    request = __make_request__(path, type='DELETE');
    
    return request

def get_available_books(book_name = 'eth_mxn'):
    r""" 
        Returns the list of availbale books (cryptos) to trade 

        example: [u'btc_mxn', u'eth_btc', u'eth_mxn', u'xrp_btc']
    """    
    request_path = '/v3/available_books/'    
    result = __make_request__(path=request_path)
    # print"available books response: ", result)
    if result["success"]:
        payload = result['payload']
        books = map(lambda x: x["book"], payload)
        book = filter(lambda x: x["book"] == book_name, payload)[0]
        print "\n\n %%book ", book_name, ": ", book, "\n\n"
        print "\n$$$ min price for ", book_name, ": ", book["minimum_price"], " and max price: ", book["maximum_price"], " average: \n"
        print "books: ", books
        return books

def get_tricker(book = 'btc_mxn'):
    r"""
        Retrieves the tricker information from the given book
        returns a tuple with the highest price to buy and the lowest price to sell
        (high, low)
    """

    request_path = '/v3/ticker/?book=' + book
    payload = __make_request__(request_path)
        
    high = float(payload["bid"])
    low = float(payload["ask"])
    print 'highest buy: ', high, ' lowest sell: ', low
    return ("{:.2f}".format(high), "{:.2f}".format(low))

def get_last_transactions(book = 'btc_mxn'):
    r"""
        Retrieves the traiding information from the given book
        returns a tuple with the highest price to buy and the lowest price to sell
        (high, low)
    """

    request_path = '/v3/order_book/?book=' + book

    payload = __make_request__(request_path)    
    # print"last trades payload: ", payload)
    low = payload["bids"][0]
    high = payload["asks"][0]

    min_ask = float(str(min(map(lambda x: x["price"], payload["asks"]))))
    max_bid = float(str(max(map(lambda x: x["price"], payload["bids"]))))
    delta = min_ask - max_bid
    # print"max_bid: ", max_bid, " min_ask: ", min_ask)
    print '%%%% last_transsactions highest buy: ', max_bid, ' lowest sell: ', min_ask, " fair price: ", min_ask + (delta/2), ' delta: ', delta
    return (max_bid, min_ask, delta)

def place_order(amount, price, book = "btc_mxn", side = "BUY", type = 'limit', time_in_force = 'immediateorcancel'):
    """
        Place an order into the 
        @param $amount
    """
    nonce =  str(int(round(time.time() * 1000)))
    request_path = '/v3/orders/'
    #params
    params = {
        'book': book,
        'side': side,
        "type": type,
        'major': str(amount),
        'price': str(price),
        # 'time_in_force': time_in_force
    }
    signature = __getSignature__(http_method="POST", request_path=request_path, parameters=params)
    # Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)  

    response = requests.post("https://api.bitso.com" + request_path, json = params, headers={"Authorization": auth_header})
    print"response: ", response.content
    result = json.loads(response.content)
    if result["success"]:
        return result["payload"]

if __name__ == "__main__":
    main()