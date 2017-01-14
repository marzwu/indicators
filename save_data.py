import time
import json
import traceback

from okcoin.OkcoinSpotAPI import OKCoinSpot

MODE_REAL = 'real'  # 实盘
MODE_TEST = 'test'  # 回测

# 初始化apikey, secretkey, url
apikey = '59fa9b3d-defd-47ba-81e6-d9341573a4fa'
secretkey = 'C3A17CC5AC769EAED1970E223793117F'
okcoinRESTURL = 'www.okcoin.cn'  # 请求注意：国内账号需要 修改为 www.okcoin.cn

# 现货API
okcoinSpot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)

while True:
    try:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

        time_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        print('start save {}'.format(time_str))

        kline = okcoinSpot.kline('btc_cny', '1min', 3000)
        file = open('okcoin_data/{}.json'.format(time_str), 'w')
        json.dump(kline, file)
        # file.write(json.dump(kline))
        file.close()

        print('complete and sleeping 86400s')
        time.sleep(86400)
    except Exception as e:
        print(traceback.format_exc())
