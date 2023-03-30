import os, subprocess, argparse
from pathlib import Path
from package.mp import IterMP

var_names_cg = [
    'T_S', 'ALHFL_S', 'ASHFL_S',
    'U_10M', 'V_10M', 'T_2M', 'QV_2M', 'PS',
    'CAPE_ML', 'CIN_ML', 
    'ASOB_T',
    'ASOD_T',
    'ATHB_T',
    'ASOBC_T',
    'ATHBC_T',
    'ASOBC_S',
    'ATHBC_S',
    'ASOB_S',
    'ASWDIFD_S',
    'ASWDIR_S',
    'ATHB_S',
    'ATHD_S',
]

var_names_nocg = [
    #'TQI',
    'TQV', 'TQR', 'TQS', 'TQG',
    'CLCL', 'CLCM', 'CLCH'
]

def process(file):
    print(file)
    inp_path = os.path.join(inp_dir, file)

    # coarse-grain
    out_path = os.path.join(out_dir_cg, file)
    var_name_str = ','.join(var_names_cg)
    cmd = 'ncks -v {} {} {}'.format(var_name_str, inp_path, out_path)
    subprocess.call(cmd, shell=True)

    # no coarse-grain
    out_path = os.path.join(out_dir_nocg, file)
    var_name_str = ','.join(var_names_nocg)
    cmd = 'ncks -v {} {} {}'.format(var_name_str, inp_path, out_path)
    subprocess.call(cmd, shell=True)

if __name__ == '__main__':

    ## input arguments
    parser = argparse.ArgumentParser(description = 'Compress files.')
    parser.add_argument('year', type=str)
    parser.add_argument('-p', '--n_par', type=int, default=1)
    args = parser.parse_args()

    base_dir = '/scratch/snx3000/heimc/data/compr_cosmo/SA_3_ctrl/lm_c'


    inp_dir = os.path.join(base_dir, '1h_2D', args.year)
    out_dir_cg = os.path.join(base_dir, '1h_2D_cg', args.year)
    out_dir_nocg = os.path.join(base_dir, '1h_2D_nocg', args.year)

    Path(out_dir_cg).mkdir(parents=True, exist_ok=True)
    Path(out_dir_nocg).mkdir(parents=True, exist_ok=True)

    
    IMP = IterMP(njobs=args.n_par, run_async=False)
    step_args = []

    for file in os.listdir(inp_dir):
        step_args.append(dict(file=file))

    IMP.run(process, {}, step_args)


    #quit()
