#!/usr/bin/env python3

import cudf
import pandas as pd
import pyarrow.orc
import time
import subprocess


class BaseManager:
    def __init__(self, inputOrcPath):
        self.inputOrcPath = inputOrcPath
        self.outputOrcPath = None

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
    def __init__(self, inputOrcPath):
        super().__init__(inputOrcPath)
        self.outputOrcPath = "subset_pandas_pyarrow.orc"
        print(f"pandas version: {pd.__version__}")

    def doIt(self):
        df = pd.read_orc(self.inputOrcPath)
        df.to_orc(self.outputOrcPath, engine="pyarrow",
                  engine_kwargs={"compression": "uncompressed"})


class CudfManager(BaseManager):
    def __init__(self, inputOrcPath):
        super().__init__(inputOrcPath)
        self.outputOrcPath = "subset_cudf.orc"
        print(f"cudf version: {cudf.__version__}")

    def doIt(self):
        df = cudf.read_orc(self.inputOrcPath)
        df.to_orc(self.outputOrcPath, compression=None)


class PyarrowManager(BaseManager):
    def __init__(self, inputOrcPath):
        super().__init__(inputOrcPath)
        self.outputOrcPath = "subset_pyarrow.orc"
        print(f"pyarrow version: {pyarrow.__version__}")

    def doIt(self):
        reader = pyarrow.orc.ORCFile(self.inputOrcPath)
        myDf = reader.read()

        writer = pyarrow.orc.ORCWriter(
            self.outputOrcPath, compression="uncompressed")
        writer.write(myDf)


if __name__ == "__main__":
    # orcPath = "col_b_only.orc"
    orcPath = "subset_col_b_only.orc"

    BaseManager.inspect(orcPath)

    managerList = [
        PandasManager(orcPath),
        CudfManager(orcPath),
        PyarrowManager(orcPath),
    ]
    for manager in managerList:
        manager.doIt()
        # BaseManager.inspect(manager.outputOrcPath)
