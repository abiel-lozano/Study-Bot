# Test audio interaction in isolation without visual context or GUI
# Records a question, converts it to text, and uses it as a prompt to 
# generate an answer using GPT-3.5-turbo-16k
# The answer is then converted to audio and played back to the user
# Requires API keys in credentials.py

import pyaudio
import wave
import credentials
from openai import OpenAI
from pathlib import Path
from elevenlabs import generate, play, set_api_key

client = OpenAI(api_key = credentials.openAIKey)

# set_api_key('') # Elevenlabs API key
GPT_MODEL = "gpt-3.5-turbo-16k"

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

	# STT Conversion
	# 'with open() as' automatically closes the file after the block is executed
	# allows immediate deletion
	with open(OUTPUT_FILE, "rb") as audioFile:
		question = client.audio.transcriptions.create(model="whisper-1", file=audioFile).text

	print(question)
	# Delete audio file
	Path(OUTPUT_FILE).unlink()
	print('File deleted')

recordQuestion()

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

response = client.chat.completions.create(
	model = GPT_MODEL,
	temperature = 0.2,
	messages = [
		{'role': 'system', 'content': 'You answer questions in the same language as the question.'},
		{'role': 'user', 'content': query},
	]
)
# This does not work anymore, response is no longer a dictionary
# answer = response['choices'][0]['message']['content']

# New way to get the answer, response is now an object of the Response class
answer = response.choices[0].message.content
print('Answer: ', answer)

audioOutput = generate(answer)
play(audioOutput)