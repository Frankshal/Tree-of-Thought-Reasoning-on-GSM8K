prompt_head=\
    f"""
        Imagine you are trying to solve a math problem with a step-by-step approach. 
        
        The format of the problem is as below, follow this format only
        Question: XXXX
        Current_State: YYYY
        Possible next steps: ZZZZ
        Next State: ZZZZ

        """

question_prompt=    \
    f"""
        Question: [question]
        Current_State: [[state]]
        Possible next steps: [[action]]
        Next State: [Unknown]
        """

get_action_prompt=\
f"""

        Given the Current_State, you should propose a single next step to solve the problem involving a single arithmetic option. If there are multiple options for how to proceed, you should generate up to [breath] options.
        NOTE: You can only generate [breath] options, no more or no less. 
        NOTE: The next steps you generated should be actions.
        NOTE: The options should not be sequential or connected with each other, each option should be in a way that it can be evaluated independently. Dont jump to the result directly.
        IMPORTANT: MAKE SURE NOT TO HAVE THE DIRECT ANSWER IN YOUR POSSIBLE STEPS OUTPUT, JUST MAKE ONE STEP AT A TIME.
        Solved Example:

        Example 1
        
        Question: "Jasper will serve charcuterie at his dinner party. He buys 2 pounds of cheddar cheese for $10, a pound of cream cheese that cost half the price of the cheddar cheese, and a pack of cold cuts that cost twice the price of the cheddar cheese. How much does he spend on the ingredients?"
        Current_State: [Calculate the price of cheddar cheese which is $10 (given)]
        Possible next steps:
        1) Calculate the price of cold cuts which is 2*10 = $20.
        2) Calculate the price of cream cheese which is 10/2 = $5 per pound.
        Next State: [Unknown]

        Example 2
        
        Question: "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?"
        Current_State: [None]
        Possible next steps:
        1) Convert the minutes of babysitting to hours.
        2) Convert the wage per hour to wage per minute.
        Next State: [Unknown]

        Example 3
        
        Question: "James writes a 3-page letter to 2 different friends twice a week. How many pages does he write a year?"
        Current_State: [Number of letter written to 1 friend in a week = 2 as he writes twice a week]
        Possible next steps:
        1) Number of letter written to 2 friends in a week = 2*2 = 4 letters a week.
        2) Calculate the number of pages written to 1 friend in a week = 2*3 = 6 pages.
        Next State: [Unknown]

        """

predict_state_prompt=\
f"""

        Given the Current_State and Possible next steps, you should predict the Next State.

        NOTE:The next state should reflect a concise summary of what happens when we take the possible next step in the current state.
        NOTE: Your answer should follow this format only: Next State: [Your prediction]
        IMPORTANT: MAKE SURE NOT TO HAVE THE DIRECT ANSWER IN YOUR POSSIBLE NEXT STATE OUTPUT, JUST MAKE ONE STEP AT A TIME. 
        IMPORTANT: If Next State is your final answer please follow this formate: Next State: [Final Result:[Your prediction]]
        
        Solved Example:

        Example 1

        Question: "Jasper will serve charcuterie at his dinner party. He buys 2 pounds of cheddar cheese for $10, a pound of cream cheese that cost half the price of the cheddar cheese, and a pack of cold cuts that cost twice the price of the cheddar cheese. How much does he spend on the ingredients?"
        Current_State: [Calculate the price of cheddar cheese which is $10 (given)]
        Possible next steps: [Calculate the price of cold cuts which is 2*10 = $20]
        Next State: [The price of cheddar cheese is $10, and the price of cold cuts is $20.]

        Example 2

        Question: "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?"
        Current_State: [None]
        Possible next steps:[Convert the minutes of babysitting to hours.]
        Next State: [50 minutes of babysitting is converted to hours by dividing 50 by 60, resulting in 50/60 hours.]

        Example 3

        Question: "James writes a 3-page letter to 2 different friends twice a week. How many pages does he write a year?"
        Current_State: [Number of letter written to 1 friend in a week = 2 as he writes twice a week]
        Possible next steps:[Number of letter written to 2 friends in a week = 2*2 = 4 letters a week]
        Next State: [The number of letters written to 2 friends in a week is calculated as 2 * 2 = 4 letters per week.]

        """

final_answer_prompt = ('Now please calculate the final result based on the previous analysis. The format of the result is as below, follow this format only: The answer is n where n is a number')


# the question and the state should be specify for evalation.!!!!!!!!!!!!!
evaluate_prompt = ("Below is a question and an analysis from a student. "
                   "You are required to check the correctness of the reasoning "
                   "The criterions are as follows:\n\n**Accuracy in Mathematical Operations:** Ensure calculations are correct and follow logical mathematical principles."
                   "\n\n**Understanding the Problem Statement:** Comprehend the details and conditions of the question accurately."
                   "\n\n**Correct Application of Mathematical Concepts:** Apply the right mathematical formulas, operations, or concepts to solve the problem."
                   "\n\n**Unit Conversion and Appropriateness:** When required, correctly convert units and use appropriate units in the answer."
                   "\n\n**Final Answer Relevance:** Ensure this reasoning process is highly related to the true final answer."
                   "\n\nQuestion:\n[question]\n\nStudent Analysis:\nCurrent_State:[[state]]\nNext Step to solve the problem:[[action]]\nNext State:[[new_state]]"
                   "\n\nPlease check out the Analysis through each criterion"
                   "Finally, please provide the confidence score."
                   "The confidence score should be between 0.1 and 1.0. Use the following guidelines:"
                   "**0.1 to 0.3:** The thought is false, inaccurate."
                   "**0.3 to 0.8:** The thought is partially correct but may lack detail."
                   "**0.9 to 1.0:** The thought is accurate, complete, and well-reasoned."
                   "IMPORTANT:Please present the confidence score in a separate line at the end of your response, using the format CONFIDENCE_SCORE: <score>. Ensure that it appears consistently this way every time.")

result_prompt = ("Below is a question and an reasoning chain to solve the problem."
                 "\nQuestion:\n[question]\n"
                 "\nReasoning List:\n[reasoning_list]\n"
                 "Please carefully analyze the reasoning chain,check the correctness of the reasoning and generate a result for the problem."
                 "\nIMPORTANT:Please present the result in a separate line at the end of your response, using the format Result: <number>. **Do not include any units, currency symbols, or other characters.** Ensure that it appears consistently this way every time.")

