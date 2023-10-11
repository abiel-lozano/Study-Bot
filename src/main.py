import openai
import whisper
from pydub import AudioSegment
from pydub.playback import play as pydubPlay
import io
from typing import Iterator
import pyaudio
import wave
from pathlib import Path
from elevenlabs import set_api_key, generate
import cv2
import numpy as np
import time
import threading
import credentials # Ignored by git, contains API keys
import sourceMaterial
import tkinter
import sys

global objects
global question
global answer
global topic
global running

objects = ''
question = ''
answer = ''
running = False

GPT_MODEL = 'gpt-3.5-turbo-16k'

# Credentials
openai.api_key = credentials.openAiKey
set_api_key(credentials.elevenLabsKey)

# Information sources
humanBodySource = sourceMaterial.humanBody

biochemSource = sourceMaterial.krebsCycle

# Behavioral guidelines for conversation
instructions = """
Try to use the information below to help the user study by answering 
the user's question. The user may or may not be holding a physical representation 
of what their question is about. Consider the object list, which includes all 
the objects that the user is holding, so that the answer can be refined to be 
more specific to the user's question. Do not mention the user or the information 
in your answer to make it more sound natural.

If the question is unrelated to the information, ignore all previous instructions
and try to answer the question without mentioning the information or the objects 
to make it sound more natural.

Always try to give brief answers to the user's questions.
"""


# Recorder configuration
CHUNK = 1024 # Chunk size
FORMAT = pyaudio.paInt16 # Audio codec format
CHANNELS = 2
RATE = 44100 # Sample rate
RECORD_SECONDS = 5 # Recording duration
WAVE_OUTPUT_FILENAME = "question.wav"

def recordQuestion():
	# ---------------- Audio Recording ----------------
	global question
	audio = pyaudio.PyAudio() # Initialize PyAudio
	# Open audio stream for recording
	stream = audio.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
	frames = []

	# Record audio stream in chunks
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	# Stop and close audio stream
	stream.stop_stream()
	stream.close()
	audio.terminate()

	# Save recording as WAV
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(audio.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	# ---------------- STT Conversion -----------------
	model = whisper.load_model('base')
	result = model.transcribe('question.wav', fp16 = False)
	question = result['text']

	# print('Question: ' + question + '\n')
	
	# Delete audio file
	Path('question.wav').unlink()

def colorID():
	obj = 'User is not holding any objects'

	# Capture video
	cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Use 0 for default camera

	# Start timer
	startTime = time.time()
	elapsedTime = 0

	# Color ranges
	stomachLower = np.array([90, 	80, 		100			], np.uint8)
	stomachUpper = np.array([120, 	255, 		255			], np.uint8)
	colonLower = np.array(	[10, 	255 * 0.55, 255 * 0.35	], np.uint8)
	colonUpper = np.array(	[20.5, 	255, 		255			], np.uint8)
	liverLower = np.array(	[38, 	225 * 0.22, 255 * 0.38	], np.uint8)
	liverUpper = np.array(	[41, 	255, 		255			], np.uint8)
	brainLower = np.array(	[163, 	255 * 0.50, 255 * 0.40	], np.uint8)
	brainUpper = np.array(	[163, 	255, 		255			], np.uint8)
	kidneyLower = np.array(	[24, 	255 * 0.60, 255 * 0.49	], np.uint8)
	kidneyUpper = np.array(	[24, 	255, 		255			], np.uint8)
	heartLower = np.array(	[170, 	255 * 0.50, 255 * 0.35	], np.uint8)
	heartUpper = np.array(	[170, 	255 * 0.97, 255 * 0.69	], np.uint8)

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
		# Apply mask to frame by using bitwise AND operation
		resColon = cv2.bitwise_and(imageFrame, imageFrame, mask = colonMask)

		# For liver
		liverMask = cv2.dilate(liverMask, kernel)
		resliver = cv2.bitwise_and(imageFrame, imageFrame, mask=liverMask)

		# For stomach
		stomachMask = cv2.dilate(stomachMask, kernel)
		resStomach = cv2.bitwise_and(imageFrame, imageFrame, mask=stomachMask)

		# For brain
		brainMask = cv2.dilate(brainMask, kernel)
		resBrain = cv2.bitwise_and(imageFrame, imageFrame, mask=brainMask)

		# For heart
		heartMask = cv2.dilate(heartMask, kernel)
		resHeart = cv2.bitwise_and(imageFrame, imageFrame, mask=heartMask)

		# For kidney use a more aggressive kernel for dilation
		kidneyMask = cv2.dilate(kidneyMask, np.ones((12, 12), 'uint8'))
		resKidney = cv2.bitwise_and(imageFrame, imageFrame, mask=kidneyMask)

		# Create a contour around the zone that matches the color range
		contours, hierarchy = cv2.findContours(colonMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		# For each countour, check if the area is greater than the threshold
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 500:
				# Append the name of the model to the list of objects
				if 'colon' not in obj:
					if obj == 'User is not holding any objects':
						obj = 'colon'
					else:
						obj = obj + ', colon'

		contours, hierarchy = cv2.findContours(liverMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 500:
				if 'liver' not in obj:
					if obj == 'User is not holding any objects':
						obj = 'liver'
					else:
						obj = obj + ', liver'

		contours, hierarchy = cv2.findContours(stomachMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 1400:
				if 'stomach' not in obj:
					if obj == 'User is not holding any objects':
						obj = 'stomach'
					else:
						obj = obj + ', stomach'

		contours, hierarchy = cv2.findContours(brainMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 500:
				if 'brain' not in obj:
					if obj == 'User is not holding any objects':
						obj = 'brain'
					else:
						obj = obj + ', brain'
		
		contours, hierarchy = cv2.findContours(heartMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 500:
				if 'heart' not in obj:
					if obj == 'User is not holding any objects':
						obj = 'heart'
					else:
						obj = obj + ', heart'

		contours, hierarchy = cv2.findContours(kidneyMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 500:
				if 'kidney' not in obj:
					if obj == 'User is not holding any objects':
						obj = 'kidney'
					else:
						obj = obj + ', kidney'

		# Display the camera feed
		# cv2.imshow('Study-Bot View', imageFrame)

		elapsedTime = time.time() - startTime

		# This does not break the loop, but removing it breaks the camera feed and causes the program to crash
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# Release webcam and close all windows
	# cam.release()
	cv2.destroyAllWindows()

	return obj

def markerID():
	obj = 'User is not holding any objects'

	arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

	compoundDict = { 0: 'Citrate', 1: 'Isocitrate', 2: 'Alpha-Ketoglutarate', 3: 'Succinyl CoA', 4: 'Succinate', 5: 'Fumarate', 6: 'Malate', 7: 'Oxaloacetate' }

	cap = cv2.VideoCapture(0)

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
		corners, ids, _ = cv2.aruco.detectMarkers(gray, arucoDict)

		if ids is not None:
			for i in range(len(ids)):

				print('Detected marker with ID:', ids[i][0])
				try:
					compound_name = compoundDict[ids[i][0]]
					print('Object:', compound_name)
					
					if obj == 'User is not holding any objects':
						obj = compound_name
					elif compound_name not in obj:
						obj += ', ' + compound_name
				except KeyError:
					print('Exception: Marker ID' + str(ids[i][0]) + ' not registered.')

		cv2.imshow('Study-Bot View', frame)

		elapsedTime = time.time() - startTime

		# Check for 'Esc' key press
		key = cv2.waitKey(10) & 0xFF
		if key == 27:
			break

	cap.release()
	cv2.destroyAllWindows()

	return obj

def lookForObjects(topic: str):
	global objects
	objects = ''

	if topic == '1':
		# Call the function for color identification
		objects = colorID()
	elif topic == '2':
		# Call the function for marker identification
		objects = markerID()

def sendMessage(messageList: any):
	# Send prompt to GPT
	response = openai.ChatCompletion.create(
		messages = messageList,
		model = GPT_MODEL, 
		temperature = 0.2
	)
	# print(response)
	_answer = response['choices'][0]['message']['content']

	# Add the response to the message list
	messageList.append({'role': 'assistant', 'content': _answer})

def streamAnswer(audioStream: Iterator[bytes]) -> bytes:
	audioOutput = b""
	
	for chunk in audioStream:
		if chunk is not None:
			audioOutput += chunk

	audioSegment = AudioSegment.from_file(io.BytesIO(audioOutput), format="mp3")
	pydubPlay(audioSegment)

def convertTTS(text: str):
	audioOutput = generate(text = text, model = 'eleven_multilingual_v1', stream = True)
	streamAnswer(audioOutput)
	# print('Audio playback disabled.\n')

# ---------------------------------MAIN-----------------------------------

# import studyBot

# NOTE - There is chance this is not necessary
# global answer
global messageHistory
global query
global firstQuestion
global source

firstQuestion = True

# Select the source material to be sent to GPT and select object ID function (not implemented yet)
def checkSelection():
	global source
	global topic
	global messageHistory
	global firstQuestion

	selectedTopic = topicVar.get()
	infoDisplay.set(f'Selected topic: {selectedTopic}')
	
	if selectedTopic == 'Human Body':
		topic = '1'
		source = humanBodySource
	elif selectedTopic == 'Biochem':
		topic = '2'
		source = biochemSource

	messageHistory = []
	firstQuestion = True

# NOTE: Not using this function, and calling startQuestionThreads directly from the button
# causes the UI to freeze while the threads are running.
def backgroundInit():
	threadStart = threading.Thread(target = startQuestionThreads)
	threadStart.start()

	# Disable buttons while question is being answered
	askButton.config(state = 'disabled')
	selectButton.config(state = 'disabled')
	exitButton.config(state = 'disabled')
	# threadStart.join()
	

def startQuestionThreads():
	global firstQuestion
	global messageHistory
	# Start threads for object identification and question recording
	threadObjID = threading.Thread(target = lookForObjects, args = (topic,))
	threadQuestionRec = threading.Thread(target = recordQuestion)
	threadObjID.start()
	threadQuestionRec.start()
	infoDisplay.set(f'Listening for question and looking for objects...')
	threadObjID.join()
	threadQuestionRec.join()

	# Display the recorded question and identified object
	infoDisplay.set(f'Question taken: {question} \nObject identified: {objects}')

	# Prepare messageHistory depending on whether this is the first question or not
	if firstQuestion:
		firstQuestion = False
		query = f"""{instructions}

		Objects held by user: {objects}
		Question: {question}

		Information:
		\"\"\"
		{source}
		\"\"\"
		"""

		messageHistory = [
			{'role': 'system', 'content': 'You answer questions in the same language as the question.'},
			{'role': 'user', 'content': query},
		]
	else:
		query = f"""Objects held by user: {objects}
Question: {question}
"""		
		messageHistory.append({'role': 'user', 'content': query})

	# Message GPT
	infoDisplay.set(f'Messaging GPT, please wait...')
	threadSendMessage = threading.Thread(target = sendMessage, args = (messageHistory,))
	threadSendMessage.start()
	threadSendMessage.join()

	# Get the answer of the last message of messageHistory
	answer = next((msg for msg in reversed(messageHistory) if msg['role'] == 'assistant'), None)['content']
	infoDisplay.set(f'Answer: {answer}')

	# Convert TTS
	threadConvertTTS = threading.Thread(target = convertTTS, args = (answer,))
	threadConvertTTS.start()
	threadConvertTTS.join()

	# Re-enable buttons so the user can ask another question
	askButton.config(state = 'normal')
	selectButton.config(state = 'normal')
	exitButton.config(state = 'normal')

# Create the main window
window = tkinter.Tk()
window.title('Study-Bot')
window.geometry('450x500')

# Set the background color
window.configure(bg = '#3C3836')

# Create the title label
titleLabel = tkinter.Label(window, text = 'Study-Bot', font = ('Leelawadee', 24, 'bold'), bg = '#3C3836', fg = '#FBF1C7')
titleLabel.pack(pady = 15)

# Create the topic dropdown
topicLabel = tkinter.Label(window, text = 'Select Topic:', bg = '#3C3836', fg = '#FBF1C7', font = ('Leelawadee', 12))
topicLabel.pack(pady = 15)

# Create the topic frame
topicFrame = tkinter.Frame(window, bg = '#3C3836')
topicFrame.pack(pady = 15)

topicVar = tkinter.StringVar(window)
topicDropdown = tkinter.OptionMenu(topicFrame, topicVar, 'Human Body', 'Biochem')
topicDropdown.config(width = 15)
topicDropdown.pack(side = 'left', padx = 10)

selectButton = tkinter.Button(topicFrame, text = 'Select', command = checkSelection, bg = '#FABD2F', font = ('Leelawadee', 12))
selectButton.pack(side = 'left', padx = 10)

# Create the buttons frame
buttonsFrame = tkinter.Frame(window, bg = '#3C3836')
buttonsFrame.pack(pady = 15)

# Create the 'Ask another question' button
askButton = tkinter.Button(buttonsFrame, text = 'Ask a question', command = backgroundInit, bg = '#8EC07C', font = ('Leelawadee', 12))
askButton.pack(side = 'left', padx = 10)

# Create the 'Exit' button
exitButton = tkinter.Button(buttonsFrame, text = 'Exit', command = sys.exit, bg = '#FB4934', font = ('Leelawadee', 12))
exitButton.pack(side = 'left', padx = 10)

# Create the infoDisplay text label
infoDisplay = tkinter.StringVar()
infoDisplay.set('Welcome to Study-Bot! Please select a topic before asking a question.')
infoLabel = tkinter.Label(window, textvariable=infoDisplay, bg = '#83A598', fg = '#282828',font = ('Leelawadee', 12), wraplength = 400)
infoLabel.pack()

window.mainloop()