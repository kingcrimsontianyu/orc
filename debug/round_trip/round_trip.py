#!/usr/bin/env python3

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

        orcBin = "~/biubiu/debug_orc/orc/install-debug/bin/orc-contents"
        full_command = f"{orcBin} {filePath}"
        print(f"Full command: {full_command}")
        subprocess.run([full_command], shell=True)


class PandasManager(BaseManager):
    def __init__(self, inputOrcPath):
        super().__init__(inputOrcPath)
        self.outputOrcPath = "pandas_pyarrow.orc"

    def doIt(self):
        df = pd.read_orc(self.inputOrcPath)
        df.to_orc(self.outputOrcPath, engine="pyarrow")


# import cudf


# class CudfManager(BaseManager):
#     def __init__(self, inputOrcPath):
#         super().__init__(inputOrcPath)
#         self.outputOrcPath = "cudf.orc"

#     def doIt(self):
#         df = cudf.read_orc(self.inputOrcPath)
#         df.to_orc(self.outputOrcPath)


class PyarrowManager(BaseManager):
    def __init__(self, inputOrcPath):
        super().__init__(inputOrcPath)
        self.outputOrcPath = "pyarrow.orc"

    def doIt(self):
        reader = pyarrow.orc.ORCFile(self.inputOrcPath)
        myDf = reader.read()

        writer = pyarrow.orc.ORCWriter(self.outputOrcPath)
        writer.write(myDf)


if __name__ == "__main__":
    orcPath = "timestamp_bug.snappy.orc"

    BaseManager.inspect(orcPath)

    managerList = [
        PandasManager(orcPath),
        # CudfManager(orcPath),
        PyarrowManager(orcPath),
    ]
    for manager in managerList:
        manager.doIt()
        BaseManager.inspect(manager.outputOrcPath)
