#!/bin/bash -   
#title          :setenv.sh
#description    :Set up environment variables for current analysis
#author         :Christoph Heim
#date           :20190319
#version        :1.00   
#usage          :source setenv.sh
#notes          :       
#bash_version   :4.3.48(1)-release
#============================================================================

source ../../global_env_daint.sh
source ~/scripts/load_modules.sh

# TIME INFORMATION
YEAR=2006
MONTH=07
DAY=*
HOUR=[0-9][0-9]
MODEL_NC_SEL=lffd${YEAR}${MONTH}${DAY}${HOUR}

# COPY INFORMATION
# model
SIM_NAMES=(MScTh)
#VAR_GROUPS=(mlev zlev const)
VAR_GROUPS=(mlev zlev const)
MODELS=(RAW4 SM4 RAW2 SM2 RAW1 SM1)

# DIRECTORIES
export ANA_NAME=003_MScTh
export ANA_DIR=$BASE_ANA_DIR/$ANA_NAME
export PLOT_DIR=$BASE_PLOT_DIR/$ANA_NAME
mkdir -p $ANA_DIR
mkdir -p $PLOT_DIR
