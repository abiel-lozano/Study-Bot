# Test microphone selection and audio recording

import pyaudio
import wave
from pathlib import Path
from openai import AsyncOpenAI
import credentials
import asyncio
import time

startTime = None

# Initialize clients, set API keys
openAIClient = AsyncOpenAI(api_key = credentials.openAIKey)

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


def get_microphones():
	audio = pyaudio.PyAudio()
	mics = []
	for i in range(audio.get_device_count()):
		info = audio.get_device_info_by_index(i)
		if info.get('maxInputChannels') > 0:  # this is an input device
			name = info.get('name', '')
			# Ignore devices with these keywords in their names
			ignore_keywords = ['output', 'mapper', 'mix', 'speaker', 'stereo', 'front panel']
			if not any(keyword in name.lower() for keyword in ignore_keywords):
				mics.append(info)
	audio.terminate()
	return mics

def select_microphone(mics, index):
	return mics[index]

# Recorder configuration
CHUNK = 1024 # Chunk size
FORMAT = pyaudio.paInt16 # Audio codec format
CHANNELS = 1 # Number of channels
RATE = 44100 # Sample rate
OUTPUT_FILE = 'question.wav'

def recordQuestion(micIndex: int):
	global question
	global stop
	print('Setting up audio recording...')
	audio = pyaudio.PyAudio() # Initialize PyAudio
	mics = get_microphones()
	mic = select_microphone(mics, micIndex)
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

async def convertSTT() -> None:
	global response
	global question
	
	# Print all available microphones
	microphones = get_microphones()
	for i, mic in enumerate(microphones):
		print(f'{i}: {mic["name"]}')

	# Select microphone
	micIndex = int(input('Select microphone: '))

	recordQuestion(micIndex)
	
	with open(OUTPUT_FILE, 'rb') as audioFile:
		whisperResponse = await openAIClient.audio.transcriptions.create(model = 'whisper-1', file = audioFile)
	
	question = whisperResponse.text
	print(question)
	Path(OUTPUT_FILE).unlink()
	print('File deleted')

loop = asyncio.get_event_loop()
loop.run_until_complete(convertSTT())