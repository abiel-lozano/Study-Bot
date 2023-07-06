# Study-Bot: Source Embedding (Text to Embedding) v0.1
# Uses OpenAI's Cookbook guide code to process long text inputs into embeddings
# https://github.com/openai/openai-cookbook/blob/main/examples/Embedding_long_inputs.ipynb

import tiktoken
import openai
from dotenv import load_dotenv
import os
from itertools import islice
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine

# Source material
sourceNeurulation = """

"""
sourcePharyngealApparatus = """

"""
compiledSource = sourceNeurulation + sourcePharyngealApparatus

# OpenAI API Configuration
EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'
GPT_MODEL = 'gpt-3.5-turbo'

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

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

    for chunk in chunkedTokens(text, encodingName, maxTokens):
        chunkEmbeddings.append(getEmbedding(chunk, model = model))
        chunkLens.append(len(chunk))

    if average:
        chunkEmbeddings = np.average(chunkEmbeddings, axis = 0, weights = chunkLens)
        chunkEmbeddings = chunkEmbeddings / np.linalg.norm(chunkEmbeddings) # Normalize the length to 1
        chunkEmbeddings = chunkEmbeddings.tolist()
    return chunkEmbeddings

avgEmbeddingVector = getEmbedding(compiledSource, average = True)
chunksEmbeddingVectors = getEmbedding(compiledSource, average = False)

print(f'Setting average = True gives us a single {len(avgEmbeddingVector)}-dimensional embedding vector for our long text.')
print(f'Setting average=False gives us {len(chunksEmbeddingVectors)} embedding vectors, one for each of the chunks.')

# Save the embedding vectors to a file
np.save('avgEmbedding.npy', avgEmbeddingVector)

# Save the chunked embedding vectors
np.save('chunksEmbedding.npy', chunksEmbeddingVectors)

print('Embedding vectors saved to avgEmbedding.npy and chunksEmbedding.npy')