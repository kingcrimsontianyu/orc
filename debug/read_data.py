#!/usr/bin/env python3

import pyarrow.orc
import pandas as pd


class PyarrowManager:
    def __init__(self, orcPath):
        self.orcPath = orcPath
        self.dfFull = None
        print("--> orcPath: {}".format(orcPath))

    def doIt(self):
        of = pyarrow.orc.ORCFile(self.orcPath)

        # Compression codec of the file
        print("compression: {}".format(of.compression))

        # Format version of the ORC file, must be 0.11 or 0.12
        print("file_version: {}".format(of.file_version))

        # Number of bytes to buffer for the compression codec in the file
        print("compression_size: {}".format(of.compression_size))

        # Length of the data stripes in the file in bytes
        print("content_length: {}".format(of.content_length))

        # Number of rows per entry in the row index
        print("row_index_stride: {}".format(of.row_index_stride))

        tb = of.read()
        df = tb.to_pandas()
        print(df)


if __name__ == "__main__":
    # orcPath = "timestamp_desync.orc"
    # orcPath = "timestamp_desync_snappy.orc"
    # orcPath = "timestamp_desync_v1.orc"
    # orcPath = "timestamp_desync_snappy_v1.orc"

    targetDir = "/home/biubiuty/biubiu/rapids/cudf/python/cudf/cudf/tests/data/orc/"
    # orcPath = targetDir + "TestOrcFile.timestamp.desynced.uncompressed.RLEv1.orc"
    # orcPath = targetDir + "TestOrcFile.timestamp.desynced.snappy.RLEv1.orc"
    # orcPath = targetDir + "TestOrcFile.timestamp.desynced.uncompressed.RLEv2.orc"
    orcPath = targetDir + "TestOrcFile.timestamp.desynced.snappy.RLEv2.orc"

    paObj = PyarrowManager(orcPath)
    paObj.doIt()
