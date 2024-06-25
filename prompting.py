import os
import time
import numpy as np
import pandas as pd
import json
import pickle
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from opt import get_args

if __name__ == "__main__":
    args = get_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    model_id = args.model_name

    tokenizer = AutoTokenizer.from_pretrained(model_id,padding_side="left")
    tokenizer.pad_token_id = tokenizer.eos_token_id

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )

    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        batch_size=args.batch_size
    )

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    prompts = json.load(open(os.path.join(args.data_dir,"prompts.json")))
    prompt = prompts[args.prompt_type]
   

    df = pd.read_csv(os.path.join(args.data_dir,f"df_{args.dataset_name}.csv"))
    queries = list(df.q.unique())
    
    if args.dry_run:
        queries = queries[:2]

    ps = []
    for q in queries:
        p = prompt.replace("{{REQUETE}}",q)
        ps.append(p)

    start_time = time.time()

    outputs = pipeline(
        ps,
        max_new_tokens=2000,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_k=10,
    )

    end_time = time.time()

    print(f"time elapsed: {end_time-start_time} s: {args.dataset_name}; {args.prompt_type}")

    with open(os.path.join(args.output_dir,f"response_{args.dataset_name}_{args.prompt_type}.pkl"),"wb") as f:
        pickle.dump(outputs,f,pickle.HIGHEST_PROTOCOL)

