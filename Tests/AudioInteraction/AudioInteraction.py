# Test audio interaction in isolation without visual context or GUI
# Records a question, converts it to text, and uses it as a prompt to 
# generate an answer using GPT-3.5-turbo-16k
# The answer is then converted to audio and played back to the user
# Requires API keys in credentials.py

import pyaudio
import wave
from pathlib import Path
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from openai import OpenAI, AsyncOpenAI
import credentials
import asyncio
import time
from typing import Iterator

startTime = None

# Initialize clients, set API keys
# openAIClient = OpenAI(api_key = credentials.openAIKey)
openAIClient = AsyncOpenAI(api_key = credentials.openAIKey)
elevenLabsClient = ElevenLabs(api_key = credentials.elevenLabsKey)

GPT_MODEL = "gpt-3.5-turbo"

# Recorder configuration
CHUNK = 1024 # Chunk size
FORMAT = pyaudio.paInt16 # Audio codec format
CHANNELS = 2
RATE = 44100 # Sample rate
OUTPUT_FILE = 'question.wav'

question = ''

def recordQuestion():
	global question
	global stop
	print('Setting up audio recording...')
	audio = pyaudio.PyAudio() # Initialize PyAudio
	# Open audio stream for recording
	stream = audio.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
	frames = []
	
	print('Recording...')
	for i in range(0, int(RATE / CHUNK * 5)):
		data = stream.read(CHUNK)
		frames.append(data)

	# Stop and close audio stream
	stream.stop_stream()
	stream.close()
	audio.terminate()

	print('Recording stopped')

	# Save recording as WAV
	wf = wave.open(OUTPUT_FILE, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(audio.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	print('File saved as "question.wav"')

def streamAudio(audio_stream: Iterator[bytes]) -> bytes:
    audio = b""
    for chunk in audio_stream:
        if chunk is not None:
            audio += chunk

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format = pyaudio.paInt16,  # 16-bit PCM
                    channels = 1,  # mono
                    rate = 22050,  # sample rate
                    output = True)

    # Play stream
    for i in range(0, len(audio), 1024):
        stream.write(audio[i:i+1024])

    # Stop stream
    stream.stop_stream()
    stream.close()

    # Close PyAudio
    p.terminate()

    return audio

# Add infromation source
source = """
"""

# Build the prompt
query = f"""Try and use the information below to answer the question. If the 
question is unrelated to the information, ignore the information, and try to
answer the question without it.
Information:
\"\"\"
{source}
\"\"\"
Question: {question}"""

response = str()

async def sendMessage() -> None:
	global response
	global startTime

	startTime = time.time()
	recordQuestion()
	
	with open(OUTPUT_FILE, "rb") as audioFile:
		question = await openAIClient.audio.transcriptions.create(model = "whisper-1", file = audioFile)
	
	question = question.text

	print(question)
	# Delete audio file
	Path(OUTPUT_FILE).unlink()
	print('File deleted')
	
	stream = await openAIClient.chat.completions.create(
		model=GPT_MODEL,
		temperature=0.2,
		messages=[
			{'role': 'system', 'content': 'You answer questions in the same language as the question.'},
			{'role': 'user', 'content': query},
		],
		stream = True
	)
	async for chunk in stream:
		if chunk.choices[0].delta.content is not None:
			response += chunk.choices[0].delta.content or ''

loop = asyncio.get_event_loop()
loop.run_until_complete(sendMessage())


# New way to get the answer, response is now an object of the Response class
# answer = response.choices[0].message.content
# print('Answer: ', answer)
print(response)

print(f'\n Response time: {time.time() - startTime:.3f} seconds')

print('Audio playback disabled')
audioOutput = elevenLabsClient.generate(text = response, model = 'eleven_multilingual_v2', output_format = 'pcm_22050')
streamAudio(audioOutput)