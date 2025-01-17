#!/usr/bin/env python3

import pandas as pd
import pyarrow.orc
import time
import subprocess
import pathlib


class Inspector:
    def __init__(self, inputOrcPath):
        self.inputOrcPath = inputOrcPath
        self.orcBin = "{}/biubiu/debug_orc/orc/install-debug/bin/orc-contents".format(
            pathlib.Path.home()
        )

    def inspect(self):
        print(f"\n--> orcPath: {self.inputOrcPath}")
        reader = pyarrow.orc.ORCFile(self.inputOrcPath)
        print("compression: {}".format(reader.compression))
        print(f"file_version: {reader.file_version}")
        print("compression_size: {}".format(reader.compression_size))
        print(f"software_version: {reader.software_version}")
        # print(f"writer: {reader.writer}")
        print(f"writer_version: {reader.writer_version}")
        print("row_index_stride: {}".format(reader.row_index_stride))

        full_command = f"{self.orcBin} {self.inputOrcPath}"
        print(f"Full command: {full_command}")
        subprocess.run(full_command.split())


if __name__ == "__main__":
    orcPathList = ["subset_cudf.orc", "subset_pandas_pyarrow.orc", "subset_pyarrow.orc"]

    for orcPath in orcPathList:
        ins = Inspector(orcPath)
        ins.inspect()
