import whisper
import pyaudio
import wave
import ffmpeg
import sys
import select
import openai
# import os
from gtts import gTTS
from pathlib import Path
import playsound
from recoder import recorder
from elevenlabs import generate, play, set_api_key
# from dotenv import load_dotenv
# import os

# from credentials import API_KEY

set_api_key('') # API KEY HERE

EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

def request_answer():

    recorder()
    model = whisper.load_model("base")
    result = model.transcribe("output.wav", fp16=False, language="English")
    print(result["text"])

    # Set up OpenAI API credentials
    # openai.api_key = os.getenv("API_KEY")
    openai.api_key = '' # API KEY HERE

    # Define the prompt. Change the source when needed.
    source = """
    
    """

    query = f"""Intenta usar el siguiente texto sobre la etapa de neurulación del embrión 
    para responder la pregunta. Si la respuesta no esta en el texto, usa tu conocimiento 
    general sobre el tema de la pregunta para responderla.
    Texto:
    \"\"\"
    {source}
    \"\"\"
    Pregunta: {result}"""

    response = openai.ChatCompletion.create(
        messages=[
            {'role': 'system', 'content': 'Answer any question about embryology. Make sure to answer in english.'},
            {'role': 'user', 'content': query},
        ],
        model=GPT_MODEL,
        temperature=0,
    )

    print('Answer: ', end='')
    answer = response['choices'][0]['message']['content']
    print(answer)
    # print(response)

    audio_output = generate(answer)

    play(audio_output)

# recording()
request_answer()

# If there is a file with the name "output.mp3" in the directory, delete it.
if Path("output.mp3").is_file():
    Path("output.mp3").unlink()

# If there is a file with the name "output.wav" in the directory, delete it.
if Path("output.wav").is_file():
    Path("output.wav").unlink()