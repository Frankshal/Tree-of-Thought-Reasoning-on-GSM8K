from instruction import *
import re
import utils

class Prompt:
    # This class is to manage the prompt
    def __init__(self, breadth, question):
        """

        :param breadth: define how many steps to be generated
        :param question:
        :param init_state:
        """
        self.breadth = breadth
        self.question = question
        self.prompt_head = prompt_head
        self.question_prompt = question_prompt.replace('[question]',self.question)
        self.get_action_prompt = get_action_prompt
        self.predict_state_prompt = predict_state_prompt
        self.evaluate_prompt = evaluate_prompt.replace('[question]',self.question)
        self.result_prompt = result_prompt.replace('[question]',self.question)

    def get_next_action_prompt(self,breath,state):
        # create a prompt to instruct lm to get next actions
        q = self.question_prompt.replace('[state]',state).replace('[action]','Unknown')
        print('\n***get_next_action:***\n',q)
        s = f"\nPlease follow the instruction above and generate {breath} possible next steps for this question\n"
        prompt = self.prompt_head + self.get_action_prompt.replace('[breath]',str(breath)) + s + q
        return prompt.lstrip()

    def predict_next_state_prompt(self,state,action):
        # create a prompt to instruct lm to predict next state
        q = self.question_prompt.replace('[state]',state).replace('[action]',action)
        print('\n***predict_next_state:***\n',q)
        s = "\nPlease follow the instruction above and predict the next state for this question\n"
        prompt = self.prompt_head + self.predict_state_prompt + s + q
        return prompt.lstrip()

    def get_result_prompt(self,state_list:list[str]):
        reasoning_list = utils.convert_to_reasoning_list_string(state_list)
        prompt = result_prompt.replace('[reasoning_list]',reasoning_list)
        return prompt.lstrip()

    def evalutate_prompt(self,state,action,new_state):
        prompt = self.evaluate_prompt.replace('[state]',state).replace('[action]',action).replace('[new_state]',new_state)
        return prompt.lstrip()

    def update_question(self,question):
        self.question = question
        self.evaluate_prompt = evaluate_prompt.replace('[question]',question)
        self.result_prompt = result_prompt.replace('[question]',question)
        self.question_prompt = question_prompt.replace('[question]',question)

