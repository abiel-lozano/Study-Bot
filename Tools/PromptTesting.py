# Prompt tester: Test if the model gives appropriate answers 
# given the source material, different custom instructions, 
# models, and temperature settings.

import openai
import credentials

print('Prompt Tester', end = '\n\n')
GPT_MODEL = 'gpt-3.5-turbo-16k'

openai.api_key = credentials.openAIKey

# Source material, preferably from a realiable textbook
source = """

"""

question = input('Question: ')

# Build the prompt
query = f"""
Try to use the following text to answer the user's question
If the question is not related to the text, ignore the previous
instruction and answer the question with your knowledge about
the topic of the question.
Text:
\"\"\"
{source}
\"\"\"
Question: {question}
Answer the question in the same language of the question.
"""

# Send the prompt to the API
response = openai.ChatCompletion.create(
    messages = [
        {'role': 'system', 'content': 'Answer questions in the language of the question.'},
		{'role': 'user', 'content': query},
	],
    model = GPT_MODEL,
    temperature = 0, # High temperature will make the AI more 'creative', low temperature will make the AI more 'factual' and reliant on the given source
)

print('Answer:', response['choices'][0]['message']['content'])