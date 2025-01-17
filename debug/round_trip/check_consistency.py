#!/usr/bin/env python3

import cudf
import pandas as pd
import pyarrow.orc


class Checker:
    def __init__(self, orcInputPath, orcOutputPath):
        self.orcInputPath = orcInputPath
        self.orcOutputPath = orcOutputPath

    def check(self):
        dfInput = pd.read_orc(self.orcInputPath)
        dfOutput = pd.read_orc(self.orcInputPath)
        print(f"--> input: {self.orcInputPath}")
        print(f"    output: {self.orcOutputPath}")
        print(f"    equal?: {dfInput.equals(dfOutput)}")


if __name__ == "__main__":
    orcInputPath = "col_b_only.orc"
    orcOutputPathList = [
        "cudf.orc",
        "pandas_pyarrow.orc",
        "pyarrow.orc",
    ]

    # orcInputPath = "subset_col_b_only.orc"
    # orcOutputPathList = [
    #     "subset_cudf.orc",
    #     "subset_pandas_pyarrow.orc",
    #     "subset_pyarrow.orc",
    # ]

    for orcOutputPath in orcOutputPathList:
        ins = Checker(orcInputPath, orcOutputPath)
        ins.check()
