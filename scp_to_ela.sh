#!/bin/bash -   
#title          :scp_to_ela.sh
#description    :Copy a file arg1 to CSCS ela location arg2
#author         :Christoph Heim
#date           :20190319
#version        :1.00   
#usage          :./scp_to_ela.sh arg1 arg2
#notes          :       
#bash_version   :4.3.48(1)-release
#============================================================================

scp ${1} heimc@ela.cscs.ch:/${2}


