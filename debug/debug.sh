#!/usr/bin/env bash

my_debugger=gdb

orc_root=../../install-debug/bin
my_program=$orc_root/orc-contents

data_dir=data
# orc_file="$data_dir/good_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/special_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_2_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_3_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_4_OrcEmptyRowGroup.orc"
orc_file="$data_dir/chunked_read_simple_nullable.orc"

# $my_debugger -ex start --ex 'source breakpoints_contents.txt' --args $my_program $orc_file

$my_program $orc_file