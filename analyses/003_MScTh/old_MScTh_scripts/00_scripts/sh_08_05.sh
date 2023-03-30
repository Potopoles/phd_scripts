#!/bin/bash


hydrometeors=('zQC' 'zQI' 'zQV' 'zQR' 'zQS' 'zQG')
TTendencies=('zATT_MIC' 'zATT_RAD' 'zATT_ADV' 'zATT_ZADV' 'zATT_TURB' 'zATT_TOT')
QVTendencies=('zAQVT_MIC' 'zAQVT_ADV' 'zAQVT_ZADV' 'zAQVT_TURB' 'zAQVT_TOT')
dynamics=('zW' 'zU' 'zV' 'zT')


for field in "${dynamics[@]}" 
do
    echo "#####################" $field "#########################"
    python -u -W ignore 00_scripts/08_05_freqDist_vert.py $field 
done
