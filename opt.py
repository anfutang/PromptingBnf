from argparse import ArgumentParser

def get_args():
     parser = ArgumentParser(description="prompting with ambiguity type definitions.")
	
     parser.add_argument("--data_dir",type=str,default="./data/")
     parser.add_argument("--output_dir",type=str,default="./output/")
     parser.add_argument("--dataset_name",type=str)
     parser.add_argument("--model_name",type=str,default="meta-llama/Llama-2-13b-chat-hf")
     parser.add_argument("--prompt_type",type=str)
     parser.add_argument("--batch_size",type=int,default=2,help="batch size used for inference")
     parser.add_argument("--save_as_csv",action="store_true")
     parser.add_argument("--dry_run",action="store_true")
     args = parser.parse_args()
     return args