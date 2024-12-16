#!/usr/bin/env python3

import pandas as pd
import numpy as np
import datetime as dt


class Analyzer:
    def __init__(self, csvPath):
        self.csvPath = csvPath

    def doIt(self):
        df = pd.read_csv(self.csvPath, header=None)
        print(df)


if __name__ == "__main__":
    csvPath = "sampleWithNull.csv"

    aobj = Analyzer(csvPath)
    aobj.doIt()
