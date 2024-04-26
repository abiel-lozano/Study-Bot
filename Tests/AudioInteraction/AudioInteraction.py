# Test audio interaction in isolation without visual context or GUI
# Records a question, converts it to text, and uses it as a prompt to 
# generate an answer using GPT-3.5-turbo

# The answer is then converted to audio and played back to the user
# Requires API keys in credentials.py

# Based on the ElevenLabs example code provided in the ElevenLabs API documentation
# for voice streaming using ElevenLabs and OpenAI APIs:
# https://elevenlabs.io/docs/api-reference/websockets#example-voice-streaming-using-elevenlabs-and-openai

import pyaudio
import wave
from pathlib import Path
from elevenlabs.client import ElevenLabs, AsyncElevenLabs
from elevenlabs import play
from openai import OpenAI, AsyncOpenAI
import credentials
import asyncio
import time
from typing import Iterator, AsyncGenerator

import websockets
import json
import base64

startTime = None

# Initialize clients, set API keys
# openAIClient = OpenAI(api_key = credentials.openAIKey)
openAIClient = AsyncOpenAI(api_key = credentials.openAIKey)
# elevenLabsClient = ElevenLabs(api_key = credentials.elevenLabsKey)
elevenLabsClient = AsyncElevenLabs(api_key = credentials.elevenLabsKey)

GPT_MODEL = "gpt-3.5-turbo"


question = ''

# Add infromation source
source = """
"""

# Build the prompt
query = f"""
Answer the following question in the same language as the question:
Question: {question}"""

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

	print('Recording stopped')

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

async def text_chunker(chunks):
	"""Split text into chunks, ensuring to not break sentences."""
	splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]", "}", " ")
	buffer = ""

	async for text in chunks:
		if text is None:
			continue
		if buffer.endswith(splitters):
			yield buffer + " "
			buffer = text
		elif text.startswith(splitters):
			yield buffer + text[0] + " "
			buffer = text[1:]
		else:
			buffer += text

	if buffer:
		yield buffer + " "


async def streamAudio(audio_stream: Iterator[bytes]) -> bytes:
	global startTime

	audio = b""
	async for chunk in audio_stream:
		if chunk is not None:
			audio += chunk

	# Create a PyAudio object
	p = pyaudio.PyAudio()

	# Open stream
	stream = p.open(format = pyaudio.paInt16,  # 16-bit PCM
					channels = 1,  # mono
					rate = 22050,  # sample rate
					output = True)
	
	print(f'\n Response time: {time.time() - startTime:.3f} seconds')

	# Play stream
	for i in range(0, len(audio), 1024):
		stream.write(audio[i:i+1024])

	# Stop stream
	stream.stop_stream()
	stream.close()

	# Close PyAudio
	p.terminate()

	return audio

async def text_to_speech_input_streaming(voice_id, text_iterator):
	"""Send text to ElevenLabs API and stream the returned audio."""
	uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id=eleven_multilingual_v2"

	async with websockets.connect(uri) as websocket:
		await websocket.send(json.dumps({
			"text": " ",
			"voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
			"xi_api_key": credentials.elevenLabsKey,
			"output_format": "pcm_22050"
		}))

		async def listen():
			"""Listen to the websocket for audio data and stream it."""
			while True:
				try:
					print('Listening...')
					message = await websocket.recv()
					if message is not None:
						print('Message received')
					data = json.loads(message)
					if data.get("audio"):
						print('Audio received')
						yield base64.b64decode(data["audio"])
					elif data.get('isFinal'):
						print('Final audio received')
						break
				except websockets.exceptions.ConnectionClosed:
					print("Connection closed")
					break

		listen_task = asyncio.create_task(streamAudio(listen()))

		async for text in text_chunker(text_iterator):
			await websocket.send(json.dumps({"text": text, "try_trigger_generation": True}))

		await websocket.send(json.dumps({"text": ""}))

		await listen_task


async def sendMessage() -> AsyncGenerator[str, None]:
	global response
	textStream = await openAIClient.chat.completions.create(
		model=GPT_MODEL,
		temperature=0.2,
		messages=[
			{'role': 'system', 'content': 'You answer questions in the same language as the question.'},
			{'role': 'user', 'content': query},
		],
		stream = True
	)
	async def textIterator():
		completeResponse = ''
		async for chunk in textStream:
			if chunk.choices[0].delta is not None:
				delta = chunk.choices[0].delta
				if delta.content is not None:
					completeResponse += delta.content
				yield delta.content
		print('Text stream ended')
		print(completeResponse)

	await text_to_speech_input_streaming("EXAVITQu4vr4xnSDxMaL", textIterator())
			

async def convertTTS() -> None:
	global response
	global question
	
	recordQuestion()
	
	with open(OUTPUT_FILE, "rb") as audioFile:
		whisperResponse = await openAIClient.audio.transcriptions.create(model = "whisper-1", file = audioFile)
	
	question = whisperResponse.text

	print(question)
	# Delete audio file
	Path(OUTPUT_FILE).unlink()
	print('File deleted')
	# print('Audio playback disabled')
 
	# audioOutput = await elevenLabsClient.generate(text = sendMessage(), model = 'eleven_multilingual_v2', output_format = 'pcm_22050', stream = True)
	# print(response)
	# await streamAudio(audioOutput)
 
	await sendMessage()

loop = asyncio.get_event_loop()
loop.run_until_complete(convertTTS())