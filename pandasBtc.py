import pandas as pd
import numpy as np

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
