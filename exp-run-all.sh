#!/bin/sh

dataset=$1

sbatch exp-zs.sh $dataset 
sbatch exp-fs.sh $dataset 
sbatch exp-atzs.sh $dataset 
sbatch exp-atfs.sh $dataset 
sbatch exp-cotzs.sh $dataset 
sbatch exp-cotfs.sh $dataset 
sbatch exp-atcotzs.sh $dataset 
sbatch exp-atcotfs.sh $dataset 