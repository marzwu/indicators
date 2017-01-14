import datetime
import math
import time
import traceback

import indicators
from okcoin.OkcoinSpotAPI import OKCoinSpot

MODE_REAL = 'real'  # 实盘
MODE_TEST = 'test'  # 回测

# 初始化apikey, secretkey, url
apikey = '59fa9b3d-defd-47ba-81e6-d9341573a4fa'
secretkey = 'C3A17CC5AC769EAED1970E223793117F'
okcoinRESTURL = 'www.okcoin.cn'  # 请求注意：国内账号需要 修改为 www.okcoin.cn

# 现货API
okcoinSpot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)

cash = 100.0
coin = 0.0

raw_cash = cash
start_time = time.time()

mode = MODE_TEST
t = time.mktime(datetime.date(2016, 5, 1).timetuple()) * 1000

while True:
    try:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('t: {}'.format(t))

        kline = okcoinSpot.kline('btc_cny', '1min', 2880, t)
        # kline = okcoinSpot.kline('btc_cny', '1min', 100, int(t / 1000))

        print('kline长度{}'.format(len(kline)))
        # kdj = KDJ_stoch(kline)
        kdj = indicators.KDJ(kline)
        print(kdj)

        last = kdj[-1]
        middle = kdj[-2]
        far = kdj[-3]
        fast = 2
        slow = 1
        gold = False
        fork = False  # 金叉或死叉
        if (last[fast] - last[slow]) * (middle[fast] - middle[slow]) < 0:
            gold = last[fast] > last[slow]
            fork = True
        elif (far[fast] - far[slow]) * (middle[fast] - middle[slow]) < 0:
            gold = middle[fast] > middle[slow]
            fork = True

        if fork:
            print('金叉') if gold else print('死叉')

            ticker = okcoinSpot.ticker('btc_cny')
            if gold:
                print('买入')
                coin += cash / float(ticker['ticker']['sell'])
                cash = 0.0
            else:
                print('卖出')
                cash += coin * float(ticker['ticker']['buy'])
                coin = 0.0

                rate = cash / raw_cash
                days = math.ceil((time.time() - start_time) / 86400)
                print('总增长率: {}, 日增长率: {}'.format(rate - 1, math.pow(rate, days) - 1))

            print('cash: {}, coin: {}, total: {}'.format(cash, coin, cash + coin * float(ticker['ticker']['buy'])))
    except Exception as e:
        print(traceback.format_exc())
    finally:
        # t = kline[-1][0]
        t += 60 * 1000

# while True:
#     try:
#         print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#
#         time.mktime(datetime.date(2016, 1, 1).timetuple())
#
#         if mode == MODE_REAL:
#             kline = okcoinSpot.kline('btc_cny', '1min', 100)
#         else:
#             kline = okcoinSpot.kline('btc_cny', '1min', 10000,
#                                      time.mktime(datetime.date(2016, 1, 1).timetuple()) * 1000)
#
#         print('kline长度{}'.format(len(kline)))
#         # kdj = KDJ_stoch(kline)
#         kdj = indicators.KDJ(kline)
#         print(kdj)
#
#         last = kdj[-1]
#         middle = kdj[-2]
#         far = kdj[-3]
#         fast = 2
#         slow = 1
#         gold = False
#         fork = False  # 金叉或死叉
#         if (last[fast] - last[slow]) * (middle[fast] - middle[slow]) < 0:
#             gold = last[fast] > last[slow]
#             fork = True
#         elif (far[fast] - far[slow]) * (middle[fast] - middle[slow]) < 0:
#             gold = middle[fast] > middle[slow]
#             fork = True
#
#         if fork:
#             print('金叉') if gold else print('死叉')
#
#             ticker = okcoinSpot.ticker('btc_cny')
#             if gold:
#                 print('买入')
#                 coin += cash / float(ticker['ticker']['sell'])
#                 cash = 0.0
#             else:
#                 print('卖出')
#                 cash += coin * float(ticker['ticker']['buy'])
#                 coin = 0.0
#
#                 rate = cash / raw_cash
#                 days = math.ceil((time.time() - start_time) / 86400)
#                 print('总增长率: {}, 日增长率: {}'.format(rate - 1, math.pow(rate, days) - 1))
#
#             print('cash: {}, coin: {}, total: {}'.format(cash, coin, cash + coin * float(ticker['ticker']['buy'])))
#     except Exception as e:
#         print(traceback.format_exc())
#     finally:
#         if mode == MODE_REAL:
#             time.sleep(60)
#             # time.sleep(5)
