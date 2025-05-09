#!/usr/bin/env bash

# References:
# https://orc.apache.org/specification/ORCv1/
# https://cwiki.apache.org/confluence/display/hive/languagemanual+orc

hadoop_dir=/home/biubiuty/biubiu/hadoop

export HADOOP_HOME=$hadoop_dir/hadoop-3.4.1

hive_bin=$hadoop_dir/apache-hive-4.0.1-bin/bin/hive

data_dir=data
# orc_file="$data_dir/good_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/special_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_2_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_3_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/ref.orc"
orc_file="$data_dir/chunked_read_simple_nullable.orc"

# -t: print the timezone id of the writer
# -j: print the ORC file metadata in JSON format
# -p: pretty print the JSON metadata
$hive_bin --orcfiledump -t -j -p $orc_file
