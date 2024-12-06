# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
from worldmodel import gsm8k_tot_solver
from datasets import load_dataset
from tqdm import tqdm
import utils


tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct"
                                          ,torch_dtype="auto"
                                          ,device_map="auto"
                                          ,trust_remote_code=True
                                          ,cache_dir="/data/shaoy/task2/tmp")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct"
                                          ,torch_dtype="auto"
                                          ,device_map="auto"
                                          ,trust_remote_code=True
                                          ,cache_dir="/data/shaoy/task2/tmp")


ds = load_dataset("openai/gsm8k", "main",cache_dir='/data/shaoy/task2/tmp')
dataset = ds['test']
question=dataset['question']
answer=dataset['answer']
tot=gsm8k_tot_solver(base_model=model,tokenizer=tokenizer,question='data',breath=5,depth=4)

results = []
for i in tqdm(range(100)):
    q=question[i]
    a=answer[i]
    true_label=utils.extract_true_answer_from_test(a)
    print(f"\n***Question***:\n{q}\n")
    tot.update_question(question=q)
    final_result = tot.solve()
    results.append({
        "question": q,
        "final_result": final_result,
        "true_label": true_label
    })

df = pd.DataFrame(results)

df.to_csv('5_4_result.csv', index=False)

print("Data saved to model_results.csv")

