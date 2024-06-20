#!/bin/bash
#SBATCH --partition=funky
#SBATCH --nodelist=rodgers
#SBATCH --job-name=aczs
#SBATCH --nodes=1
#SBATCH --time=7200
#SBATCH --gpus-per-node=1
#SBATCH --output=at-cot-zs.out
#SBATCH --error=at-cot-zs.err

dataset=$1

srun python3 prompting.py --dataset_name $dataset --prompt_type AT-CoT-zero-shot --model_name meta-llama/Meta-Llama-3-8B-Instruct
#meta-llama/Llama-2-13b-chat-hf
#meta-llama/Llama-2-13b-chat-hf
