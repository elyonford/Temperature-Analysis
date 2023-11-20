# statistical analysis of temperature data, QuantPy on YouTube
# heating degree days (HDD), cooling degree days (CDD) "average" Temperature = Tmax + Tmin / 2
# index (?) for a period "N" is the sum of HDD or CDD over that period

# KANSAS CITY ?, 1889-01-01 to 12/31/1933
# KANSAS CITY DOWNTOWN AIRPORT, 1/1/1934 to 9/30/1972
# KANSAS CITY INTL AIRPORT, 10/1/1972 to 12/31/2021

# Tmax, Tmin, Precipitation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

kansas_city = pd.read_csv("data/USW00003947.csv")
st_louis = pd.read_csv("data/USW00013994.csv")
bhm = pd.read_csv("data/USW00013876.csv")

### Checking for missing max and min temperatures #was 63 and 56 with 54 misaligned; restricted to KCI there are 0
# max_temp = kansas_city[["Date","tmax"]]
# min_temp = kansas_city[["Date","tmin"]]
# # print(max_temp_kc.isnull().value_counts())
# # print(min_temp_kc.isnull().value_counts())

# count = 0
# for mx, mn in zip(np.where(max_temp.isnull())[0], np.where(min_temp.isnull())[0]):
#     if mx != mn:
#         count += 1
# print('\nNumber of misaligned null values equals', count)
###
 
kansas_city["Date"] = pd.to_datetime(kansas_city["Date"]) #Thanks skbrimmer!
st_louis["Date"] = pd.to_datetime(st_louis["Date"])
bhm["Date"] = pd.to_datetime(bhm["Date"])
kansas_city.set_index("Date", inplace=True)
st_louis.set_index("Date", inplace=True)
bhm.set_index("Date", inplace=True)
kc_temps = kansas_city[["tmax", "tmin"]]
stl_temps = st_louis[["tmax", "tmin"]]
bhm_temps = bhm[["tmax", "tmin"]]
 
def avg_temp(row):
    return (row.tmax + row.tmin) / 2
 
kc_temps["Tavg"] = kc_temps.apply(avg_temp,axis=1)
stl_temps["Tavg"] = stl_temps.apply(avg_temp,axis=1)
bhm_temps["Tavg"] = bhm_temps.apply(avg_temp,axis=1)
#drop na values here
kc_temps = kc_temps.dropna()
stl_temps = stl_temps.dropna()
bhm_temps = bhm_temps.dropna()
# print(kc_temps)
# print(kc_temps.describe())
 
# why deep copy? does it matter if the same values are referenced, and why do we need completely new bits?
kc_temps_season = kc_temps.copy(deep=True)
stl_temps_season = stl_temps.copy(deep=True)
bhm_temps_season = bhm_temps.copy(deep=True)
kc_temps_season["month"] = kc_temps_season.index.month
stl_temps_season["month"] = stl_temps_season.index.month
bhm_temps_season["month"] = bhm_temps_season.index.month
kc_mask = (kc_temps_season["month"] >= 5) & (kc_temps_season["month"] <= 10)
stl_mask = (stl_temps_season["month"] >= 5) & (stl_temps_season["month"] <= 10)
bhm_mask = (bhm_temps_season["month"] >= 5) & (bhm_temps_season["month"] <= 10)
kc_temps_season["summer"] = np.where(kc_mask,1,0)
stl_temps_season["summer"] = np.where(stl_mask,1,0)
bhm_temps_season["summer"] = np.where(bhm_mask,1,0)
kc_temps_season["winter"] = np.where(kc_temps_season["summer"] != 1,1,0)
stl_temps_season["winter"] = np.where(stl_temps_season["summer"] != 1,1,0)
bhm_temps_season["winter"] = np.where(bhm_temps_season["summer"] != 1,1,0)
# print(kc_temps_season.head(120))
 
# observe cycles in temperature
# kc_temps[-2000:].plot(figsize=(8,6))
# plt.show()
 
# distribution of temperatures
# plt.figure(figsize=(8,6))
# kc_temps.tmin.hist(bins=60, alpha=0.6, label="Tmin")
# kc_temps.tmax.hist(bins=60, alpha=0.6, label="Tmax")
# kc_temps["Tavg"].hist(bins=60, alpha=0.6, label="Tavg")
# plt.legend()
# plt.show()
 
# summer vs winter histograms
# plt.figure(figsize=(8,6))
# kc_temps_season[kc_temps_season["winter"] == 1]["Tavg"].hist(bins=60, alpha=0.8, label="winter")
# kc_temps_season[kc_temps_season["summer"] == 1]["Tavg"].hist(bins=60, alpha=0.8, label="summer")
# plt.legend()
# plt.show()
 
# resample by month start, calculate mins and maxes for tmax, tmin and Tavg
kc_date_list = kc_temps.index.tolist()
stl_date_list = stl_temps.index.tolist()
bhm_date_list = bhm_temps.index.tolist()
mth_kc_temps = pd.DataFrame(data=kc_date_list, index=kc_date_list).resample("MS")[0].agg([min,max])
mth_kc_temps["month"] = mth_kc_temps.index.month
mth_stl_temps = pd.DataFrame(data=stl_date_list, index=stl_date_list).resample("MS")[0].agg([min,max])
mth_stl_temps["month"] = mth_stl_temps.index.month
mth_bhm_temps = pd.DataFrame(data=bhm_date_list, index=bhm_date_list).resample("MS")[0].agg([min,max])
mth_bhm_temps["month"] = mth_bhm_temps.index.month
def min_max_kc_temps(row):
    stats = kc_temps[(kc_temps.index >= row["min"]) & (kc_temps.index <= row["max"])].agg([min, max])
    row["tmax_max"] = stats.loc["max", "tmax"]
    row["tmax_min"] = stats.loc["min", "tmax"]
    row["tmin_max"] = stats.loc["max", "tmin"]
    row["tmin_min"] = stats.loc["min", "tmin"]
    row["Tavg_max"] = stats.loc["max", "Tavg"]
    row["Tavg_min"] = stats.loc["min", "Tavg"]
    return row
def min_max_stl_temps(row):
    stats = stl_temps[(stl_temps.index >= row["min"]) & (stl_temps.index <= row["max"])].agg([min, max])
    row["tmax_max"] = stats.loc["max", "tmax"]
    row["tmax_min"] = stats.loc["min", "tmax"]
    row["tmin_max"] = stats.loc["max", "tmin"]
    row["tmin_min"] = stats.loc["min", "tmin"]
    row["Tavg_max"] = stats.loc["max", "Tavg"]
    row["Tavg_min"] = stats.loc["min", "Tavg"]
    return row
def min_max_bhm_temps(row):
    stats = bhm_temps[(bhm_temps.index >= row["min"]) & (bhm_temps.index <= row["max"])].agg([min, max])
    row["tmax_max"] = stats.loc["max", "tmax"]
    row["tmax_min"] = stats.loc["min", "tmax"]
    row["tmin_max"] = stats.loc["max", "tmin"]
    row["tmin_min"] = stats.loc["min", "tmin"]
    row["Tavg_max"] = stats.loc["max", "Tavg"]
    row["Tavg_min"] = stats.loc["min", "Tavg"]
    return row

mth_kc_temps = mth_kc_temps.apply(min_max_kc_temps,axis=1)
mth_stl_temps = mth_stl_temps.apply(min_max_stl_temps,axis=1)
mth_bhm_temps = mth_bhm_temps.apply(min_max_stl_temps,axis=1)
# print(mth_kc_temps)
 
# group min and max temps by month, relabel from numbers to abbreviations
grouped_mths_kc = mth_kc_temps.groupby(mth_kc_temps.month)[["tmax_max", "tmax_min", "tmin_max", "tmin_min", "Tavg_max", "Tavg_min"]].agg([min, max])
grouped_mths_kc['months'] = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
grouped_mths_kc = grouped_mths_kc.set_index('months')
grouped_mths_stl = mth_stl_temps.groupby(mth_stl_temps.month)[["tmax_max", "tmax_min", "tmin_max", "tmin_min", "Tavg_max", "Tavg_min"]].agg([min, max])
grouped_mths_stl['months'] = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
grouped_mths_stl = grouped_mths_stl.set_index('months')
grouped_mths_bhm = mth_bhm_temps.groupby(mth_bhm_temps.month)[["tmax_max", "tmax_min", "tmin_max", "tmin_min", "Tavg_max", "Tavg_min"]].agg([min, max])
grouped_mths_bhm['months'] = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
grouped_mths_bhm = grouped_mths_bhm.set_index('months')
# print(grouped_mths_kc[[("tmax_max", "max"),("tmin_min", "min"),("tmax_min", "min"),("tmin_max", "max")]])
 
# Look at the max and min of the Tavg max and min
# print(grouped_mths_kc[[("Tavg_max", "max"),("Tavg_max", "min"),("Tavg_min", "max"),("Tavg_min", "min")]])
 
# Now, decomposition of time-series components
# trend - decreasin, constant or increasing?
# seasonality - periodic signal
# noise - variation in signal not accounted for by trend or seasonailty, a.k.a. "remainder"
from statsmodels.tsa.seasonal import seasonal_decompose
kc_temps.sort_index(inplace=True)
stl_temps.sort_index(inplace=True)
bhm_temps.sort_index(inplace=True)
# print(kc_temps)

# kc_temps["Tavg"].rolling(window = 365*10).mean().plot(figsize=(8,4), color="tab:red", title="Rolling mean over a 10 year window")
fig, axs = plt.subplots(3, figsize=(8,6))
fig.suptitle('Rolling mean over a 10 year window for KC, STL and BHM')
axs[0].plot(kc_temps["Tavg"].rolling(window = 365*10).mean(), color="red")
axs[1].plot(stl_temps["Tavg"].rolling(window = 365*10).mean(), color="blue")
axs[2].plot(bhm_temps["Tavg"].rolling(window = 365*10).mean(), color="green")
plt.show()

# work on this piece -----
# to set the plot size 
plt.figure(figsize=(16, 8), dpi=150)
# in plot method we set the label and color of the curve. 
kc_temps["Tavg"].rolling(window = 365*10).mean().plot(label='KC', color='orange') 
stl_temps["Tavg"].rolling(window = 365*10).mean().plot(label='STL') 
bhm_temps["Tavg"].rolling(window = 365*10).mean().plot(label='BHM') 
# adding title to the plot 
plt.title('Single Axis Temp Plot') 
# adding Label to the x-axis 
plt.xlabel('Years') 
# adding legend to the curve 
plt.legend()
# work on the thing above this line ----

# kc_temps["Tavg"].rolling(window = 365*10).var().plot(figsize=(8,4), color="tab:red", title="Rolling variance over a 10 year window")
# plt.show()
 
# seasonal decomposition
# decompose_result_kc = seasonal_decompose(kc_temps['Tavg'], model='additive', period=int(365*10), extrapolate_trend='freq')
# decompose_result_stl = seasonal_decompose(stl_temps['Tavg'], model='additive', period=int(365*10), extrapolate_trend='freq')
# decompose_result_bhm = seasonal_decompose(bhm_temps['Tavg'], model='additive', period=int(365*10), extrapolate_trend='freq')

# trend_kc = decompose_result_kc.trend
# seasonal_kc = decompose_result_kc.seasonal
# residual_kc = decompose_result_kc.resid

# trend_stl = decompose_result_stl.trend
# seasonal_stl = decompose_result_stl.seasonal
# residual_stl = decompose_result_stl.resid

# trend_bhm = decompose_result_bhm.trend
# seasonal_bhm = decompose_result_bhm.seasonal
# residual_bhm = decompose_result_bhm.resid

# decompose_result.plot()
# plt.show()
 
# visualize 10 years
# years_examine = 365*5
# start_date = 3*years_examine
# fig, axs = plt.subplots(3, figsize=(8,6))
# fig.suptitle('Removed Trends for KC, STL and BHM')
# axs[0].plot(trend_kc[-start_date:-years_examine], color="red")
# axs[1].plot(trend_stl[-start_date:-years_examine], color="blue")
# axs[2].plot(trend_bhm[-start_date:-years_examine], color="green")
# axs[1].plot(seasonal_kc[-start_date:-years_examine])
# axs[1].set_ylim([-25,25])
# axs[2].plot(residual_kc[-start_date:-years_examine])
# axs[2].set_ylim([-20,20])
# plt.show()