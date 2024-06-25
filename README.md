### Prompting on BnF user queries 

Install necessary packages:
```
pip install requirements.txt
```

Run a quick test on several examples:
```
sbatch exp-zs.sh bnf_demo
```

Run all prompts on the first subset of queries (1000):
```
sh exp-run-all.sh bnf_p1
```

Parse CQs from generated texts and generate a processing log file:
```
python3 parse.py --dataset_name bnf_test --prompt_type few-shot --save_as_csv > logs/parse_bnf_test_fs.log
```
