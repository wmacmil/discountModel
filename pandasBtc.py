import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# current := spot
# parse_dates gives pandas internal date representation
futures = pd.read_csv('f.csv',parse_dates=['date'])
current = pd.read_csv('c.csv',parse_dates=['date'])

futuresDates = futures["date"]

# only keep those entries which satisfy isInFutureDates(x) predicate, see link for solution
# https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values
def isInFutureDates(x):
    for y in futuresDates:
        if x == y:
            return True

filteredSpotrent = current.loc[current['date'].isin(futuresDates)]

# tests
testDates = np.all(futures.date.values == filteredSpotrent.date.values) == True
testTestValid = np.all(np.array([False,True])) == False

# date,open,high,low,close,adjClose,volume
# def diffPrice(x,y):

def diffCol(d,x,y):
    return d[x] - d[y]

def divCol(d,x,y):
    return d[x] / d[y]


# merge the tables, now x and y parameters
futSpot = pd.merge(futures, filteredSpotrent , on="date")


# # difference between spot and futures is in finance called "basis"
# futSpot["diffOpenXY"] = diffCol(futSpot,'open_x','open_y')
# futSpot["diffCloseXY"] = diffCol(futSpot,'close_x','close_y')
# futSpot["ratioDiffXY"] = divCol(futSpot,'diffOpenXY','diffCloseXY')

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


def main():
    ax = plt.gca()

    futSpot.plot(kind='scatter',x='date',y='ratioNormalizedFutSpot',ax=ax,s=1)

    # finding the outlier
    # futSpot[futSpot.ratioNormalizedFutSpot == futSpot.ratioNormalizedFutSpot.min()]

    plt.show()

main()

# maybe delete

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
