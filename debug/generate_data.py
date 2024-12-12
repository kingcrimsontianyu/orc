#!/usr/bin/env python3

import pandas as pd
import numpy as np
import datetime as dt


class Analyzer:
    def __init__(self, csvPath):
        self.csvPath = csvPath
        self.dfFull = None
        self.numRows = 200
        print("--> csvPath: {}".format(self.csvPath))

    def doIt(self):
        x = np.empty(self.numRows, dtype="datetime64[ms]")
        initialTime = np.datetime64("2000-01-21T03:30")
        deltaTime = np.timedelta64(1001, "ms")
        for idx in range(len(x)):
            x[idx] = initialTime + idx * deltaTime
        df = pd.DataFrame(data=x)
        df.to_csv(self.csvPath, header=False, index=False)


if __name__ == "__main__":
    csvPath = "sample.csv"
    aobj = Analyzer(csvPath)
    aobj.doIt()
