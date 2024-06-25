import os
import re
import numpy as np
import pandas as pd
import json
import pickle
from opt import get_args

def extract_indexes(s):
    matches = re.findall(r"\((.*?)\)",s)
    indexes = []
    for match in matches:
        if match.isdigit():
            indexes.append(int(match))
    if len(indexes) != 5:
        print("WARNING: # CQ != 5.")
    return sorted(indexes)

def extract_cqs(s,indexes):
    cqs =  []
    for i in range(len(indexes)-1):
        cqs.append(re.search(rf"\({indexes[i]}\)(.*?)\({indexes[i+1]}\)",s).group(1).strip('\n').strip())
    last_ph = f"({indexes[-1]})"
    cqs.append(s[s.index(last_ph)+len(last_ph):].strip('\n').strip())
    return cqs

def clean_text(s,s_index):
    cqs = []
    if s.count("[QC]")  == 1 and s.count("[/QC]") == 1:
        s = re.findall(r"\[QC\](.*?)\[\/QC\]",s.replace('\n',''))[0]
        indexes = extract_indexes(s)
        if indexes:
            cqs = extract_cqs(s,indexes)
    elif "[QC]" in s and "[/QC]" in s:
        # if multiple marker pairs exist, hypothesize that LLM repeats some input and the last occurence is the valid output.
        s = re.findall(r"\[QC\](.*?)\[\/QC\]",s.replace('\n',''))[-1]
        indexes = extract_indexes(s)
        if indexes:
            cqs = extract_cqs(s,indexes)
    elif "il n'y a pas besoin de clarification" in s.lower():
        cqs = ["[unambiguous]"]
    else:
        print(f"ERROR markers not found: {s_index}")
    return cqs

def clean(docs):
    res = []
    for ix, doc in enumerate(docs):
        s = doc[0]["generated_text"].split("assistant<|end_header_id|>")[1].strip("\n").strip()
        res.append(clean_text(s,ix))
    return res

def generate_csv(qs,cqs):
    copied_qs, copied_cqs = [], []
    for q, tmp_cqs in zip(qs,cqs):
        copied_qs += [q] * len(tmp_cqs)
        copied_cqs += tmp_cqs
    df_res = pd.DataFrame({"q":copied_qs,"cq1":copied_cqs})
    return df_res

if __name__ == "__main__":
    args = get_args()

    generated_docs = pickle.load(open(os.path.join(args.output_dir,f"response_{args.dataset_name}_{args.prompt_type}.pkl"),"rb"))
    cqs = clean(generated_docs)

    n_failure, n_unambiguous, n_cqs_extracted = list(map(len,cqs)).count(0), list(map(len,cqs)).count(1), list(map(len,cqs)).count(5)
    print(f"processing finished: ")
    print(f"\t # failures: {n_failure}.")
    print(f"\t # unambiguous: {n_unambiguous}.")
    print(f"\t # 5 CQs extracted: {n_cqs_extracted}.")

    if n_failure + n_unambiguous + n_cqs_extracted != len(cqs):
        print(f"\t abnormal cases: {len(cqs)-n_failure-n_unambiguous-n_cqs_extracted}.")

    dst_pkl_file_path = os.path.join(args.output_dir,f"cqs_{args.dataset_name}_{args.prompt_type}.pkl")
    with open(dst_pkl_file_path,"wb") as f:
        pickle.dump(cqs,f,pickle.HIGHEST_PROTOCOL)

    print(f"results saved as a pkl file: {dst_pkl_file_path}")

    if args.save_as_csv:
        df = pd.read_csv(os.path.join(args.data_dir,f"df_{args.dataset_name}.csv"))
        qs = df.q.values
        assert len(qs) == len(cqs), "number of original queries and set of clarification questions NOT equal."

        df_cqs = generate_csv(qs,cqs)
        dst_csv_file_path = os.path.join(args.output_dir,f"df_cqs_{args.dataset_name}_{args.prompt_type}.csv")
        df_cqs.to_csv(dst_csv_file_path,index=False)

        print(f"results saved as a csv file: {dst_csv_file_path}")