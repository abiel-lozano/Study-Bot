import studyBot
import tkinter
import sys
import winsound

studyBot.answer = ''
studyBot.question = ''
studyBot.objects = ''
studyBot.topic = 0
source = ''
firstQuestion = True
lastHistoryItem = ''

ENG = {
	# Audio Name ------- ID --------------------- Suggested Audio Descriptions
	'welcome': 			'Fcr09G5osIVgPdB54Gwe', # Welcome to Study-Bot! To begin, choose a topic from the dropdown menu using number 1 to go through the options. Then, select the topic by pressing number 2.
	'language': 		'FcRqjD9nTRQUbQchNBG8', # English
	'topicHumanBody': 	'Xpzofl8BcoZi3LpebPUQ', # Human Body
	'topicBiochem': 	'7dKNxFd2HIR30dKFwdmY', # Biochemistry
	'confirmHumanBody': 'gOLazidFXjWtAVHX2J6L', # Human Body selected. Be ready to present the objects to the camera. Then, use number 3 to start recording the question. The recording will begin after the tone. Use number 4 to stop recording.
	'confirmBiochem': 	'9WqViI4hHc4FGqQguMPq', # Biochemistry selected. Be ready to present the objects to the camera. Then, use number 3 to start recording the question. The recording will begin after the tone. Use number 4 to stop recording.
	'questionRecorded': 'XCs47V952gWAhZrZoNtO', # Question recorded, please wait.
}

ESP = {
	# Audio Name ------- ID --------------------- Suggested Audio Descriptions
	'welcome': 			'GZALP3KM1fBIH4uU2of7', # Hola! Para comenzar, elige un tema del menú usando el número uno para navegar las opciones. Después, selecciona el tema presionando el número dos.
	'language': 		'IIH34ANdEoFnUh9mn7Dn', # Español
	'topicHumanBody': 	'hHEoz72Yl43NrxelKrkE', # Cuerpo Humano
	'topicBiochem': 	'fYqUQJcQHkPm1EJ3F2SM', # Bioquímica
	'confirmHumanBody': '8YIW9hjNIvcAivStBGRB', # Cuerpo Humano seleccionado. Prepárate para presentar los objetos a la cámara. Luego, presiona el número tres para comenzar a grabar la pregunta. La grabación comenzará después del tono. Usa el número cuatro para detener la grabación cuando hayas terminado.
	'confirmBiochem': 	'diSUSBcjZoyuKwTBtfpL', # Bioquímica seleccionada. Prepárate para presentar los objetos a la cámara. Luego, presiona el número tres para comenzar a grabar la pregunta. La grabación comenzará después del tono. Usa el número cuatro para detener la grabación cuando hayas terminado.
	'questionRecorded': 'UkKdDEpH3g8DeRHA9w3V', # Pregunta grabada. Por favor espera.
}

# Select default audio language here
audioSelect = ENG

# Play specific history item ID
def playAudioWithID(itemID: str):
	# PLay audio if audio instructions are enabled
	if audioInstructions.get():
		threadAudio = studyBot.threading.Thread(target = studyBot.play, args = (studyBot.elevenLabsClient.history.get_audio(itemID), False, False))
		threadAudio.start()

def replay():
	# Refresh audio history, play the last audio item
	global audioHistory
	audioHistory = studyBot.elevenLabsClient.history.get_all()
	studyBot.threading.Thread(target = studyBot.play, args = (audioHistory.history[0].history_item_id, False, False)).start()

def toggleAudioDesc():
	global audioInstructions
	audioInstructions.set(not audioInstructions.get()) # Invert boolean value

	if audioInstructions.get():
		winsound.Beep(700, 400)
	else:
		winsound.Beep(500, 400)

# Switch between English and Spanish audio, depending on the selected language
def selectAudioLanguage():
	global audioSelect

	if langVar.get() == '<C> English':
		audioSelect = ESP
		langVar.set('<C> Español')
	else:
		audioSelect = ENG
		langVar.set('<C> English')

	playAudioWithID(audioSelect['language'])

# Select next option in dropdown menu
def selectNextOption():
	currentIndex = options.index(topicVar.get()) # Get index of current option
	nextIndex = (currentIndex + 1) % len(options) # Get index of next option by adding 1 and wrapping around
	nextOption = options[nextIndex]
	topicVar.set(nextOption)

	# Play audio for selected option
	if nextOption == '<1> Human Body':
		playAudioWithID(audioSelect['topicHumanBody'])
	elif nextOption == '<1> Biochem':
		playAudioWithID(audioSelect['topicBiochem'])
	# Add new topics here

# Select source material to be sent to GPT and select object ID function
def checkSelection():
	global source
	global messageHistory
	global firstQuestion
	global query

	winsound.Beep(600, 800) # frequency, duration
	
	topic = topicVar.get()
	# Remove the first 4 characters of topic string '<1> ' to get the topic name
	infoDisplay.set(f'Selected topic: {topic[4:]}')
	
	# Set the topic for the studyBot module
	# Set the source material for the message
	# Play audio confirmation for selected topic
	if topic == '<1> Human Body':
		studyBot.topic = 1
		source = studyBot.sourceMaterial.humanBody
		playAudioWithID(audioSelect['confirmHumanBody'])
	elif topic == '<1> Biochem':
		studyBot.topic = 2
		source = studyBot.sourceMaterial.krebsCycle
		playAudioWithID(audioSelect['confirmBiochem'])
	# Add new topics here

	# Check if the 'Ask Question' button isn't already bound
	if window.bind('3') == '':
		window.bind('3', lambda _: backgroundInit())
		askButton.config(state = 'normal')

	# Resets message history, firstQuestion, and query if the topic is changed
	messageHistory = []
	firstQuestion = True
	query = ''
	
# Allow the question processing threads to start and join in the background
# using threadOrchestration() while the UI remains responsive
def backgroundInit():
	# Gets the show running by calling all the study-Bot functions
	threadStart = studyBot.threading.Thread(target = threadOrchestration)
	threadStart.start()

	# Disable buttons while question is being processed
	topicDropdown.config(state = 'disabled')
	selectButton.config(state = 'disabled')
	askButton.config(state = 'disabled')
	replayButton.config(state = 'disabled')
	# Enable stop button
	stopButton.config(state = 'normal')

	# Unbind keys while question is being processed
	window.unbind('1')
	window.unbind('2')
	window.unbind('3')
	window.unbind('r')
	# Bind stop recording key
	window.bind('4', lambda _: stopRecording())

def threadOrchestration():
	global firstQuestion
	global messageHistory
	global query
	global cameraVar

	# Perform object detection and question recording concurrently, wait for results
	threadObjID = studyBot.threading.Thread(target = studyBot.lookForObjects, args = (studyBot.topic, int(cameraVar.get()[7:]) - 1)) # Get camera selection from dropdown menu
	threadQuestionRec = studyBot.threading.Thread(target = studyBot.recordQuestion)
	threadTimeLimiter = studyBot.threading.Thread(target = timeLimiter)
	
	threadObjID.start()
	threadTimeLimiter.start()
	threadQuestionRec.start()

	winsound.Beep(700, 600)
	infoDisplay.set(f'Listening for question and looking for objects...')

	threadObjID.join()
	threadQuestionRec.join()

	# Display recorded question and identified object
	infoDisplay.set(f'Question taken: {studyBot.question} \nObject identified: {studyBot.objects} \nMessaging GPT, please wait...')

	# Build prompt for GPT  
	# Prepare messageHistory if this is the first question
	if firstQuestion:
		firstQuestion = False
		query = f'Objects held by user: {studyBot.objects} Question: {studyBot.question} Information:{source}'

		messageHistory = [
			{'role': 'system', 'content': studyBot.customInstructions},
			{'role': 'user', 'content': query},
		]
	# Otherwise, just add the question to the messageHistory
	else:
		query = f'Objects held by user: {studyBot.objects} Question: {studyBot.question}'
		messageHistory.append({'role': 'user', 'content': query})

	# Message GPT
	# threadSendMessage = studyBot.threading.Thread(target = studyBot.sendMessage, args = (messageHistory,))
	# threadSendMessage.start()
	# threadSendMessage.join()

	# Get answer of last message from messageHistory

	# # Convert TTS
	# threadConvertTTS = studyBot.threading.Thread(target = studyBot.convertTTS, args = (answer,))
	# threadConvertTTS.start()
	# threadConvertTTS.join()

	studyBot.threading.Thread(target = studyBot.playAudioFromQueue).start()
	threadSendMessage = studyBot.threading.Thread(target = studyBot.asyncio.run, args = (studyBot.sendMessage(),)).start()
	threadSendMessage.join()


	answer = next((msg for msg in reversed(messageHistory) if msg['role'] == 'assistant'), None)['content']
	infoDisplay.set(f'Answer: {answer}')

	# Enable buttons
	topicDropdown.config(state = 'normal')
	selectButton.config(state = 'normal')
	askButton.config(state = 'normal')
	replayButton.config(state = 'normal')

	# Bind keys
	window.bind('1', lambda _: selectNextOption())
	window.bind('2', lambda _: checkSelection())
	window.bind('3', lambda _: backgroundInit())
	window.bind('r', lambda _: replay())

def timeLimiter():
	# While the user hasn't stopped the recording, or less than 1 second has passed, and more than 30 have not passed
	while (not studyBot.stop or studyBot.time.time() - studyBot.startTime < 1) and studyBot.time.time() - studyBot.startTime < 30:
		continue
	
	# If the user has not called stopRecording()
	if not studyBot.stop:
		stopRecording()

def stopRecording():
	studyBot.stop = True
	winsound.Beep(700, 300) # Stop signal
	# Disable stop button and unbind stop key
	stopButton.config(state = 'disabled')
	window.unbind('4')
	playAudioWithID(audioSelect['questionRecorded']) # Play audio confirmation

# Given a camera index, open the camera for 3 seconds and display the feed
def testCamera(index: int):
	cap = studyBot.cv2.VideoCapture(index, studyBot.cv2.CAP_DSHOW)
	start = studyBot.time.time()
	elapsedTime = 0

	while elapsedTime < 3:
		ret, frame = cap.read()
		if not ret:
			break
		studyBot.cv2.imshow('Frame', frame)
		elapsedTime = studyBot.time.time() - start
		key = studyBot.cv2.waitKey(10) & 0xFF
		if key == 27:
			break
		
	cap.release()
	studyBot.cv2.destroyAllWindows()

def close():
	# Wake up system sounds
	winsound.Beep(37, 600) # Unaudible frequency in most speakers

	# Closing signal
	winsound.Beep(700, 250) 
	studyBot.time.sleep(0.01) # Avoid overlapping sounds and popping
	winsound.Beep(600, 250)
	studyBot.time.sleep(0.01)
	winsound.Beep(500, 250)
	
	sys.exit()

# Using cv2 from studyBot, test and count all cameras until failure
i = 0
while True:
	testCap = studyBot.cv2.VideoCapture(i, studyBot.cv2.CAP_DSHOW)

	if not testCap.isOpened():
		break

	testCap.release()
	i += 1

# Create main window
window = tkinter.Tk()
window.title('Study-Bot')
window.geometry('525x500')

# Set background color
window.configure(bg = '#282828')

# Create title label
titleLabel = tkinter.Label(
	window, 
	text = 'Study-Bot', 
	font = ('Leelawadee', 24, 'bold'), 
	bg = '#282828', 
	fg = '#FBF1C7'
)
titleLabel.pack(pady = 15)

# Audio instructions checkbox
audioInstructions = tkinter.BooleanVar()
audioInstructions.set(True)

audioCheckBox = tkinter.Checkbutton(
	window, 
	text = '<Spacebar> Audio feedback and instructions',
	font = ('Leelawadee', 12),
	bg = '#282828',
	fg = '#FBF1C7',
	selectcolor = '#282828',
	activebackground = '#282828',
	activeforeground = '#FBF1C7',
	variable = audioInstructions
)
audioCheckBox.pack(pady = 0)

# Create audio language frame
langFrame = tkinter.Frame(window, bg = '#282828')
langFrame.pack(pady = 8)

# Create language label
langLabel = tkinter.Label(
	langFrame,
	text = 'Select audio language:', 
	bg = '#282828', 
	font = ('Leelawadee', 12), 
	fg = '#FBF1C7'
)
langLabel.pack(pady=8)

langVar = tkinter.StringVar(window)
langVar.set('<C> Español') # default value
langDropdown = tkinter.OptionMenu(
	langFrame, 
	langVar,
	'<C> Español',
	'<C> English'
)

langDropdown.config(width = 15)
langDropdown.pack(
	side = 'right', 
	padx = 10
)

# Create camera frame
camFrame = tkinter.Frame(window, bg = '#282828')
camFrame.pack(pady = 7)

cameraVar = tkinter.StringVar(camFrame)
cameraVar.set(f'Camera 1') # default value
cameraDropdown = tkinter.OptionMenu(
	camFrame, 
	cameraVar,
	*[f'Camera {i + 1}' for i in range(i)] # Dropdown menu items
)
cameraDropdown.config(width = 15)
cameraDropdown.pack(side = 'left', padx = 10)

# Create camera test button
cameraButton = tkinter.Button(
	camFrame, 
	text = 'Test Camera', 
	command = lambda: testCamera(int(cameraVar.get()[7:]) - 1), # Get camera index from dropdown menu text
	bg = '#b16286', 
	font = ('Leelawadee', 12)
)
cameraButton.pack(side = 'left', padx = 5)

# Create topic frame
topicFrame = tkinter.Frame(window, bg = '#282828')
topicFrame.pack(pady = 15)

topicVar = tkinter.StringVar(window)
topicVar.set('<1> Human Body') # default value
topicDropdown = tkinter.OptionMenu(
	topicFrame, 
	topicVar,
	'<1> Human Body',
	'<1> Biochem'
)
topicDropdown.config(width = 15)
topicDropdown.pack(
	side = 'left', 
	padx = 10
)

selectButton = tkinter.Button(
	topicFrame, 
	text = '<2> Select Topic', 
	command = checkSelection, 
	bg = '#FABD2F', 
	font = ('Leelawadee', 12)
)
selectButton.pack(
	side = 'left', 
	padx = 10
)

conversationControls = tkinter.Frame(
	window, 
	bg = '#282828'
)
conversationControls.pack(pady = 10)

askButton = tkinter.Button(
	conversationControls, 
	text = '<3> Ask Question', 
	command = backgroundInit, 
	bg = '#8EC07C', 
	font = ('Leelawadee', 12)
)
askButton.pack(
	side = 'left',
	padx = 10
)

stopButton = tkinter.Button(
	conversationControls,
	text = '<4> Stop Recording',
	command = stopRecording,
	bg = '#FE8019',
	font = ('Leelawadee', 12)
)

stopButton.pack(
	side = 'left',
	padx = 10
)

replayButton = tkinter.Button(
	conversationControls,
	text = '<R> Replay Answer',
	command = lambda: replay(),
	bg = '#458588',
	font = ('Leelawadee', 12)
)

replayButton.pack(
	side = 'left',
	padx = 10
)

exitFrame = tkinter.Frame(
	window, 
	bg = '#282828'
)
exitFrame.pack(pady = 8)

exitButton = tkinter.Button(
	exitFrame, 
	text = '<esc> Exit', 
	command = close, 
	bg = '#FB4934', 
	font = ('Leelawadee', 12)
)
exitButton.pack()

infoDisplay = tkinter.StringVar()
infoDisplay.set('Welcome to Study-Bot! Please select a topic before asking a question.')
infoLabel = tkinter.Label(
	window, 
	textvariable=infoDisplay, 
	bg = '#282828',
	fg = '#FBF1C7',
	font = ('Leelawadee', 12), 
	wraplength = 400,
	justify='left'
)
infoLabel.pack()

options = []

# For each option in the dropdown menu, add it to the options list
for i in range(topicDropdown['menu'].index('end') + 1): # Size of dropdown menu
	optionLabel = topicDropdown['menu'].entrycget(i, 'label')
	options.append(optionLabel)

# Setup before main loop

# Keyboard bindings for all functions with keys 1, 2, 3, 4 and Esc
window.bind('1', lambda _: selectNextOption())
window.bind('2', lambda _: checkSelection())
window.bind('<Escape>', lambda _: close())
window.bind('<space>', lambda _: toggleAudioDesc())
window.bind('c', lambda _: selectAudioLanguage())
window.bind('w', lambda _: playAudioWithID(audioSelect['welcome']))

# Stop, ask, and replay buttons disabled by default
stopButton.config(state = 'disabled')
askButton.config(state = 'disabled')
replayButton.config(state = 'disabled')

# Access get_all() method from elevenLabsClient in studyBot module
audioHistory = studyBot.elevenLabsClient.history.get_all()

# NOTE: System sounds are not always immediately enabled, which causes 
# the first sounds to be inaudible. This beep is used to 'wake up' the 
# system sounds.
winsound.Beep(37, 1000) # Unaudible frequency in most speakers

# Boot-up signal
window.after(0, winsound.Beep, 500, 350)
studyBot.time.sleep(0.01) # Avoid overlapping sounds and popping
window.after(310, winsound.Beep, 630, 350)
studyBot.time.sleep(0.01)
window.after(610, winsound.Beep, 750, 350)

window.after(1000, playAudioWithID, audioSelect['welcome']) # Play welcome audio
window.mainloop()