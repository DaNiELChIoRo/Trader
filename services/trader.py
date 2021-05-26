
from bitso_requester import get_account_balance, get_tricker, place_order, get_last_transactions

def make_order(currency, action):
    balances = get_account_balance()
    action = action.upper()
    if action == 'BUY':
        fiat_currency = filter(lambda x: x["currency"] == "mxn", balances)[0]
        cripto_currency = filter(lambda x: x["currency"] == currency, balances)[0]
        # print('## fiat currency: ', fiat_currency)
        balance = (float(fiat_currency['available']), float(cripto_currency['available']))
        print("user account currency balance: ", balance)
        if balance[0] > 0 and balance[1] <= 0:
            # gettin' the last trade prices for that asset!
            prices = get_last_transactions(currency + "_mxn")
            if prices:
                # TRyin' to apply saffe rules
                budget = 100 #balance/(2 * 4)
                # calculation the amount of crypto per budget.
                amount = float("{:.5f}".format(budget/prices[1])) #balance/(2 * 4)
                #Getting the highest price to buy
                price = prices[0] + 1
                print("$$$$$$ the order to ", action, " will be place with price ", price, " and amount of cryptos", amount, "\n")
                # placing the order!
                return place_order(amount, price, book=currency+"_mxn" ,side=action.lower())
    elif action == 'SELL':
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
                    return place_order(amount, price, book=currency+"_mxn" ,side=action.lower())
        else:
            return Exception('No crypto assets available for transaction!!')