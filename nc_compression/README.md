# nc_compression

Python scripts to compress COSMO output NC files using the tool nczip by Urs Beyerle.  
Allows for parallel execution.  
nczip is based on the NCO command ncqs.  
Scripts were tested with python 3.7.7.  

Usage:
1)  If necessary, copy COSMO output from project to scratch.  
        Scripts assume that COSMO output to compress is stored under:  
            `$work_dir/$simulation/$output_group`  
            example of input arguments:  
                `$work_dir=/scratch/snx3000/heimc/data/compr_cosmo`  
                `$simulation=SA_12`  
                `$output_group=1h_2D`   
            like this, `run_compression.py` assumes that under:  
            `/scratch/snx3000/heimc/data/compr_cosmo/SA_12/1h_2D`  
            it will find the `lffd...` files to compress.  
2)  Set `$work_dir` variable in the `namelist.py`.
3)  prepare batch job in `submit.sbatch` by adjusting the input arguments:    
        **1st:** (`$n_workers`) number of workers for parallel execution  
        **2nd:** (`$simulation`) subdirectory path to simulation output groups  
        **3rd:** (`$output_group`) COSMO output groups to compress (separated by `,` if multiple output groups should be compressed)  
4)  submit batch job.



