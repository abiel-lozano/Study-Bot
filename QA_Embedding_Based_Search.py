# Study-Bot: Question Answering (Embedding-based Search) v0.2
# Uses OpenAI's Cookbook guide code to use embedding-based search
# https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb

# import ast
import tiktoken
# from scipy import spatial
import openai
from dotenv import load_dotenv
import os
from itertools import islice
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine

# OpenAI API Configuration
EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'
GPT_MODEL = 'gpt-3.5-turbo' # Max tokens: 4096
load_dotenv()
openai.api_key = os.getenv("API_KEY")

# Count number of tokens in a string
def numTokens(text: str, model: str = GPT_MODEL) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Breaks up a sequence into chunks of size n, last chunk may be shorter
def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least 1')
    it = iter(iterable)
    # While there are elements to iterate over in the iterable object (it), take the next n elements and return them as a tuple
    while (batch := tuple(islice(it, n))):
        yield batch

# Encode a string into tokens and break into chunks
def chunkedTokens(text, encoding_name, chunk_length):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    chunks_iterator = batched(tokens, chunk_length)
    yield from chunks_iterator

# Handle embedding requests larger than 4096 tokens, chunk the input tokens and embed each chunk individually.
def getEmbedding(text, model = EMBEDDING_MODEL, maxTokens = EMBEDDING_CTX_LENGTH, encodingName = EMBEDDING_ENCODING, average = True):
    chunkEmbeddings = []
    chunkLens = []

    for chunk in chunkedTokens(text, encodingName = encodingName, chunkLength = maxTokens):
        chunkEmbeddings.append(getEmbedding(chunk, model = model))
        chunkLens.append(len(chunk))

    if average:
        chunkEmbeddings = np.average(chunkEmbeddings, axis = 0, weights = chunkLens)
        chunkEmbeddings = chunkEmbeddings / np.linalg.norm(chunkEmbeddings) # Normalize the length to 1
        chunkEmbeddings = chunkEmbeddings.tolist()
    return chunkEmbeddings

# Load the source material
sourceNeurulation = """
"""
sourcePharyngealApparatus = """

"""

# question = input("Question: ")
question = "¿Qué es la neurulación?"

query = f"""
Intenta usar alguna de las etapas de desarrollo del embrión o de alguno 
de sus sistemas para responder la pregunta. Si la respuesta no esta en el texto, ignora 
la instrucción anterior, no menciones el texto, e intenta responder la pregunta.
Texto:
\"\"\"
{sourcePharyngealApparatus}
\"\"\"
Pregunta: {question}"""

# response = openai.ChatCompletion.create(
#     messages = [
#         {'role': 'system', 'content': 'Contesta las preguntas sobre la neurulación del embrión.'},
# 		{'role': 'user', 'content': query},
# 	],
#     model = GPT_MODEL,
#     temperature = 0,
# )


# print('Answer: ', response['choices'][0]['message']['content'], end='\n\n')
queryTokens = numTokens(query)
# answerTokens = numTokens(response['choices'][0]['message']['content'])
print('Query Token Count: ', queryTokens)
# print('Answer Token Count: ', answerTokens)
# print('Total Token Count: ', end='')
# print(queryTokens + answerTokens)
print('Source Token Count: ', numTokens(sourcePharyngealApparatus), end='\n\n')
sourceMaterial = 'Very long text will be here soon.'

avgEmbeddingVector = getEmbedding(sourceMaterial, average = True)
chunksEmbeddingVectors = getEmbedding(sourceMaterial, average = False)

print(f'Setting average = True gives us a single {len(avgEmbeddingVector)}-dimensional embedding vector for our long text.')
print(f'Setting average=False gives us {len(chunksEmbeddingVectors)} embedding vectors, one for each of the chunks.')

# Save the embedding vectors to a file
np.save('avgEmbedding.npy', avgEmbeddingVector)

# Save the chunked embedding vectors
np.save('chunksEmbedding.npy', chunksEmbeddingVectors)

# ---------------------------------------------------------------

# Load the average embedding vector
avgEmbedding = np.load('avg_embedding.npy')

# Load the chunked embedding vectors
chunksEmbedding = np.load('chunks_embedding.npy', allow_pickle=True)

def calcSimilarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

def findMostSimilarChunk(query):
    maxSimilarity = -1
    mostSimilarChunk = None

    for chunk in chunksEmbedding:
        similarity = calcSimilarity(query, chunk)
        if similarity > maxSimilarity:
            maxSimilarity = similarity
            mostSimilarChunk = chunk

        return mostSimilarChunk
    
question = "¿Qué es la neurulación?"

# Calculate similarity between the question and the average embedding
similarityScores = np.array([calcSimilarity(avgEmbedding, chunksEmbedding) for chunkEmbedding in chunksEmbedding])

# Find the chunk with the highest similarity to the question
mostSimilarChunk = findMostSimilarChunk(question)

# Retrieve the original text of the most similar chunk
chunkText = tiktoken.get_encoding('cl100k_base').decode(mostSimilarChunk)

# Print the answer
print('Question', question)
print('Answer:', chunkText)