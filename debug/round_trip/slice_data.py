#!/usr/bin/env python3

import pandas as pd


class PandasManager:
    def __init__(self, orcPath, isSubset):
        self.orcPath = orcPath
        self.isSubset = isSubset
        print("--> orcPath: {}".format(orcPath))

    def subSetByCol(self):
        df = pd.read_orc(self.orcPath)

        df = df[["b"]]

        if self.isSubset:
            df = df[620000:]
            df = df.reset_index(drop=True)

        outputPath = "col_b_only.orc"
        if self.isSubset:
            outputPath = "subset_" + outputPath

        df.to_orc(outputPath, engine_kwargs={"compression": "UNCOMPRESSED"})

        df = pd.read_orc(outputPath)
        print(df)


if __name__ == "__main__":
    orcPath = "timestamp_bug.snappy.orc"
    isSubset = False

    pdObj = PandasManager(orcPath, isSubset)
    pdObj.subSetByCol()
