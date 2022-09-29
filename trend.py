# https://www.analyticsvidhya.com/blog/2021/06/download-financial-dataset-using-yahoo-finance-in-python-a-complete-guide/?

import pandas as pd
import datetime as dt
import yfinance as yf
from yahoofinancials import YahooFinancials
import bottleneck as bn
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib.dates as mdates
import streamlit as st


# ma は moving average。

def moving_average(issue_name):
    dt_today = dt.datetime.now().strftime('%Y-%m-%d')
    df = yf.download(issue_name,
                     start='2018-01-01',
                     end=dt_today,
                     progress=False,
                     )
    df[issue_name + '_3days_ma'] = bn.move_mean(df['Close'], window=3)
    df = df.rename(columns={'Close': issue_name + '_close'})
    return df.loc[:, [issue_name + '_close', issue_name + '_3days_ma']]


ma_df = pd.merge(moving_average('^DJI'), moving_average(
    '^N225'), on='Date', how='outer').sort_values('Date')
ma_df = pd.merge(ma_df, moving_average('^GSPC'), on='Date',
                 how='outer').sort_values('Date')

ma_df_filled = ma_df.fillna(method='ffill')

# https://www.yutaka-note.com/entry/pandas_plot
# https://www.yutaka-note.com/entry/matplotlib_time_axis#%E6%9C%88%E5%8D%98%E4%BD%8D%E3%81%AE%E7%9B%AE%E7%9B%9B%E3%82%8A
fig = plt.figure()

ax1 = fig.add_subplot()
ax2 = ax1.twinx()
ax1.plot(ma_df_filled.index,
         ma_df_filled['^DJI_3days_ma'], color="orange", label='NYダウ')
ax1.plot(ma_df_filled.index,
         ma_df_filled['^N225_3days_ma'], color="blue", label='日経225')
ax2.plot(ma_df_filled.index,
         ma_df_filled['^GSPC_3days_ma'], color="green", label='S&P500')
locator = mdates.MonthLocator(bymonthday=15, interval=2)
ax1.xaxis.set_major_locator(locator)
ax1.xaxis.set_tick_params(rotation=45)

ax1.set_ylabel("NYダウ/日経225")  # y1軸ラベル
ax2.set_ylabel("S&P500")  # y2軸ラベル

# 凡例
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='lower right')
# plt.show()
st.pyplot(fig)

# print(moving_average('^DJI').head(20))
# print(moving_average('^N225').head(20))
# print(ma_df)
# print(ma_df.fillna(method='ffill'))

# ma_df.to_csv('/Volumes/外付けSSD1/python/trade/trend/with_na.csv')
# ma_df.fillna(method='ffill').to_csv('/Volumes/外付けSSD1/python/trade/trend/no_na.csv'
