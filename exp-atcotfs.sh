#!/bin/bash
#SBATCH --partition=funky
#SBATCH --nodelist=edwards
#SBATCH --job-name=b-atcotfs
#SBATCH --nodes=1
#SBATCH --time=7200
#SBATCH --gpus-per-node=1
#SBATCH --output=b-atcotfs.out
#SBATCH --error=b-atcotfs.err

dataset=$1

srun python3 prompting.py --dataset_name $dataset --prompt_type AT-CoT-few-shot --model_name meta-llama/Meta-Llama-3-8B-Instruct
#meta-llama/Llama-2-13b-chat-hf
#meta-llama/Llama-2-13b-chat-hf
