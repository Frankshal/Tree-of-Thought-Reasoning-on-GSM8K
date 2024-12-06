import utils
from prompt import Prompt
import copy

BWState = str
BWAction = str

class gsm8k_tot_solver():
    def __init__(self,base_model,tokenizer,question,breath,depth):
        super().__init__()
        self.base_model = base_model
        self.tokenizer = tokenizer
        self.question = question
        self.breath = breath
        self.depth = depth
        self.prompt = Prompt(breath,question)

    def update_question(self,question):
        self.question = question
        self.prompt.update_question(question)

    def init_state(self) :
        # extract the statement from a given problem
        # e.g., "the red block is clear, the blue block is clear..."
        return self.question

    def predict_new_state(self, state, action) :
        # call the LLM to predict the state transition
        state = copy.deepcopy(state)
        # load the prompt for the LLM to predict the next state
        # e.g. "... I have that <state>, if I <action>, then ..."
        world_update_prompt = self.prompt.predict_next_state_prompt(state,action)
        model_inputs = utils.get_model_inputs(world_update_prompt,self.tokenizer).to('cuda')
        generated_ids = self.base_model.generate(**model_inputs,max_new_tokens=512)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print('\n***response***:\n',response)
        new_state = utils.extract_new_state(response)
        # till now, we have the new state after the action
        # the following part is to speed up the reward calculation
        return new_state

    def get_new_action(self,state)->list:
        state = copy.deepcopy(state)
        action_update_prompt = self.prompt.get_next_action_prompt(self.breath,state)
        model_inputs = utils.get_model_inputs(action_update_prompt,self.tokenizer).to('cuda')
        generated_ids = self.base_model.generate(**model_inputs,max_new_tokens=512)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print('\n***response***:\n',response)
        actions = utils.extract_next_action(response)
        return actions

    def evaluate_state(self,state,action,new_state):
        state,action,new_state = copy.deepcopy(state),copy.deepcopy(action),copy.deepcopy(new_state)
        eval_prompt = self.prompt.evalutate_prompt(state,action,new_state)
        model_inputs = utils.get_model_inputs(eval_prompt, self.tokenizer).to('cuda')
        generated_ids = self.base_model.generate(**model_inputs,max_new_tokens=512)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        confidence = utils.extract_eval(response)
        return confidence

    def get_final_result(self,state_list):
        #given the former state list, then generate the final result!
        result_list=[]
        the_result_prompt = self.prompt.get_result_prompt(state_list)
        model_inputs = utils.get_model_inputs(the_result_prompt, self.tokenizer).to('cuda')
        for i in range(self.breath):
            generated_ids = self.base_model.generate(**model_inputs, max_new_tokens=512,temperature=0.3)
            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            result = utils.extract_result(response)
            result_list.append(result)
        final_result = utils.majority_vote(result_list)
        print('\n***final_result***:\n',final_result)
        return final_result

    def solve(self):
        #init_state
        state_list=[]
        state_list.append(self.init_state())
        #state='None'
        state="Total number of eggs laid by Janet's ducks per day is 16."
        for i in range(1,self.depth):
            action_list = self.get_new_action(state)
            best_state = None
            best_confidence = float('-inf')
            for action in action_list:
                new_state = self.predict_new_state(state,action)
                confidence = self.evaluate_state(state,action,new_state)
                #print(f'\n\n****confidence score****\n\n={confidence}')
                if confidence > best_confidence:
                    best_state = new_state
                    best_confidence = confidence
            state_list.append(best_state)
            state = best_state
        # get final answer
        final_result = self.get_final_result(state_list)
        return final_result







