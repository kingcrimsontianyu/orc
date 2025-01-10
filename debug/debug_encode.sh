#!/usr/bin/env bash

my_debugger=gdb

root_dir=~/biubiu/debug_orc

# csv_file=timestamp_desync.csv
# orc_file=timestamp_desync_v1.orc
# orc_file=timestamp_desync_snappy_v1.orc

# csv_file=timestamp_desync.csv
# orc_file=timestamp_desync.orc
# orc_file=timestamp_desync_snappy.orc

csv_file=timestamp_desync_with_null.csv
orc_file=timestamp_desync_with_null.orc


# orc_file=$root_dir/data/first_27000_rows.orc
# orc_file=$root_dir/data/cudf_col_b_only.orc
# orc_file=$root_dir/data/mini.orc

# schema="struct<my_timestamp:timestamp,my_idx:int>"
schema="struct<my_timestamp:timestamp>"

orc_bin=$root_dir/orc/install-debug/bin/csv-import
# $my_debugger -ex start -ex 'source breakpoints_encode' --args $orc_bin $schema $csv_file $orc_file
$orc_bin $schema $csv_file $orc_file




