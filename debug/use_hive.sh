#!/usr/bin/env bash

# References:
# https://orc.apache.org/specification/ORCv1/
# https://cwiki.apache.org/confluence/display/hive/languagemanual+orc

hadoop_dir=/home/biubiuty/biubiu/hadoop

export HADOOP_HOME=$hadoop_dir/hadoop-3.4.1

hive_bin=$hadoop_dir/apache-hive-4.0.1-bin/bin/hive

# orc_file=data/generated_data_pyarrow.orc
# orc_file=data/col_b_only.orc
# orc_file=data/cudf_col_b_only.orc
# orc_file=data/timestamp_bug.snappy.orc
# orc_file=sample.orc
# orc_file=sample_csvImport.orc
# orc_file=sampleWithNull.orc
# orc_file=timestamp_desync.orc
# orc_file=timestamp_desync_v1.orc
# orc_file=timestamp_desync_snappy.orc
# orc_file=timestamp_desync_with_null_ref.orc
# orc_file=timestamp_desync_with_null.orc
# orc_file=/home/biubiuty/biubiu/rapids/cudf/python/cudf/cudf/tests/data/orc/TestOrcFile.timestamp.desynced.snappy.RLEv2.orc
orc_file="round_trip/timestamp_bug.snappy.orc"

# -t: print the timezone id of the writer
# -j: print the ORC file metadata in JSON format
# -p: pretty print the JSON metadata
$hive_bin --orcfiledump -t -j -p $orc_file
