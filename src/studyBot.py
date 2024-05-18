# Study-Bot: Question answering using audio interaction and object detection, 
# CLI version for testing, and functions for GUI version

import pyaudio
import wave
import time
from pathlib import Path
from openai import OpenAI
import cv2
import numpy as np
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import threading
import keyboard
import credentials # Contains API keys, create your own credentials.py file
import sourceMaterial

objects = str()
question = str()
answer = str()
stop = bool()
startTime = 0.0

# Credentials
openAIClient = OpenAI(api_key = credentials.openAIKey)
elevenLabsClient = ElevenLabs(api_key = credentials.elevenLabsKey)

# TODO: Fix custom instructions, these don't work anymore, again

# Behavioral guidelines for conversation
customInstructions = """
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

# Recorder configuration
CHUNK = 1024 # Chunk size
FORMAT = pyaudio.paInt16 # Audio codec format
CHANNELS = 2
RATE = 44100 # Sample rate
OUTPUT_FILE = 'question.wav'

def recordQuestion():
	global question
	global stop
	global startTime

	startTime = time.time()
	stop = False

	audio = pyaudio.PyAudio()
	stream = audio.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
	frames = []

	# Record audio stream in chunks
	while not stop:
		data = stream.read(CHUNK)
		frames.append(data)

	# Stop and close audio stream
	stream.stop_stream()
	stream.close()
	audio.terminate()

	# Save recording as WAV
	wf = wave.open(OUTPUT_FILE, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(audio.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	# STT Conversion
	with open(OUTPUT_FILE, 'rb') as audioFile:
		question = openAIClient.audio.transcriptions.create(model = 'whisper-1', file = audioFile).text
	Path(OUTPUT_FILE).unlink()

def colorID(camera: int = 0):
	global objects
	objects = 'User is not holding any objects'

	# Capture video
	cam = cv2.VideoCapture(camera, cv2.CAP_DSHOW) # Use 0 for default camera

	# Start timer
	startTime = time.time()
	elapsedTime = 0

	# Color ranges
	stomachLower = np.array([90, 	80, 		100			], np.uint8)
	stomachUpper = np.array([120, 	255, 		255			], np.uint8)
	colonLower = np.array(	[10, 	255 * 0.55, 255 * 0.35	], np.uint8)
	colonUpper = np.array(	[19.5, 	255, 		255			], np.uint8)
	liverLower = np.array(	[38, 	225 * 0.22, 255 * 0.38	], np.uint8)
	liverUpper = np.array(	[41, 	255, 		255			], np.uint8)
	brainLower = np.array(	[161, 	255 * 0.50, 255 * 0.40	], np.uint8)
	brainUpper = np.array(	[161, 	255, 		255			], np.uint8)
	kidneyLower = np.array(	[26, 	255 * 0.60, 255 * 0.69	], np.uint8)
	kidneyUpper = np.array(	[26, 	255, 		255			], np.uint8)
	heartLower = np.array(	[179, 	255 * 0.50, 255 * 0.35	], np.uint8)
	heartUpper = np.array(	[179, 	255 * 0.97, 255 * 0.69	], np.uint8)

	while elapsedTime < 1:

		_, imageFrame = cam.read()

		# Convert frame from BGR color space to HSV
		hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

		# Create masks for each organ
		colonMask = cv2.inRange(hsvFrame, colonLower, colonUpper)
		liverMask = cv2.inRange(hsvFrame, liverLower, liverUpper)
		stomachMask = cv2.inRange(hsvFrame, stomachLower, stomachUpper)
		brainMask = cv2.inRange(hsvFrame, brainLower, brainUpper)
		kidneyMask = cv2.inRange(hsvFrame, kidneyLower, kidneyUpper)
		heartMask = cv2.inRange(hsvFrame, heartLower, heartUpper)

		# Create a 5x5 square-shaped filter called kernel
		# Filter is filled with ones and will be used for morphological transformations such as dilation for better detection
		kernel = np.ones((5, 5), 'uint8')

		# For colon
		# Dilate mask: Remove holes in the mask by adding pixels to the boundaires of the objects in the mask
		colonMask = cv2.dilate(colonMask, kernel)
		liverMask = cv2.dilate(liverMask, kernel)
		stomachMask = cv2.dilate(stomachMask, kernel)
		brainMask = cv2.dilate(brainMask, kernel)
		heartMask = cv2.dilate(heartMask, kernel)
		# Use a larger kernel for heart and kidney masks
		kidneyMask = cv2.dilate(kidneyMask, np.ones((12, 12), 'uint8'))
		heartMask = cv2.dilate(heartMask, np.ones((12, 12), 'uint8'))

		# Create a contour around the zone that matches the color range
		contours, _ = cv2.findContours(colonMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		# Fo_ach countour, check if the area is greater than the threshold
		for _, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 700:
				# Append the name of the model to the list of objects
				if 'colon' not in objects:
					if objects == 'User is not holding any objects':
						objects = 'colon'
					else:
						objects = objects + ', colon'

		contours, _ = cv2.findContours(liverMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for _, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 500:
				if 'liver' not in objects:
					if objects == 'User is not holding any objects':
						objects = 'liver'
					else:
						objects = objects + ', liver'

		contours, _ = cv2.findContours(stomachMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for _, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 1400:
				if 'stomach' not in objects:
					if objects == 'User is not holding any objects':
						objects = 'stomach'
					else:
						objects = objects + ', stomach'

		contours, _ = cv2.findContours(brainMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for _, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 2500:
				if 'brain' not in objects:
					if objects == 'User is not holding any objects':
						objects = 'brain'
					else:
						objects = objects + ', brain'
		
		contours, _ = cv2.findContours(heartMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for _, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 650:
				if 'heart' not in objects:
					if objects == 'User is not holding any objects':
						objects = 'heart'
					else:
						objects = objects + ', heart'

		contours, _ = cv2.findContours(kidneyMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for _, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 50:
				if 'kidney' not in objects:
					if objects == 'User is not holding any objects':
						objects = 'kidney'
					else:
						objects = objects + ', kidney'

		elapsedTime = time.time() - startTime

		# This does not break the loop, but removing it breaks the camera feed and causes the program to crash
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# Release webcam and close all windows
	cam.release()
	cv2.destroyAllWindows()

def markerID(camera: int = 0):
	global objects
	objects = 'User is not holding any objects'

	# Choose the predefined dictionary to use
	arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

	# Define the names of the objects
	compoundDict = { 0: 'Citrate', 1: 'Isocitrate', 2: 'Alpha-Ketoglutarate', 3: 'Succinyl CoA', 4: 'Succinate', 5: 'Fumarate', 6: 'Malate', 7: 'Oxaloacetate' }

	cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW) # Use 0 for default camera

	# Start timer
	startTime = time.time()
	elapsedTime = 0


	while elapsedTime < 5:
		ret, frame = cap.read()

		if not ret:
			print('Failed to capture frame.')
			break

		# Convert the frame to grayscale for marker detection
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Detect markers
		_, ids, _ = cv2.aruco.detectMarkers(gray, arucoDict)

		if ids is not None:
			# For each marker found in current frame
			for i in range(len(ids)):
				try:
					# Try to get the name of the compound from the dictionary
					compoundName = compoundDict[ids[i][0]]
					# Append compound to list while avoiding repeats
					if objects == 'User is not holding any objects':
						objects = compoundName
					elif compoundName not in objects:
						objects += ', ' + compoundName
				except KeyError:
					continue

		# Display the frame
		cv2.imshow('Study-Bot View', frame)

		elapsedTime = time.time() - startTime
		key = cv2.waitKey(10) & 0xFF
		if key == 27:
			break

	cap.release()
	cv2.destroyAllWindows()

# Takes the topic number and camera number as arguments, if no camera number is provided, the default camera is used
def lookForObjects(topic: int, camera: int = 0):
	if topic == 1:
		# Call the function for color identification
		colorID(camera)
	elif topic == 2:
		# Call the function for marker identification
		markerID(camera)

def sendMessage(messageList: any):
	# Send prompt to GPT
	response = openAIClient.chat.completions.create(
		model = 'gpt-3.5-turbo',
		temperature = 0.2,
		messages = messageList
	)

	# print(response) # For debugging only
	gptAnswer = response.choices[0].message.content

	# Add the response to the message list
	messageList.append({'role': 'assistant', 'content': gptAnswer})

def convertTTS(answer: str):
	# threading.Thread(target = play, args = (elevenLabsClient.generate(text = answer, model = 'eleven_multilingual_v2', stream = True), False, False)).start()
	print('Audio playback disabled.\n')

# Functions for CLI version only
def sendMessageStreamAnswer(messageList: any):
	gptAnswer = ''

	stream = openAIClient.chat.completions.create(
    	model = 'gpt-3.5-turbo',
    	messages = messageList,
		temperature = 0.2,
    	stream=True,
	)

	for chunk in stream:
		print(chunk.choices[0].delta.content or '', end='', flush=True)

		if chunk.choices[0].delta.content is not None:
			gptAnswer += chunk.choices[0].delta.content

	messageList.append({'role': 'assistant', 'content': gptAnswer})

def stopRec():
	global stop
	stop = True

# Run on CLI version only
if __name__ == '__main__':
	# Listen for keyboard input to stop recording
	keyboard.add_hotkey('s', stopRec)
	selectedTopic = False

	while selectedTopic == False:
		print('Select a topic NUMBER from the list:\n')
		print('[1] - Human Body')
		print('[2] - Krebs Cycle\n')
		topic = int(input('Topic: '))
		source = ''

		# Load the source material based on the selected topic
		if topic == 1:
			print('Topic: Human Body\n')
			source = sourceMaterial.humanBody
			selectedTopic = True
		elif topic == 2:
			print('Topic: Krebs Cycle\n')
			source = sourceMaterial.krebsCycle
			selectedTopic = True
		else:
			print('Invalid topic number.\n')

	# Start question processing threads
	objID = threading.Thread(target = lookForObjects, args = (topic,))
	audioRec = threading.Thread(target = recordQuestion)

	objID.start()
	print('Looking for objects...\n')
	audioRec.start()
	print('Listening for question...\n')

	objID.join()
	print('Object detection complete.\n')
	print('Objects detected: ' + objects + '\n')
	audioRec.join()
	print('Question recorded.\n')
	print('Question: ' + question + '\n')

	# Build prompt
	query = f"""
	Objects held by user: {objects}.
	Question: {question}
	Information: 
	\"\"\"
	{source}
	\"\"\"
	"""

	# Send prompt to GPT
	messageHistory = [
		{'role': 'system', 'content': customInstructions},
		{'role': 'user', 'content': query},
	]

	print('Sending prompt to GPT...\n')
	sendMessageStreamAnswer(messageHistory)
	# Get the answer from the last message in the message history
	answer = next((msg for msg in reversed(messageHistory) if msg['role'] == 'assistant'), None)['content']

	# Convert answer to audio
	print('Converting answer to audio...\n')
	convertTTS(answer)

	# Conversation loop, handles any follow-up questions
	while True:
		print('Press space to ask another question, or press q to quit.\n')

		while True:
			if keyboard.is_pressed(' '):
				print('Preparing for next question, please hold...\n')
				break
			if keyboard.is_pressed('q'):
				print('Exiting program...\n')
				exit()

		# Reset variables
		objects = 'User is not holding any objects'
		question = ''

		# Restart threads

		objID = threading.Thread(target = lookForObjects, args = (topic,))
		audioRec = threading.Thread(target = recordQuestion)

		objID.start()
		print('Looking for objects...\n')
		audioRec.start()
		print('Listening for question...\n')

		objID.join()
		print('Object detection complete.\n')
		print('Objects detected: ' + objects + '\n')
		audioRec.join()
		print('Question recorded.\n')
		print('Question: ' + question + '\n')

		# Build new prompt and add to chat history
		query = f"""Objects held by user: {objects}.
Question: {question}
"""
		messageHistory.append({'role': 'user', 'content': query})
		answer = ''

		# Send prompt to GPT
		# print('Prompt: ' + query + '\n') # For debugging only
		print('Sending prompt to GPT...\n')

		sendMessage(messageHistory)
		answer = next((msg for msg in reversed(messageHistory) if msg['role'] == 'assistant'), None)['content']

		if answer != '':
			print('Answer: ' + answer + '\n\n')

		print('Converting answer to audio...\n')
		convertTTS(answer)