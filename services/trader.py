
from bitso_requester import get_account_balance, get_tricker, place_order, get_last_transactions, get_open_orders, cancel_order
import sys
import time

def __main__(*args):
    print "currency: " + args[0] + " action: " + args[1]
    if len(args) <= 2:
        make_order(currency=args[0], action=args[1])
    else:
        make_order(currency=args[0], action=args[1], type=args[2])        

def make_order(currency, action, type="fixed"):
    balances = get_account_balance()
    action = action.upper()
    currency_available_in_user_balance = currency in map(lambda x: x["currency"], balances)   
    if action == 'BUY':
        fiat_currency = filter(lambda x: x["currency"] == "mxn", balances)[0]
        cripto_currency = filter(lambda x: x["currency"] == currency, balances)[0] if currency in map(lambda x: x["currency"], balances)  else {'available': 0}
        balance = (float(fiat_currency['available']), float(cripto_currency['available']))
        print '## balance: ', fiat_currency
        print "user account currency balance: ", balance
        if balance[0] > 0 and (type == 'all' or balance[1] <= 0):
            # gettin' the last trade prices for that asset!
            prices = get_last_transactions(currency + "_mxn")
            if prices:
                # TRyin' to apply saffe rules
                budget = balance[0] / 2 if type == "fixed" else balance[0]
                # print "budget: " + budget
                # calculation the amount of crypto per budget.
                amount = float("{:.5f}".format(budget/prices[1])) #balance/(2 * 4)
                #Getting the highest price to buy
                price = prices[0] + 1
                print("$$$$$$ the order to ", action, " will be place with price ", price, " and amount of cryptos", amount, "\n")
                # placing the order!
                placed_order = place_order(amount, price, book=currency+"_mxn" ,side=action.lower())
                time.sleep(1)
                # Forcing the selling!
                while len(get_open_orders(currency+'_mxn')) > 0:
                    cancel_order()
                    make_order(currency=currency, action=action, type=type)
                    time.sleep(1)
                return placed_order
        elif balance[1] >= 0:
            print "You alredy has this crypto-currency !!" + " transaction type: " + type
        else:
            print "the user does not account the requested currency! :C, balance: " + balance[0] 
    elif action == 'SELL':
        if currency_available_in_user_balance == False:
            print "the user does not account the requested currency! :C "
            return
        cripto_currency = filter(lambda x: x["currency"] == currency, balances)[0]
        print('## cripto currency: ', cripto_currency)
        if cripto_currency:
            balance = float(cripto_currency['available'])
            print("user account currency balance: ", balance)
            if balance > 0:
                # gettin' the last trade prices for that asset!
                prices = get_last_transactions(currency + "_mxn")
                if prices:
                    # Sell all the cryptos mutherfucker!
                    amount = balance
                    # Getting the lowest price to sell :/
                    price = prices[0] - 1
                    print("$$$$$$ the order to ", action, " will be place with price ", price, " and amount of cryptos", amount, "\n")
                    placed_order = place_order(amount, price, book=currency+"_mxn" ,side=action.lower())
                    time.sleep(0.5)
                    while len(get_open_orders(currency+'_mxn')) > 0:
                        cancel_order()
                        make_order(currency=currency, action=action, type=type)
                        time.sleep(0.5)                
                    return placed_order 
        else:
            return Exception('No crypto assets available for transaction!!')

if __name__ == '__main__':
    __main__(*sys.argv[1:])