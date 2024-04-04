# Prompt tester: Test if the model gives appropriate answers 
# given the source material, different custom instructions, 
# models, and temperature settings.

from openai import OpenAI
import credentials

print('Prompt Tester', end = '\n\n')
GPT_MODEL = 'gpt-3.5-turbo-16k'

# Initialize the OpenAI client
client = OpenAI(api_key = credentials.openAIKey)

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
response = client.chat.completions.create(
    model = GPT_MODEL,
    temperature = 0.2,
    messages = [
        {'role': 'system', 'content': 'You answer questions in the same language as the question.'},
        {'role': 'user', 'content': query},
    ]
)

print('Answer:', response['choices'][0]['message']['content'])