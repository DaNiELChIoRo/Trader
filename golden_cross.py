
# Raw Package
from numpy.core.numeric import NaN
#Data Source
import yfinance as yf
#Data viz
import plotly.graph_objs as go
import functools
import datetime
import  sched, time
from services.trader import make_order
import sys

s = sched.scheduler(time.time, time.sleep)
sleep = 60 * 10
def main():
    print("Doing stuff...")
    # do your stuff
    s.enter(0, 1, make_calculus, (s,))
    s.run()  

def make_calculus(sc):
    print("making calculations", datetime.datetime.now())
    s.enter(sleep, 1, make_calculus, (sc, ))
    calculate('BTC-USD', show=False)
    calculate('ETH-USD', show=False)
    calculate('XRP-USD', show=False)
    calculate('MANA-USD', show=False)
    calculate('LTC-USD', show=False)

def trade(currency, action):
    """
        Decides whether to place the order in type sell or buy 
    """

    return make_order(currency=currency, action=action)

def calculate(pair, period = '8d', interval = '90m', show = True):
#Importing market data
    try:
        data = yf.download(tickers=pair, period = period, interval = interval)
    except:
        calculate(pair=pair, period=period, show=show)
        print("Calculate after error!!!, ", error)

    #Adding Moving average calculated field
    data['MA5'] = data['Close'].rolling(5).mean()
    data['MA20'] = data['Close'].rolling(20).mean()
    time = datetime.datetime.now() - datetime.timedelta(minutes=90)
    # print("current time ", datetime.datetime.now() , " and minus 90 min ", time)
    
    crosses = []
    for idx, item in enumerate(data['MA5']):        
        if idx == 0 or idx == len(data) or data['MA20'][idx] == NaN or item == NaN:
            continue
        if data['MA20'][idx] == item:
            print('NEVER TO BE CALLED ***** cross point: ', item)   
            crosses.append((data.index[idx], data['MA20'][idx]))          
        if idx + 1 < len(data['MA5']):   
            low_long_range = functools.reduce(lambda x, y: x + y, data['MA20'][idx - 1:idx + 1])
            low_short_range = functools.reduce(lambda x, y: x + y, data['MA5'][idx - 1:idx + 1])
            long_long_range = functools.reduce(lambda x, y: x + y, data['MA20'][idx:idx + 2])
            long_short_range = functools.reduce(lambda x, y: x + y, data['MA5'][idx:idx + 2])
            if low_long_range > low_short_range and long_long_range < long_short_range:
                # print('***** cross point: ', item , ' and ', data.index[idx].timestamp())   
                crosses.append((data.index[idx], data['MA20'][idx], "BUY"))                
                continue
            elif low_long_range < low_short_range and long_long_range > long_short_range:
                # print('***** cross point: ', item, 'and ' , data.index[idx].timestamp()) 
                crosses.append((data.index[idx], data['MA20'][idx], "SELL"))                
                continue             
    
    #Deciding if buying or selling
    last_cross_time = crosses[-1][0]
    current_less_90_timestamp = to_seconds(time)
    
    # Validating 
    if last_cross_time.timestamp() >= current_less_90_timestamp:
        # TODO:- call to action
        action = crosses[-1][2]
        currency = pair.partition("-")[0].lower()
        print("YOU SHOULD ", action, "!!!")             
        trade(currency=currency, action=action)
    else:
        print("Too long for to act!!")

    #Not even calculating chart if is not going to be shown!
    if show == False:
        return
    #declare figure
    fig = go.Figure()

    #Title
    fig.update_layout(title_text=pair)

    #Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'], name = 'market data'))

    #Add Moving average on the graph
    fig.add_trace(go.Scatter(x=data.index, y= data['MA20'],line=dict(color='blue', width=1.5), name = 'Long Term MA'))
    fig.add_trace(go.Scatter(x=data.index, y= data['MA5'],line=dict(color='orange', width=1.5), name = 'Short Term MA'))
    for idx, cross in enumerate(crosses):
        # print('cross: ', cross, ' x: ', crosses_index[idx])
        fig.add_annotation(x=cross[0],
                            y=cross[1],
                        # text="intersect",
                        text = cross[2],
                        font=dict(family="sans serif",
                                    size=18,
                                    color="green"),                        
                        ax=0,
                        ay=-100,
                        showarrow=True,
                        arrowcolor='purple',
                        arrowwidth=3,
                        arrowhead=1)

    #Updating X axis and graph
    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(count=5, label="5d", step="day", stepmode="backward"),
                dict(count=7, label="WTD", step="day", stepmode="todate"),
                dict(step="all")
            ])
        )
    )

    #Show    
    fig.show()

def to_seconds(date):
    return float(time.mktime(date.timetuple()))

# def _line_intersection(line1, line2):
#     intersections = []
#     print('line1: ', len(line1))
#     print('line1 0: ', len(line1[0]))
#     print('line1 1: ', len(line1[1]))
#     print('line2: ', len(line2))
#     print('line2 0: ', len(line2[0]))
#     print('line2 1: ', len(line2[1]))
#     for idx, _ in enumerate(line1[0]):
#         if idx + 1 < len(line1[0]):
#             if line1[1][idx] == NaN or line2[1][idx] == NaN:
#                 continue
#             print('loop ', idx, ' line 1_0: ', line1[0][idx], ' line2_0: ', line2[0][idx], ' line 1_1: ', line1[1][idx], ' line2_1: ', line2[1][idx])                        
#             xdiff = (line1[0][idx] - line1[1][idx], line2[0][idx] - line2[1][idx])
#             ydiff = (line1[0][idx + 1] - line1[1][idx + 1], line2[0][idx + 1] - line2[1][ idx + 1])

#             def det(a, b):
#                 return a[0] * b[1] - a[1] * b[0]

#             def _det(a, b):
#                 print('a: ', len(a), ' b: ', len(b))
#                 return a[idx] * b[idx + 1] - a[idx + 1] * b[idx]

#             div = det(xdiff, ydiff)
#             if div == 0:
#                 raise Exception('lines do not intersect')

#             d = (_det(*line1), _det(*line2))
#             x = det(d, xdiff) / div
#             y = det(d, ydiff) / div
#             print('x: ', x, 'y: ', y, ' div: ', div, ' d: ', d)
#             intersections.append((x, y ))
#     return intersections

# def line(p1, p2):
#     A = (p1[1] - p2[1])
#     B = (p2[0] - p1[0])
#     C = (p1[0]*p2[1] - p2[0]*p1[1])
#     return A, B, -C

# def intersection(L1, L2):
#     D  = L1[0] * L2[1] - L1[1] * L2[0]
#     Dx = L1[2] * L2[1] - L1[1] * L2[2]
#     Dy = L1[0] * L2[2] - L1[2] * L2[0]
#     if D != 0:
#         x = Dx / D
#         y = Dy / D
#         return x,y
#     else:
#         return False

# def line_intersection(line1, line2):
#     xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
#     ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

#     def det(a, b):
#         return a[0] * b[1] - a[1] * b[0]

#     div = det(xdiff, ydiff)
#     if div == 0:
#         raise Exception('lines do not intersect')

#     d = (det(*line1), det(*line2))
#     x = det(d, xdiff) / div
#     y = det(d, ydiff) / div
#     # print('x: ', x, 'y: ', y, ' div: ', div, ' d: ', d)
#     return x, y

if __name__ == "__main__":
    print len(sys.argv)
    if len(sys.argv) <= 1:
        main()
    else:
        calculate(pair=sys.argv[1])
