# Study-Bot: Question Answering v0.2 (Text-Based Search With Topic Selector)
# Uses OpenAI's Cookbook guide code to answer questions from a text
# https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb

import openai

print('Study-Bot: Question Answering (Text-Based Search)', end='\n\n')

# OpenAI API Configuration
EMBEDDING_MODEL = 'text-embedding-ada-002'
GPT_MODEL = 'gpt-3.5-turbo'

# Set up OpenAI API credentials
openai.api_key = '' # API KEY HERE

# Topic selection
print('Select a topic from the list:')
print('[1] - Neurulation')
print('[2] - Pharyngeal Apparatus')
print('[3] - Spinal Cord')
print('[4] - Allantois and Endoderm')
topic = input('Topic: ')

source = ''

# Load the source material based on the selected topic
if topic == '1':
    print('Topic: Neurulation')
    source = """
    
    """
elif topic == '2':
    print('Topic: Pharyngeal Apparatus')
    source = """
    
    """
elif topic == '3':
    print('Topic: Spinal Cord.')
    print('There is no source for this topic.')
    exit()
elif topic == '4':
    print('Topic: Allantois and Endoderm')
    print('There is no source for this topic.')
    exit()
else:
    print('This topic does not exist.')
    exit()

question = input('Question: ')

query = f"""
Try to use the following text about the development of the embryo to answer
the question. If the question is not related to the text,
ignore the previous instruction and answer the question with your knowledge
about the topic of the question.

Text:
\"\"\"
{source}
\"\"\"
Question: {question}
If the question is in English, your answer must be in English.
If the question is in Spanish, your answer must be in Spanish.
"""

response = openai.ChatCompletion.create(
    messages=[
        {'role': 'system', 'content': 'Answer questions in the language of the question.'},
		{'role': 'user', 'content': query},
	],
    model=GPT_MODEL,
    temperature=0,
)

print('Answer: ')
print(response['choices'][0]['message']['content'])