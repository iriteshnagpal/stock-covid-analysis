import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import numpy as np
import matplotlib.pyplot as plt

confirmCasesDF1 = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
demiseCasesDF2 = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

confirmCasesDF1.rename(columns={'Province/State':'Province', 'Country/Region':'Country'}, inplace=True)
demiseCasesDF2.rename(columns={'Province/State':'Province', 'Country/Region':'Country'}, inplace=True)

confirmCasesDF1["Country"].replace("Winter Olympics 2022", "Invalid", inplace=True)
confirmCasesDF1["Country"].replace("Summer Olympics 2020", "Invalid", inplace=True)
confirmCasesDF1["Country"].replace("Diamond Princess", "Invalid", inplace=True)
confirmCasesDF1["Country"].replace("MS Zaandam", "Invalid", inplace=True)
confirmCasesDF1["Country"].replace("Korea, North", "North Korea", inplace=True)
confirmCasesDF1["Country"].replace("Korea, South", "South Korea", inplace=True)
confirmCasesDF1["Country"].replace("Taiwan*", "Taiwan", inplace=True)
confirmCasesDF1["Country"].replace("Invalid", np.nan, inplace=True)
confirmCasesDF1.dropna(subset=['Country'], inplace=True)
confirmCasesDF1["Province"].replace("Diamond Princess", "Invalid1", inplace=True)
confirmCasesDF1["Province"].replace("Grand Princess", "Invalid1", inplace=True)
confirmCasesDF1["Province"].replace("Repatriated Travellers", "Invalid1", inplace=True)
confirmCasesDF1.drop(confirmCasesDF1.loc[(confirmCasesDF1['Country']=="Canada") & (confirmCasesDF1['Province']=='Invalid1')].index, inplace=True)

# Some country names are invalid or having some special characters, Need to clean those country names
# import numpy as np
demiseCasesDF2["Country"].replace("Winter Olympics 2022", "Invalid", inplace=True)
demiseCasesDF2["Country"].replace("Summer Olympics 2020", "Invalid", inplace=True)
demiseCasesDF2["Country"].replace("Diamond Princess", "Invalid", inplace=True)
demiseCasesDF2["Country"].replace("MS Zaandam", "Invalid", inplace=True)
demiseCasesDF2["Country"].replace("Korea, North", "North Korea", inplace=True)
demiseCasesDF2["Country"].replace("Korea, South", "South Korea", inplace=True)
demiseCasesDF2["Country"].replace("Taiwan*", "Taiwan", inplace=True)
demiseCasesDF2["Country"].replace("Invalid", np.nan, inplace=True)
demiseCasesDF2.dropna(subset=['Country'], inplace=True)
demiseCasesDF2["Province"].replace("Diamond Princess", "Invalid1", inplace=True)
demiseCasesDF2["Province"].replace("Grand Princess", "Invalid1", inplace=True)
demiseCasesDF2["Province"].replace("Repatriated Travellers", "Invalid1", inplace=True)
demiseCasesDF2.drop(demiseCasesDF2.loc[(demiseCasesDF2['Country']=="Canada") & (demiseCasesDF2['Province']=='Invalid1')].index, inplace=True)

confirmed_summary_new = confirmCasesDF1.groupby('Country').agg({col : 'sum' for col in confirmCasesDF1.select_dtypes(include='int64').columns}).T
desmise_summary_new = demiseCasesDF2.groupby('Country').agg({col : 'sum' for col in confirmCasesDF1.select_dtypes(include='int64').columns}).T

aggr_data = pd.DataFrame({'Confirm Cases': confirmed_summary_new.sum(axis=1), 'Desmise case': desmise_summary_new.sum(axis=1) })

acc_key = 'YELUUO6EFBP48XHQ'
ts = TimeSeries(key=acc_key,output_format='pandas')
tuple_apple_stock_data = ts.get_daily('AAPL', outputsize= 'full')
df_apple_stck_data = tuple_apple_stock_data[0]
df_apple_stck_data.drop(['1. open', '4. close', '5. volume'], axis=1, inplace=True)
df_apple_stck_data.rename({'2. high':'high', '3. low': 'low'}, axis=1, inplace=True)
df_apple_stck_data.sort_index(inplace=True)
df_apple_stck_data = df_apple_stck_data.loc['2020-01-22' : '2023-03-09']
df_apple_stck_data.index = df_apple_stck_data.index.strftime('%m/%d/%y')
tuple_airca_stock_data = ts.get_daily('AC', outputsize= 'full')
df_airca_stck_data = tuple_airca_stock_data[0].copy()
df_airca_stck_data.drop(['1. open', '4. close', '5. volume'], axis=1, inplace=True)
df_airca_stck_data.rename({'2. high':'high', '3. low': 'low'}, axis=1, inplace=True)
df_airca_stck_data.sort_index(inplace=True)
df_airca_stck_data = df_airca_stck_data.loc['2020-01-22' : '2023-03-09']
df_airca_stck_data.index = df_airca_stck_data.index.strftime('%m/%d/%y')

aggr_data.index = pd.to_datetime(aggr_data.index).strftime('%m/%d/%y')
aggr_data['Apple High'] = df_apple_stck_data['high']
aggr_data['Apple Low'] = df_apple_stck_data['low']
aggr_data['Air Canada High'] = df_airca_stck_data['high']
aggr_data['Air Canada Low'] = df_airca_stck_data['low']
aggr_data.rename(columns = {'Confirm Cases': 'confirm_cases', 'Desmise case' : 'demise_cases', 'Apple High':'apple_high_value', 
                            'Apple Low': 'apple_low_value', 'Air Canada High': 'air_canada_high', 'Air Canada Low': 'air_canada_low'}, 
                            inplace=True)

previous_date = None
for current_date in aggr_data.index:
    appl_high_val = aggr_data.loc[current_date, 'apple_high_value']
    appl_low_val = aggr_data.loc[current_date, 'apple_low_value']
    ac_high_val = aggr_data.loc[current_date, 'air_canada_high']
    ac_low_val = aggr_data.loc[current_date, 'air_canada_low']

    # Check if the current value is missing
    if pd.isna(appl_high_val):
        aggr_data.loc[current_date, 'apple_high_value'] = aggr_data.loc[previous_date, 'apple_high_value']
    if pd.isna(appl_low_val):
        aggr_data.loc[current_date, 'apple_low_value'] = aggr_data.loc[previous_date, 'apple_low_value']
    if pd.isna(ac_high_val):
        aggr_data.loc[current_date, 'air_canada_high'] = aggr_data.loc[previous_date, 'air_canada_high']
    if pd.isna(ac_low_val):
        aggr_data.loc[current_date, 'air_canada_low'] = aggr_data.loc[previous_date, 'air_canada_low']
    
    # Update the previous index for the next iteration
    previous_date = current_date

# Plotting the graph to show the impact of covid on Apple stock
aggr_data_2022 = aggr_data.loc['01/01/22':'12/31/22']
fig, ax1 = plt.subplots(figsize=(8, 6))

color = 'tab:blue'
ax1.set_xlabel('Year 2022')
ax1.set_ylabel('Confirm cases in 10xCrores', color=color)
ax1.plot(aggr_data_2022.index, aggr_data_2022['confirm_cases'], label='Confirm cases', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='upper left')
ax1.set_xticks(aggr_data_2022.index[::30])
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30)

ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Apple Stock Price ($)', color=color)
ax2.plot(aggr_data_2022.index, aggr_data_2022['apple_high_value'], label='Apple Stock Price ($)', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc='upper right')

ax1.set_title('Impact of Covid-19 on Apple Stock')
plt.tight_layout()

plt.show()

# Plotting the graph to show the impact of covid on Air Canada Stock
fig, ax1 = plt.subplots(figsize=(8, 6))

color = 'tab:blue'
ax1.set_xlabel('Year 2022')
ax1.set_ylabel('Confirm cases in 10xCrores', color=color)
ax1.plot(aggr_data_2022.index, aggr_data_2022['confirm_cases'], label='Confirm cases', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='upper left')
ax1.set_xticks(aggr_data_2022.index[::30])
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30)

ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Air Canada Stock Price ($)', color=color)
ax2.plot(aggr_data_2022.index, aggr_data_2022['air_canada_high'], label='Air Canada Stock Price ($)', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc='upper right')

ax1.set_title('Impact of Covid-19 on Air Canada Stock')
plt.tight_layout()
plt.show()

# Top 20 countries according to the confirmed COVID-19 numbers for a given date.
given_date = '1/21/22'
data = confirmed_summary_new.loc[given_date].sort_values().tail(20)
df = pd.DataFrame(data)

fig = plt.figure(figsize =(10, 7))

# Horizontal Bar Plot
plt.barh(pd.Series(data.index[0:20]), pd.Series(data[0:20]), color=plt.cm.viridis(np.linspace(0, 1, len(pd.Series(data.index[0:20])))))
plt.xlabel('Confirm Cases')

# Show Plot
plt.show()
