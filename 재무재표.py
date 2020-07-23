from pykrx import stock
import pandas as pd
tickers = stock.get_market_ticker_list()

def low_evaluation_list():
    # 종목별 DIV/BPS/PER/EPS 조회
    df = stock.get_market_fundamental_by_ticker("20200721")
    df = df[ (df['PER'] <= 9) & (df['PBR'] <= 1) ]

    df2 = stock.get_market_cap_by_ticker("20200721")

    df3 = pd.merge(df, df2, left_index=True, right_index=True, how='outer')

    df3 = df3[['종목명', 'DIV', 'BPS', 'PER', 'EPS', 'PBR', '시가총액', '거래량']]
    df3['거래량'] = df3['거래량'].apply(lambda x : format(x, ','))
    df3['시가총액'] = df3['시가총액'].apply(lambda x: x/100000000).apply(int).apply(lambda x : format(x, ',')) + ' 억'
    df3['PBR'] = df3['PBR'].apply(lambda x: '%.2f' % x)

    df3= df3.sort_values(['EPS'], ascending=False)
    print(df3.head(10))

def calculate_RSI(df, period):
    date_index = df.index.astype('str')
    import numpy as np
    U = np.where(df.diff(1)['종가'] > 0,  df.diff(1)['종가'], 0)
    D = np.where(df.diff(1)['종가'] < 0,  df.diff(1)['종가'] * (-1), 0)
    AU = pd.DataFrame(U, index=date_index).rolling(window=period).mean()
    AD = pd.DataFrame(D, index=date_index).rolling(window=period).mean()
    RSI = (AU* 100)/ (AD+AU)
    return RSI

df = stock.get_market_ohlcv_by_date("20200510", "20200720", "003240")
ma_ls = [10,20,30]
for i in range(len(ma_ls)):
    a = df['Close'].rolling(window=ma_ls[i]).mean()
    df['MA'+str(ma_ls[i])] = a
print(df)


import matplotlib.pyplot as plt
fig, axes = plt.subplots(nrows=2, ncols=1)

fig.set_size_inches((16, 10))


axes[0].plot(df.index, df['종가'],'rs--', label='종가')
axes[0].plot(df.index, df['MA5'], label='MA5')
axes[0].plot(df.index, df['MA10'], label='MA10')
axes[0].set_title('주식 분석 차트')

axes[0].set_xlabel('date')
axes[0].set_ylabel('price')
axes[0].set_ylim(690000, 810000)
axes[0].legend(loc='upper right')
# annotation
axes[0].annotate('매수', xy=('2020-07-01', 701000), xytext=('2020-07-02', 706000), arrowprops={'color': 'green'})

axes[1].plot(df.index, df['RSI'], label='RSI')
axes[1].plot(df.index, df['RSI signal'], label='RSI signal')
axes[1].set_title('주식 분석 차트')

axes[1].set_xlabel('date')
axes[1].set_ylabel('price')
axes[1].set_ylim(25, 65)
axes[1].legend(loc='upper right')

for ax in fig.axes:
    plt.sca(ax)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.rcParams["font.family"] = 'NanumBarunGothic'
    plt.rcParams["font.size"] = 10
    plt.rcParams["figure.figsize"] = (8, 4)
plt.show()





'''
market_sum = []
quant = []
for ticker in df.loc[:10, '티커']:
    ticker_info = stock.get_market_cap_by_date("20200721", "20200721", ticker)

    market_sum.append(ticker_info.iloc[0, 0])
    quant.append(ticker_info.iloc[0, 1])

df = pd.concat([df, pd.Series(market_sum, name='시가총액')], axis=1)
df = pd.concat([df, pd.Series(quant, name='거래량')], axis=1)
print(df.head(10))

'''