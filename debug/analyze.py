#!/usr/bin/env python3

# References:
# https://github.com/rapidsai/cudf/issues/17155
#
# In the shell, export KVIKIO_COMPAT_MODE=ON
#
# Col 'a' is the same for pandas and cudf.
# Col 'b' starts to differ at row 630107.

import pandas as pd
import numpy as np
import datetime as dt


class Analyzer:
    def __init__(self, csvPath):
        self.csvPath = csvPath
        self.dfFull = None
        print("--> orcPath: {}".format(csvPath))

    def doIt(self):
        df = pd.read_csv(
            csvPath,
            names=["batch_idx", "run_length", "encoding_scheme", "timestamp_component"],
        )
        df["encoding_scheme"] = df["encoding_scheme"].astype("category")
        df["timestamp_component"] = df["timestamp_component"].astype("category")
        dfSec = df.loc[df["timestamp_component"] == "SECOND"]
        dfNano = df.loc[df["timestamp_component"] == "NANO"]

        print("--> sec")
        self.summarize(dfSec)

        print("--> nano")
        self.summarize(dfNano)

    def summarize(self, df):
        print("    sum: {}".format(df["run_length"].sum()))
        print("{}".format(df.to_string()))


if __name__ == "__main__":
    csvPath = "orc_ref.csv"
    aobj = Analyzer(csvPath)
    aobj.doIt()
