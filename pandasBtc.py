import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

filteredCurrent = current.loc[current['date'].isin(futuresDates)]

# tests
testDates = np.all(futures.date.values == filteredCurrent.date.values) == True
testTestValid = np.all(np.array([False,True])) == False

# date,open,high,low,close,adjClose,volume
# def diffPrice(x,y):

def diffCol(d,x,y):
    return d[x] - d[y]

# too bad these aren't actual indexes
openCloseDiff = lambda d: diffCol(d,'open','close')
highLowDiff = lambda d: diffCol(d,'high','low')

currentStartStop = openCloseDiff(filteredCurrent)
futuresStartStop = openCloseDiff(futures)

# merge the tables, now x and y parameters
futCur = pd.merge(futures, filteredCurrent , on="date")

# diff1  = diffCol(futCur,'open_x','open_y')

futCur["diffOpenXY"] = diffCol(futCur,'open_x','open_y')
futCur["diffCloseXY"] = diffCol(futCur,'close_x','close_y')

futCur["diffOpenCloseX"] = diffCol(futCur,'open_x','close_x')
futCur["diffOpenCloseY"] = diffCol(futCur,'open_y','close_y')

# futCurDif = 

# df3.plot(x="open_x", y="B")

ax = plt.gca()

# futCur.plot(kind='scatter',x='date',y='diffOpenXY',ax=ax)
# futCur.plot(kind='scatter',x='date',y='diffCloseXY', color='red', ax=ax)

futCur.plot(kind='scatter',x='date',y='diffOpenCloseX',ax=ax)
futCur.plot(kind='scatter',x='date',y='diffOpenCloseY',color='red', ax=ax)

# futCur.plot(kind='scatter',x='date',y='open_x',ax=ax)
# futCur.plot(kind='scatter',x='date',y='open_y', color='red', ax=ax)


# diff1.plot

plt.show()

# def main():
#     ax = plt.gca()

#     futCur.plot(kind='line',x='date',y='open_x',ax=ax)
#     futCur.plot(kind='line',x='date',y='open_y', color='red', ax=ax)

#     plt.show()

# main()

# >>> diffCol(result,'open_x','open_y')

# example = currentStartStop / futuresStartStop --indexing issue

# def diffCol(d,x,y):
#     return d[x] - d[y]

# def openClose(d):
#     return lamba x : 


