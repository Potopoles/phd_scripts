#!/bin/csh
#!/bin/bash




module load daint-gpu
module load NCL


#set DD_all = (01 02)
#set HH_all = (00 01 02)


set str_resol = 'resol="12km"'
set str_conv = 'conv="PARAM"'

set str_sim = 'sim="Atlantic_ppcc_PARAM_subhourly"'



set DD_all = ('dd="10"' 'dd="11"' 'dd="12"' 'dd="13"' 'dd="14"' 'dd="15"' 'dd="16"' 'dd="17"' 'dd="18"' 'dd="19"')

set HH_all = ('hh="00"' 'hh="01"' 'hh="02"' 'hh="03"' 'hh="04"' 'hh="05"' 'hh="06"' 'hh="07"' 'hh="08"' 'hh="09"' 'hh="10"' 'hh="11"' 'hh="12"' 'hh="13"' 'hh="14"' 'hh="15"' 'hh="16"' 'hh="17"' 'hh="18"' 'hh="19"' 'hh="20"' 'hh="21"' 'hh="22"' 'hh="23"')

set MMIN_all = ('mmin="00"' 'mmin="15"' 'mmin="30"' 'mmin="45"')

foreach str_dd ($DD_all)
foreach str_hh ($HH_all)
foreach str_mmin ($MMIN_all)
    ncl $str_resol $str_conv $str_sim  $str_dd $str_hh $str_mmin maps_movies.ncl
end
end
end


module unload NCL
module unload daint-gpu
