#!/bin/bash
#srun --partition=dev -c24 --nodelist=keschcn-0003 -t10:00:00 --pty /bin/bash
#srun --partition=postproc -c1 -t1:00:00 --pty bash

salloc -C gpu --account='pr04' --partition=normal --time=5:00:00
