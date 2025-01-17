#!/usr/bin/env python3

import cudf
import pandas as pd
import pyarrow.orc
import time
import subprocess


class BaseManager:
    def __init__(self, inputOrcPath, outputOrcPath=None):
        self.inputOrcPath = inputOrcPath
        self.outputOrcPath = outputOrcPath

    @staticmethod
    def inspect(filePath):
        print(f"\n--> orcPath: {filePath}")
        reader = pyarrow.orc.ORCFile(filePath)
        print(f"file_version: {reader.file_version}")
        print(f"software_version: {reader.software_version}")
        print(f"writer: {reader.writer}")
        print(f"writer_version: {reader.writer_version}")

        # orcBin = "~/biubiu/debug_orc/orc/install-debug/bin/orc-contents"
        # full_command = f"{orcBin} {filePath}"
        # print(f"Full command: {full_command}")
        # subprocess.run([full_command], shell=True)


class PandasManager(BaseManager):
    def __init__(self, inputOrcPath, outputOrcPath):
        super().__init__(inputOrcPath, outputOrcPath)
        print(f"pandas version: {pd.__version__}")

    def doIt(self):
        df = pd.read_orc(self.inputOrcPath)
        df.to_orc(
            self.outputOrcPath,
            engine="pyarrow",
            engine_kwargs={"compression": "uncompressed"},
        )
        print(df)


class CudfManager(BaseManager):
    def __init__(self, inputOrcPath, outputOrcPath):
        super().__init__(inputOrcPath, outputOrcPath)
        print(f"cudf version: {cudf.__version__}")

    def doIt(self):
        df = cudf.read_orc(self.inputOrcPath)
        df.to_orc(self.outputOrcPath, compression=None)
        print(df)


class PyarrowManager(BaseManager):
    def __init__(self, inputOrcPath, outputOrcPath):
        super().__init__(inputOrcPath, outputOrcPath)
        print(f"pyarrow version: {pyarrow.__version__}")

    def doIt(self):
        reader = pyarrow.orc.ORCFile(self.inputOrcPath)
        myDf = reader.read()

        writer = pyarrow.orc.ORCWriter(self.outputOrcPath, compression="uncompressed")
        writer.write(myDf)
        print(myDf)


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

    BaseManager.inspect(orcInputPath)

    managerList = [
        CudfManager(orcInputPath, orcOutputPathList[0]),
        PandasManager(orcInputPath, orcOutputPathList[1]),
        PyarrowManager(orcInputPath, orcOutputPathList[2]),
    ]
    for manager in managerList:
        manager.doIt()
        # BaseManager.inspect(manager.outputOrcPath)
