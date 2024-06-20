#!/bin/bash
#SBATCH --partition=funky 
#SBATCH --nodelist=edwards
#SBATCH --job-name=cotfs
#SBATCH --nodes=1
#SBATCH --time=7200
#SBATCH --gpus-per-node=1
#SBATCH --output=cotfs.out
#SBATCH --error=cotfs.err

dataset=$1

srun python3 prompting.py --dataset_name $dataset --prompt_type CoT-few-shot --model_name meta-llama/Meta-Llama-3-8B-Instruct
#meta-llama/Llama-2-13b-chat-hf
#meta-llama/Llama-2-7b-chat-hf
