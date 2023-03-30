#!/bin/bash


salloc --job-name="salloc" --time=0:30:00 --cpus-per-task=12 \
    --account='pr04' --constraint=gpu --partition=debug




