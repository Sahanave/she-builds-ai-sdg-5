import os
import google.generativeai as genai
import json
from google.protobuf import json_format
import protos 

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

MAX_ATTEMPTS = 3

def complete_game_scenario(background_story, work_distribution):
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
    prompt = f'''Generate a continuation of game that shows the benefits of sharing unpaid work. 
    Keep it short within 5 sentences 
    1.The division of chores: {work_distribution}
    2. The original background story: {background_story}
    3. Add new line character at end of set

    '''
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        try:
            response = model.generate_content(prompt)
            if response.text:  # Check if the response is valid
                return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}") 
        attempt += 1

def generate_game_scenario(chores=[]):
    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )
    prompt = f'''
            For a game, \n\n1. Name a couple (man and woman).
            2. Assuming they are partners, choose a task from to complete form list (task, energy_to_be spent) : {chores} 
            3. Generate a background stort  using LLMs . Keep it short within 10 sentences.
            4. Match a list of tasks of tasks to be completed by them as part of the story
            6. If not using the exact chore string, You are free to rename a chore string but match the close one in list and pass it as renamed. 
            7. generate another element to json . related Fact about how we can encourage equality  and create more opportunities for women 'equality_fact": "" 

    '''
    prompt += '''
            8. Return as json {couple_names, list_of_chores, renamed, background_story,equality_fact}
            9. Example : {
                            "couple_names": {
                                "man": {
                                "name": "Ethan",
                                },
                                "woman": {
                                "name": "Amelia",
                                }
                            },
                            "list_of_chores": [
                                {
                                "name": "Washdishes",
                                "energy_to_be_spent": 2,
                                },
                                {
                                "name": "Clean bathroom",
                                "energy_to_be_spent": 3,
                                },
                                {
                                "name": "Garden",
                                "energy_to_be_spent": 4,
                                },
                                {
                                "name": "GroceryShopping",
                                "energy_to_be_spent": 1,
                                },
                                {
                                "name": "Cook dinner",
                                "energy_to_be_spent": 2,
                                }
                            ],
                            "renamed" : {'Clean bathroom':'Cleaning','Cook dinner':'Cooking'},
                            "background_story": "Ethan and Amelia, a young couple living in a bustling city, were both ambitious professionals. Ethan, a software engineer, thrived on the challenge of his demanding job, while Amelia, a freelance writer, found inspiration in the rhythm of her creative pursuits. Their apartment, though cozy, was often neglected amidst the whirlwind of their busy lives. Dishes piled high in the sink, laundry overflowed from the hamper, and the once pristine bathroom was starting to show signs of neglect. They knew they needed to find a way to balance their careers with taking care of their home, but they felt overwhelmed by the sheer amount of chores.",
                            "equality_fact": "Studies have shown that providing affordable and accessible childcare reduces the burden of unpaid care work on women, allowing them to participate more equally in the workforce."
                            }
                ''' 
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        try:
            response = model.generate_content(prompt)
            if response.text:  # Check if the response is valid
                game_data = json.loads(response.text[7:-3]) # remove some unnecessary strings that breaks json.loads
                return game_data
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}") 
        attempt += 1
