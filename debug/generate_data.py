#!/usr/bin/env python3

import pandas as pd
import numpy as np
import datetime as dt
import csv


class Analyzer:
    def __init__(self, csvPath, orcPath, hasNull, includeMyIdx):
        """
        hasNull: even row is replaced by null
        includeMyIdx: include an integer column "my_idx"
        """
        self.csvPath = csvPath
        self.orcPath = orcPath
        self.hasNull = hasNull
        self.includeMyIdx = includeMyIdx
        self.dfFull = None
        self.numRows = 2660
        print("--> csvPath: {}".format(self.csvPath))

    def doIt(self):
        x = np.empty(self.numRows, dtype="datetime64[us]")
        y = np.empty(self.numRows, dtype=np.int32)
        initialTime = np.datetime64("2000-01-21T03:30")
        deltaTime = np.timedelta64(1000001, "us")
        for idx in range(len(x)):
            if self.hasNull and idx % 100 == 0:
                x[idx] = np.datetime64("nat")
            else:
                x[idx] = initialTime + idx * deltaTime

            y[idx] = idx

        if self.includeMyIdx:
            myDict = {"my_timestamp": x, "my_idx": y}
        else:
            myDict = {"my_timestamp": x}
        df = pd.DataFrame(myDict)

        df.to_csv(self.csvPath, header=False, index=False)

        # Reduce the row group size!!!
        # df.to_orc(self.orcPath, engine_kwargs={"row_index_stride": 1536})


if __name__ == "__main__":
    # csvPath = "timestamp_desync.csv"
    # orcPath = "timestamp_desync_ref.orc"
    # hasNull = False
    # includeMyIdx = False

    csvPath = "timestamp_desync_with_null.csv"
    orcPath = "timestamp_desync_with_null_ref.orc"
    hasNull = True
    includeMyIdx = False

    aobj = Analyzer(csvPath, orcPath, hasNull, includeMyIdx)
    aobj.doIt()
