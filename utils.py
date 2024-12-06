import re
from collections import Counter

def get_model_inputs(text, tokenizer):
    """
    transfer text 2 message
    :return: msg that can be fed into data
    """
    messages = [
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
        {"role": "user", "content": text}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt")
    return model_inputs

def extract_new_state(input_text):
    next_state_content = re.search(r"Next State:\s*\[(.*?)\]", input_text)
    if next_state_content:
        return next_state_content.group(1)
    else:
        print("未找到 Next State 内容")
        return 'None'


def extract_next_action(input_text):
    # Using regular expressions to capture the possible next steps
    # assuming next steps are separated by bullet points, numbers, or line breaks
    # Define regex pattern to find next steps after 'Output: Possible next steps:'
    steps = re.findall(r'\d+\)\s+(.*?)(?:\n|$)', input_text)
    return steps

def extract_eval(input_text):
    confidence_score = re.search(r"CONFIDENCE_SCORE:\s*([0-9.]+)", input_text)
    if confidence_score:
        try:
            return float(confidence_score.group(1))
        except (AttributeError, ValueError):
            return 0.0
    else:
        print('Can not extract confidence score!')
        return 0.0

def extract_result(input_text):
    result = re.search(r"Result:\s*([0-9.]+)", input_text)
    if result:
        result_str = result.group(1)
        try:
            # Attempt to convert to an integer
            return int(result_str)
        except ValueError:
            try:
                # If it fails, convert to a float
                return float(result_str)
            except ValueError:
                pass
    else:
        print('Cannot get the final result!')
        return 0

def majority_vote(result_list):
    # Count the occurrences of each result
    counts = Counter(result_list)
    # Find the result with the highest frequency
    majority_result = counts.most_common(1)[0][0]
    return majority_result

def convert_to_reasoning_list_string(state_list):
    reasoning_list = []
    for i, state in enumerate(state_list, 1):  # Start numbering from 1 for readability
        reasoning_list.append(f"{i}. {state}")
    # Join all items into a single string with line breaks
    return "\n".join(reasoning_list)


def eval_output(self, answer, output):
    if output is None:
        return False
    try:
        output = int(output)
        answer = int(answer)
        return output == answer
    except ValueError:
        pass
    try:
        output = float(output)
        answer = float(answer)
        return output == answer
    except ValueError:
        pass
    return output == answer


def extract_true_answer_from_test(input_text):
    final_answer = re.search(r"####\s*([0-9]+)", input_text)
    if final_answer:
        result_str = final_answer.group(1)
        try:
            # Attempt to convert to an integer
            final_result = int(result_str)
        except ValueError:
            # If it fails, convert to a float
            final_result = float(result_str)
    else:
        print('Can not get the true answer!')
        return None

    return final_result

