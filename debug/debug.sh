#!/usr/bin/env bash

my_debugger=gdb

root_dir=~/biubiu/debug_orc

orc_file=$root_dir/data/col_b_only.orc
# orc_file=$root_dir/data/first_27000_rows.orc
# orc_file=$root_dir/data/cudf_col_b_only.orc
# orc_file=$root_dir/data/mini.orc


orc_bin=$root_dir/orc/install-debug/bin/orc-contents
# $my_debugger -ex start -ex 'source breakpoints' --args $orc_bin $orc_file

# orc_bin=$root_dir/orc/install-debug/bin/orc-statistics
# $my_debugger -ex start -ex 'source row_idx_breakpoints' -args $orc_bin --withIndex $orc_file

# orc_bin=$root_dir/orc/install-debug/bin/orc-metadata
# $my_debugger -ex start --args $orc_bin -r -v $orc_file


$orc_bin $orc_file
