# Prompt tester: Test if the model gives appropriate answers 
# given the source material, different custom instructions, 
# models, and temperature settings.

from openai import OpenAI
import credentials

print('\n', '|', '-'*50, '|', '\n', '|', ' Prompt Tester '.center(50, '-'), '|', '\n', '|', '-'*50, '|', '\n', sep = '', end = '\n\n')

GPT_MODEL = 'gpt-3.5-turbo'

# Initialize the OpenAI client
client = OpenAI(api_key = credentials.openAIKey)

# Source material, preferably from a realiable textbook
source = """

"""

question = input('Question: ')
objects = input('Objects: ')

# Build the prompt
query = f"""
Objects held by user: {objects}
Question: {question}
Information:
\"\"\"
{source}
\"\"\"
"""

# Send the prompt to the API
response = client.chat.completions.create(
	model = GPT_MODEL,
	temperature = 0.15,
	messages = [
		{
			'role': 'system', 
			'content': 
			"""
			Use the information below to help the user study by answering their 
			questions with thorough explanations. The user could be holding a 
			physical representation of what their question is about. Consider 
			the object list, which includes all the objects that the user is 
			holding, so that the answer can be refined to be more specific to 
			the user's question. Never mention 'the user' or 'the information' 
			in your answer, regardless of the circumstances, so that it sounds 
			natural, as if a teacher were answering a student's question. If 
			the question is unrelated to the information, try to answer the 
			question without mentioning the information or the objects to make 
			it sound more natural. If the user question is empty, or 
			unintelligible, give a summary of the topic. Refrain from adding 
			
			any additional prefixes or appendages such as 'Summary:' or 'Answer:'. 
			The response should consist solely of the content relevant to the 
			query without any additional formatting. You answer questions in the 
			same language as the question.
			"""
		}, {'role': 'user', 'content': query},
	]
)

print('\n\nChatGPT says:\n\n', response.choices[0].message.content, sep = '', end = '\n\n')