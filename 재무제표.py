from pykrx import stock
import pandas as pd
tickers = stock.get_market_ticker_list()


# 종목별 DIV/BPS/PER/EPS 조회
df = stock.get_market_fundamental_by_ticker("20200721")
df = df[ (df['PER'] <= 9) & (df['PBR'] <= 1) ]

df2 = stock.get_market_cap_by_ticker("20200721")

df3 = pd.merge(df, df2, left_index=True, right_index=True, how='outer')
#df3= df3.sort_values(['EPS'], ascending=False)
#df.to_csv('df.csv', encoding='utf-8')
#df2.to_csv('df2.csv', encoding='utf-8')
#df3.sort_index().to_csv('df3.csv', encoding='utf-8')
print(df.sort_index())
print(df2.sort_index())



df3 = df3[['종목명', 'DIV', 'BPS', 'PER', 'EPS', 'PBR', '시가총액', '거래량']]
for c in df3[['시가총액', '거래량']]:
    df3[c] = df3[c].apply(lambda x : format(x, ','))
df3= df3.sort_values(['EPS'], ascending=False)
print(df3.head(10))



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