#!/usr/bin/env bash

# References:
# https://orc.apache.org/specification/ORCv1/
# https://cwiki.apache.org/confluence/display/hive/languagemanual+orc

orc_root=../../install-debug/bin

data_dir=data
# orc_file="$data_dir/good_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/special_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_2_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/bad_3_OrcEmptyRowGroup.orc"
# orc_file="$data_dir/ref.orc"
# orc_file="$data_dir/ref.orc"
orc_file="$data_dir/chunked_read_simple_nullable.orc"

$orc_root/orc-contents $orc_file

# withIndex: include column statistics in each row group
# $orc_root/orc-statistics --withIndex $orc_file

# $orc_root/orc-metadata -r -v $orc_file
