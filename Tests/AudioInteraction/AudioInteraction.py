# Test audio interaction in isolation without visual context or GUI
# Records a question, converts it to text. Sends question to ChatGPT
# and converts the response to audio and plays it back to the user 
# in real-time while GPT is generating the answer.

# The answer is then converted to audio and played back to the user
# Requires API keys in credentials.py

# Input streaming based on the ElevenLabs example code provided in the 
# ElevenLabs API documentation for voice streaming using ElevenLabs 
# and OpenAI APIs, available at:
# https://elevenlabs.io/docs/api-reference/websockets#example-voice-streaming-using-elevenlabs-and-openai

# Works without depending on mpv or ffmpeg

import pyaudio
import wave
from pathlib import Path
from elevenlabs.client import AsyncElevenLabs
from openai import AsyncOpenAI
import credentials
import asyncio
import time
from typing import AsyncGenerator
import websockets
import json
import base64
import threading
import queue

startTime = None

audioQueue = queue.Queue()

# Initialize clients, set API keys
openAIClient = AsyncOpenAI(api_key = credentials.openAIKey)
elevenLabsClient = AsyncElevenLabs(api_key = credentials.elevenLabsKey)

GPT_MODEL = "gpt-3.5-turbo"

global question
question = ''

# Add infromation source
source = """
"""

# Build the prompt
query = f"""
Why are silicon wafers round if chips are square? Describe the process of making silicon wafers and the process of making chips.
"""

response = str()

# Recorder configuration
CHUNK = 1024 # Chunk size
FORMAT = pyaudio.paInt16 # Audio codec format
CHANNELS = 1 # Number of channels
RATE = 44100 # Sample rate
OUTPUT_FILE = 'question.wav'

def recordQuestion():
	global question
	global stop
	print('Setting up audio recording...')
	audio = pyaudio.PyAudio() # Initialize PyAudio
	# Open audio stream for recording
	stream = audio.open(
		format = FORMAT, 
		channels = CHANNELS, 
		rate = RATE, 
		input = True, 
		frames_per_buffer = CHUNK
	)
	frames = []
	
	print('Recording...')
	for i in range(0, int(RATE / CHUNK * 5)):
		data = stream.read(CHUNK)
		frames.append(data)

	# Stop and close audio stream
	stream.stop_stream()
	stream.close()
	audio.terminate()

	print('Recording stopped, start time set')

	global startTime
	startTime = time.time()

	# Save recording as WAV
	wf = wave.open(OUTPUT_FILE, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(audio.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	print('File saved as "question.wav"')

async def textChunker(chunks):
	# Split text into chunks, ensuring to not break sentences.
	splitters = ('.', ',', '?', '!', ';', ':', '—', '-', '(', ')', '[', ']', '}', ' ')
	buffer = ''

	async for text in chunks:
		if buffer.endswith(splitters):
			yield buffer + ' '
			buffer = text
		elif text.startswith(splitters):
			yield buffer + text[0] + ' '
			buffer = text[1:]
		else:
			buffer += text

	if buffer:
		yield buffer + ' '

def playAudioFromQueue():
	p = pyaudio.PyAudio()
	stream = p.open(format = pyaudio.paInt16, channels = 1, rate = 24000, output = True, frames_per_buffer = 32768)
	
	while True:
		audioData = audioQueue.get()
		if audioData is None:
			break
		stream.write(audioData)
	
	stream.stop_stream()
	stream.close()
	p.terminate()

async def playAudio(audioData: bytes):
	global startTime
	
	if startTime is not None:
		print('Response Time: ', time.time() - startTime)
		startTime = None

	audioQueue.put(audioData)

async def stream(audioStream):
	# Stream audio data and play it.
	async for chunk in audioStream:
		if chunk:
			await playAudio(chunk)

async def ttsInputStreaming(textIterator):
	# Send text to ElevenLabs API and stream the returned audio.
	# URI: Convert TTS, use voice 'Sarah', with model 'eleven_multilingual_v1', and output in 'pcm_24000' format.
	uri = f'wss://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream-input?model_id=eleven_multilingual_v1&output_format=pcm_24000'

	async with websockets.connect(uri) as websocket:
		await websocket.send(json.dumps({
			'text': ' ',
			'xi_api_key': credentials.elevenLabsKey,
			'voice_settings': {'stability': 0.5, 'similarity_boost': 0}
		}))

		async def listen():
			# Listen to the websocket for audio data and stream it.
			while True:
				try:
					message = await websocket.recv()
					data = json.loads(message)
					# Check if the message contains audio data or is the final message.
					if data.get('audio'):	
						yield base64.b64decode(data['audio'])
					elif data.get('isFinal'):
						break
				except websockets.exceptions.ConnectionClosed:
					print('Connection closed')
					break
		
		listen_task = asyncio.create_task(stream(listen()))

		async for text in textChunker(textIterator):
			await websocket.send(json.dumps({'text': text, 'try_trigger_generation': True}))

		await websocket.send(json.dumps({'text': ''}))
		await listen_task


async def sendMessage() -> AsyncGenerator[str, None]:
	global response
	global question

	textStream = await openAIClient.chat.completions.create(
		model = GPT_MODEL,
		temperature = 0.2,
		messages = [
			{'role': 'system', 'content': 'You answer in English or Spanish depending on the language of the question.'},
			{'role': 'user', 'content': query},
		],
		stream = True
	)
	
	async def textIterator():
		global response
		async for chunk in textStream:
			delta = chunk.choices[0].delta
			if delta.content is not None:
				response += delta.content
				print(delta.content)
				yield delta.content

	await ttsInputStreaming(textIterator())
	
	# Add sentinel value to queue to stop audio playback
	audioQueue.put(None)

async def convertTTS() -> None:
	global response
	global question
	
	recordQuestion()
	
	with open(OUTPUT_FILE, 'rb') as audioFile:
		whisperResponse = await openAIClient.audio.transcriptions.create(model = 'whisper-1', file = audioFile)
	
	question = whisperResponse.text
	print(question)
	Path(OUTPUT_FILE).unlink()
	print('File deleted')

	threading.Thread(target = playAudioFromQueue).start()
	
	await sendMessage()

loop = asyncio.get_event_loop()
loop.run_until_complete(convertTTS())