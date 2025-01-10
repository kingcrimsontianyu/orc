#!/usr/bin/env python3

# References:
# https://github.com/rapidsai/cudf/issues/17155

import pandas as pd
import cudf
import numpy as np
import datetime as dt


class CompareManager:
    def __init__(self, orcPath):
        self.orcPath = orcPath
        self.dfFull = None
        print("cuDF version: {}".format(cudf.__version__))
        print("--> orcPath: {}".format(orcPath))

    # Reference: https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.timestamp.html#pandas.Timestamp.timestamp
    def getTime(self, timeStamp):
        if isinstance(timeStamp, pd.Timestamp):
            npTimeStamp = timeStamp.to_numpy()
        elif isinstance(timeStamp, np.datetime64):
            npTimeStamp = timeStamp

        tmp1 = npTimeStamp.astype("datetime64[ns]").astype("int")
        epochTimeElapsedSec = tmp1 // 1e9
        epochTimeElapsedNano = tmp1 / 1e9 - tmp1 // 1e9

        tmp2 = npTimeStamp - np.datetime64("2015-01-01")
        orcTimeElapsedSec = tmp2 // np.timedelta64(1, "s")
        orcTimeElapsedNano = tmp2 / np.timedelta64(1, "s") - orcTimeElapsedSec

        return (
            epochTimeElapsedSec,
            epochTimeElapsedNano,
            orcTimeElapsedSec,
            orcTimeElapsedNano,
        )

    def doIt(self):
        pdDf = pd.read_orc(self.orcPath)
        cfDf = cudf.read_orc(self.orcPath, engine="cudf")

        print(pdDf.shape)
        print(cfDf.shape)

        print(pdDf)
        print(cfDf)


if __name__ == "__main__":
    # orcPath = "timestamp_desync_with_null.orc"

    # orcPath = "TestOrcFile.timestamp.desynced.snappy.RLEv2.hasNull.orc"

    targetDir = "/home/biubiuty/biubiu/rapids/cudf/python/cudf/cudf/tests/data/orc/"
    orcPath = targetDir + "TestOrcFile.timestamp.desynced.snappy.RLEv2.hasNull.orc"

    cmObj = CompareManager(orcPath)
    cmObj.doIt()
