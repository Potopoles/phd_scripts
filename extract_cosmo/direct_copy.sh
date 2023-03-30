#!/bin/bash


src_files=$1
dest_path=$2
refresh=$3

#echo $src_files
#echo
#echo $dest_path
#echo 

#[ -d $dest_path ] && echo exists
#[[ "$refresh" == 1 ]] && echo refresh
if [ "$refresh" == 1 ] && [ -d $dest_path ]; then
    rm -r $dest_path
fi
mkdir -p $dest_path
cp -u $src_files $dest_path
