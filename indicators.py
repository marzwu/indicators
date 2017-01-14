import numpy as np
import talib


def KDJ_stoch(kline):
    hight = np.array([x[2] for x in kline])
    low = np.array([x[3] for x in kline])
    close = np.array([x[4] for x in kline])
    # matype: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
    K, D = talib.STOCH(hight, low, close, fastk_period=9, slowk_matype=0, slowk_period=3, slowd_period=3)
    J = 3 * K - 2 * D
    return (K[-3:], D[-3:], J[-3:])


def KDJ(date, N=9, M1=3, M2=3):
    '''
    RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
    K:SMA(RSV,M1,1);
    D:SMA(K,M2,1);
    J:3*K-2*D;
    '''
    datelen = len(date)
    array = np.array(date)
    kdjarr = []
    for i in range(datelen):
        if i - N < 0:
            b = 0
        else:
            b = i - N + 1
        rsvarr = array[b:i + 1, 0:5]
        rsv = (float(rsvarr[-1, 4]) - float(min(rsvarr[:, 3]))) / (
            float(max(rsvarr[:, 2])) - float(min(rsvarr[:, 3]))) * 100
        if i == 0:
            k = rsv
            d = rsv
        else:
            k = 1 / float(M1) * rsv + (float(M1) - 1) / M1 * float(kdjarr[-1][2])
            d = 1 / float(M2) * k + (float(M2) - 1) / M2 * float(kdjarr[-1][3])
        j = 3 * k - 2 * d
        kdjarr.append(list((rsvarr[-1, 0], rsv, k, d, j)))
    # return kdjarr
    # return [[kdjarr[-3][2], kdjarr[-3][3], kdjarr[-3][4]], [kdjarr[-2][2], kdjarr[-2][3], kdjarr[-2][4]],
    #         [kdjarr[-1][2], kdjarr[-1][3], kdjarr[-1][4]]]
    return [[x[2], x[3], x[4]] for x in kdjarr]
