# Study-Bot: Question Answering v0.2 (Text-Based Search With Topic Selector)
# Uses OpenAI's Cookbook guide code to answer questions from a text
# https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb

import openai

print('Study-Bot: Question Answering (Text-Based Search)', end='\n\n')

# OpenAI API Configuration
EMBEDDING_MODEL = 'text-embedding-ada-002'
GPT_MODEL = 'gpt-3.5-turbo-16k'

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
    Neurulation is a critical process during embryonic development that leads to the formation of the neural tube, which eventually gives rise to the central nervous system (CNS). Here is a 5-stage summary of the neurulation process:

Initiation: Neurulation begins during the third week of embryonic development. It is initiated when the notochord, a rod-like structure that runs along the embryonic midline, induces the overlying ectoderm to differentiate into neuroectoderm. This neuroectoderm is the precursor tissue for the nervous system.

Formation of the Neural Plate: The induced neuroectoderm thickens and forms a flat, plate-like structure called the neural plate. This plate is located along the dorsal (back) surface of the embryo and extends from the cranial (head) end to the caudal (tail) end.

Folding of the Neural Plate: As development progresses, the neural plate undergoes a complex series of folding events. The edges of the plate elevate and move towards each other, forming two parallel ridges called the neural folds. This folding process begins in the cranial region and proceeds towards the caudal region.

Formation of the Neural Tube: The neural folds continue to elevate and eventually fuse together along the midline of the embryo. This fusion begins in the cervical (neck) region and proceeds both cranially and caudally. Once the neural folds have completely fused, they form a hollow, tube-like structure called the neural tube. This tube will give rise to the brain and spinal cord.

Differentiation of Neural Crest Cells: During the process of neurulation, some cells at the neural crest are not incorporated into the neural tube but instead migrate to other areas of the embryo. These neural crest cells will differentiate into various cell types, including peripheral neurons, glial cells, and cells of the peripheral nervous system, as well as other non-neural cell types like cartilage, bone, and pigment cells.

The completion of neurulation is a crucial milestone in embryonic development, as it sets the stage for the formation of the entire central nervous system and other related structures. Any disruptions or abnormalities in this process can lead to serious congenital defects, such as neural tube defects like spina bifida and anencephaly.
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