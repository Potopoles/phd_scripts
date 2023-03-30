#!/bin/bash -   
#title          :scp_from_ela.sh
#description    :Copy a file arg1 from CSCS ela to local location arg2
#author         :Christoph Heim
#date           :20190319
#version        :1.00   
#usage          :./scp_from_ela.sh arg1 arg2
#notes          :       
#bash_version   :4.3.48(1)-release
#============================================================================

scp heimc@ela.cscs.ch:/${1} ${2}


