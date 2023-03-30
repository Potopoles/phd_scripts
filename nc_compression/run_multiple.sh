#!/bin/bash

years=(2007 2008 2009)
months=(1 2 3 4 5 6 7 8 9 10 11 12)

#years=(2006)
#months=(9 10 11 12)

#### NOTE THIS IS REQUIRED TO COMPUTE THE WEIGHTS!!!
years=(2006)
months=(8)


for year in ${years[@]}; do
    echo $year
    for month in ${months[@]}; do
        echo $month
        sbatch submit.sbatch $year $month
    done
done
