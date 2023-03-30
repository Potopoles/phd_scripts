#!/bin/bash -l
#SBATCH --job-name="ext"
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=12
#SBATCH --partition=debug
#SBATCH --ntasks=1
#SBATCH --account='pr133'
#SBATCH --constraint=gpu
#SBATCH --output=bOut/out0
#SBATCH --error=bOut/err0
month=1
year=2007
#year=2008
#year=2009
#year=2010

#var_names=CLCL,CLCM,CLCH,LWUTOA,CLWUTOA,SWNDTOA,SWDTOA,CSWNDTOA,TSURF,PP,QC,QI,T,QV,U,V,W,P,CAPE,TQC,TQI,TQV,WSOIL,U10M,V10M,T2M,SLHFLX,SSHFLX,CIN,CLCT,TQR,TQG,TQS,TSOIL
#
#var_names=LWNDSFC,LWDSFC,CLWNDSFC

#var_names=LWUTOA,CLWUTOA,SWNDTOA,SWDTOA,CSWNDTOA,TSURF,PP
#var_names=QC
#var_names=QI
#var_names=T
###var_names=QV
#var_names=U
#var_names=V
#var_names=W
###var_names=P
#var_names=CAPE,CLCL
#var_names=CLCM,CLCH
#var_names=TQC,TQI
#var_names=TQV,WSOIL,U10M,V10M
#var_names=T2M,SLHFLX,SSHFLX,CIN,CLCT
#var_names=TQR,TQG
#var_names=TQS,TSOIL


var_names=LWUTOA,CLWUTOA,SWNDTOA,SWDTOA,CSWNDTOA
#var_names=PP,QC,QI,TQC,TQI,TQV
#var_names=WSOIL,U10M,V10M,T2M,TSURF,SLHFLX,SSHFLX,CAPE,CIN,CLCL,CLCM,CLCH,CLCT
#var_names=TQR,TQG,TQS,T,QV,U,V,W,P,TSOIL



### 2D coarse grain & lossy compression
#var_names=SWNDTOA,SWDTOA,LWUTOA,CSWNDTOA,CLWUTOA,U10M,V10M,T2M,TSURF,SLHFLX,SSHFLX
### 2D no coarse grain & lossy compression
## !!! CLCT!!!
#var_names=CLCL,CLCM,CLCH,CLCT,TQC,PP,TQI,TQR,TQG,TQS,TQV
### 3D coarse grain & lossy compression
#var_names=T,QV,U,V,W,P,QC,QI
### 3D no coarse grain & no lossy compression
#var_names=TSOIL,WSOIL


source ../load_modules_daint.sh
module load CDO
echo -e "$SLURM_JOB_NAME $SLURM_JOB_ID started on $(date):\n $command $1 $2\n"


#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK SA_3_ctrl_4dx -y $year -v $var_names -m $month
srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
                -p $SLURM_CPUS_PER_TASK SA_3_ctrl_4dxL -y $year -v $var_names -m $month

#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK SA_3_pgw3 -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK SA_3_ctrl -y $year -v $var_names #-m $month

#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_41_4.4km -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_42_4.4km -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_43_4.4km -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_44_4.4km -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_45_4.4km -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_46_4.4km -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_47_4.4km -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_48_4.4km -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_49_4.4km -y $year -v $var_names #-m $month
#srun -c $SLURM_CPUS_PER_TASK python -u extract_case.py \
#                -p $SLURM_CPUS_PER_TASK test_50_4.4km -y $year -v $var_names #-m $month

echo -e "$SLURM_JOB_NAME $SLURM_JOB_ID finished on $(date)\n"
