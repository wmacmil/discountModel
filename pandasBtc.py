import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression


# current := spot
# parse_dates gives pandas internal date representation
future = pd.read_csv('f.csv',parse_dates=['date'])
curren = pd.read_csv('c.csv',parse_dates=['date'])

# filtered nans
futures = future[future.open.notnull()]
current = curren[curren.open.notnull()]

futuresDates = futures["date"]

# only keep those entries which satisfy isInFutureDates(x) predicate, see link for solution
# https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values
def isInFutureDates(x):
    for y in futuresDates:
        if x == y:
            return True

filteredSpotrent = current.loc[current['date'].isin(futuresDates)]


# now the test fails? this is due to something i did with filtering the nans
# basically, the subset assumption fails once we've filtered out nans
# tests
testDates = np.all(futures.date.values == filteredSpotrent.date.values) == True
testTestValid = np.all(np.array([False,True])) == False

def diffCol(d,x,y):
    return d[x] - d[y]

def divCol(d,x,y):
    return d[x] / d[y]

# merge the tables, now x and y parameters
futSpot = pd.merge(futures, filteredSpotrent , on="date")


# indices
# x := futures
# y := filteredSpotrent, e.g. filtered spot

# rate of chagne
futSpot["diffOpenCloseFut"] = diffCol(futSpot,'close_x','open_x') # delta p
futSpot["diffOpenCloseSpot"] = diffCol(futSpot,'close_y','open_y') # delta q

# futSpot["ratioDiffOpenClose"] = divCol(futSpot,'diffOpenCloseX','diffOpenCloseY')

# nomralized differences
# delta p / p0
# delta q / q0
futSpot["normalizeDiffFut"] = divCol(futSpot,'diffOpenCloseFut','open_x')
futSpot["normalizeDiffSpot"] = divCol(futSpot,'diffOpenCloseSpot','open_y')

futSpot["ratioNormalizedFutSpot"] = divCol(futSpot,'normalizeDiffFut','normalizeDiffSpot')

# finding the outlier
# futSpot[futSpot.ratioNormalizedFutSpot == futSpot.ratioNormalizedFutSpot.min()].index == 783

# probably a better way to do this than to work with nanoSec
futSpot['numDate'] = pd.to_numeric(futSpot.date)

futSpotMinusOutlier = futSpot.drop(
    labels=[783],
    axis=0
    )

# xdates = futSpotMinusOutlier.numDate.values

# this invalidates the data as there are missed dates, but we compromise for
# the time being

# problem here
# futSpot.isnull().open_x.any() == True

xdates = futSpotMinusOutlier.numDate.values
yratio = futSpotMinusOutlier.ratioNormalizedFutSpot.values
# issue here with the nan
res = stats.linregress(xdates,yratio)

# stuff = stats.linregress(futSpot['date'],futSpot['ratioNormalizedFutSpot'])

# slope, intercept, r, p, se = stats.linregress(futSpot['date'],futSpot['ratioNormalizedFutSpot'])

def main():
    ax = plt.gca()

    futSpot.plot(kind='scatter',x='date',y='ratioNormalizedFutSpot',ax=ax,s=1)
    # futSpotMinusOutlier.plot(kind='scatter',x='date',y='ratioNormalizedFutSpot',ax=ax,s=1)

    plt.show()

# main()

# maybe delete below this line

# # difference between spot and futures is in finance called "basis"
# futSpot["diffOpenXY"] = diffCol(futSpot,'open_x','open_y')
# futSpot["diffCloseXY"] = diffCol(futSpot,'close_x','close_y')
# futSpot["ratioDiffXY"] = divCol(futSpot,'diffOpenXY','diffCloseXY')

    # futSpot.plot(kind='scatter',x='date',y='ratioDiffXY',ax=ax,s=1)
    # futSpot.plot(kind='scatter',x='date',y='ratioDiffOpenClose',ax=ax,s=1)

    # futSpot.plot(kind='scatter',x='date',y='diffOpenXY',ax=ax)
    # futSpot.plot(kind='scatter',x='date',y='diffCloseXY', color='red', ax=ax)

    # # ok, could normalize
    # futSpot.plot(kind='scatter',x='date',y='diffOpenCloseX',ax=ax,s=1)
    # futSpot.plot(kind='scatter',x='date',y='diffOpenCloseY',color='red', ax=ax,s=1)

    # futSpot.plot(kind='scatter',x='date',y='open_x',ax=ax)
    # futSpot.plot(kind='scatter',x='date',y='open_y', color='red', ax=ax)


# # independent of below merger of the two csvs in futSpot
# # too bad these aren't actual indexes
# openCloseDiff = lambda d: diffCol(d,'open','close')
# highLowDiff = lambda d: diffCol(d,'high','low')
# currentStartStop = openCloseDiff(filteredSpotrent)
# futuresStartStop = openCloseDiff(futures)
