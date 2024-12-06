# Tree of Thought Reasoning on GSM8K

This repository provides instructions on how to set up and run the project. Follow the steps below to get started:

---

## How to Run

1. **Set up the Environment**  
   Create a virtual environment using the provided `vlm.yaml` file:
   ```bash
   conda env create -f vlm.yaml
   
2. **Activate the environment**
   ```bash
   conda activate vlm

3. **Modify the Cache Directory**

    Open the inference.py file and locate the CACHE_DIR variable. Update its value to point to your desired cache directory.
   ```python
   cache_dir = "/path/to/your/cache"

3. **Run the Script**
   ```bash
   python3 inference.py
   ```

## If you want to cite the paper

```
 @misc{yao2023treethoughtsdeliberateproblem,
      title={Tree of Thoughts: Deliberate Problem Solving with Large Language Models}, 
      author={Shunyu Yao and Dian Yu and Jeffrey Zhao and Izhak Shafran and Thomas L. Griffiths and Yuan Cao and Karthik Narasimhan},
      year={2023},
      eprint={2305.10601},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2305.10601}, 
}
```
For more details, you can access the paper on [arXiv](https://arxiv.org/abs/2305.10601).
