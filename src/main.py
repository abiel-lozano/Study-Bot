import studyBot
import tkinter
import sys
import winsound

# NOTE - There is chance this is not necessary
global answer
global messageHistory
global query
global firstQuestion
global source
global audioHistory
global audioInstructions

answer = ''
studyBot.question = ''
studyBot.objects = ''
studyBot.topic = 0
source = ''
firstQuestion = True

ENG = {
	'questionRecorded': '7aNkMntxEq7M9IXZ6Vkv',
	'welcome': 			'HNwmc11X0p23y77VLvOY',
	'topicHumanBody': 	'ppXHdy46xuZtg3ysNoxu',
	'topicBiochem': 	'IjsDkrqkOCQ64XyqL5ZV',
	'confirmHumanBody': 'OCE5HysrlHaX1AoGDd1j',
	'confirmBiochem': 	'CPjy6303qpWpSUEl07xz',
}

ESP = {
	'questionRecorded': 'bYlleFyvske67zV4Wr2Z',
	'welcome': 			'wij7p8zqa3uKAJMevWFT',
	'topicHumanBody': 	'OIZ9eoFel81KKe7eMjEN',
	'topicBiochem': 	'KLMTeyIhaa2hTeFahZAU',
	'confirmHumanBody': 'A0AHMdfV5qFgohvvwIdp',
	'confirmBiochem': 	'NybAwxFeEYpFKEKymRvu',
}

# Select audio language here
audioSelect = ENG

# NOTE: This is a patch for elevenlabs' play function, to avoid showing an
# empty black window when playing audio in the compiled version. The lack of
# this flag is not an issue when running through the interpreter.
def playPatch(audio: bytes, notebook: bool = False) -> None:
	if notebook:
		from IPython.display import Audio, display
		display(Audio(audio, rate=44100, autoplay=True))
	else:
		# Access subprocess module through elevenlabs from studyBot 
		# to avoid double import
		if not studyBot.is_installed("ffplay"):
			raise ValueError("ffplay from ffmpeg not found, necessary to play audio.")
		
		args = ["ffplay", "-autoexit", "-", "-nodisp"]
		proc = studyBot.subprocess.Popen(
			args = args,
			stdout = studyBot.subprocess.PIPE,
			stdin = studyBot.subprocess.PIPE,
			stderr = studyBot.subprocess.PIPE,
			# Flag prevents black window from showing
			creationflags = studyBot.subprocess.CREATE_NO_WINDOW,
		)
		out, err = proc.communicate(input=audio)
		proc.poll()

def toggleAudioDesc(event = None):
	global audioInstructions
	audioInstructions.set(not audioInstructions.get())

	if audioInstructions.get():
		winsound.Beep(700, 300)
	else:
		winsound.Beep(500, 300)

# Play specific history item ID
def playAudioWithID(itemID):
	global audioHistory
	global audioInstructions

	if audioInstructions.get():
		for item in audioHistory:
			if item.history_item_id == itemID:
				threadAudio = studyBot.threading.Thread(target = playPatch, args = (item.audio,))
				threadAudio.start()

# Select source material to be sent to GPT and select object ID function
def checkSelection():
	global source
	global messageHistory
	global firstQuestion
	global query

	winsound.Beep(600, 800) # frequency, duration
	
	topic = topicVar.get()
	# Remove the first 4 characters of topic string
	infoDisplay.set(f'Selected topic: {topic[4:]}')
	
	if topic == '<1> Human Body':
		studyBot.topic = 1
		source = studyBot.sourceMaterial.humanBody
		playAudioWithID(audioSelect['confirmHumanBody'])

	elif topic == '<1> Biochem':
		studyBot.topic = 1
		source = studyBot.sourceMaterial.krebsCycle
		playAudioWithID(audioSelect['confirmBiochem'])
	# Add new topics here

	if window.bind('3') == '':
		window.bind('3', lambda e: backgroundInit())
		askButton.config(state = 'normal')

	# Resets message history, firstQuestion, and query if the topic is changed
	messageHistory = []
	firstQuestion = True
	query = ''
	

# NOTE: Not using this function, and calling startQuestionThreads directly from the button
# causes the UI to freeze while the threads are running.
def backgroundInit():
	threadStart = studyBot.threading.Thread(target = startQuestionThreads)
	threadStart.start()

	# Disable all buttons while question is being processed
	topicDropdown.config(state = 'disabled')
	selectButton.config(state = 'disabled')
	stopButton.config(state = 'normal')
	askButton.config(state = 'disabled')
	exitButton.config(state = 'disabled')

	# Unbind keys while question is being processed
	window.unbind('1')
	window.unbind('2')
	window.unbind('3')
	window.bind('4', lambda e: stopRecording())
	window.unbind('<Escape>')

def startQuestionThreads():
	global firstQuestion
	global messageHistory
	global query

	# Start threads for object identification and question recording
	threadObjID = studyBot.threading.Thread(target = studyBot.lookForObjects, args = (studyBot.topic,))
	threadQuestionRec = studyBot.threading.Thread(target = studyBot.recordQuestion)
	threadObjID.start()
	threadQuestionRec.start()
	winsound.Beep(700, 600)
	infoDisplay.set(f'Listening for question and looking for objects...')
	threadObjID.join()
	threadQuestionRec.join()

	# Display recorded question and identified object
	infoDisplay.set(f'Question taken: {studyBot.question} \nObject identified: {studyBot.objects} \nMessaging GPT, please wait...')

	# Prepare messageHistory if this is the first question or not
	if firstQuestion:
		firstQuestion = False
		query = f"""{studyBot.instructions}

		Objects held by user: {studyBot.objects}
		Question: {studyBot.question}

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
		query = f"""Objects held by user: {studyBot.objects}
Question: {studyBot.question}
"""		
		messageHistory.append({'role': 'user', 'content': query})

	# Message GPT
	threadSendMessage = studyBot.threading.Thread(target = studyBot.sendMessage, args = (messageHistory,))
	threadSendMessage.start()
	threadSendMessage.join()

	# Get answer of last message from messageHistory
	answer = next((msg for msg in reversed(messageHistory) if msg['role'] == 'assistant'), None)['content']
	infoDisplay.set(f'Answer: {answer}')

	# Convert TTS
	threadConvertTTS = studyBot.threading.Thread(target = studyBot.convertTTS, args = (answer,))
	threadConvertTTS.start()
	threadConvertTTS.join()

	# Reenable buttons
	topicDropdown.config(state = 'normal')
	selectButton.config(state = 'normal')
	askButton.config(state = 'normal')
	exitButton.config(state = 'normal')

	# Rebind keys
	window.bind('1', lambda e: selectNextOption())
	window.bind('2', lambda e: checkSelection())
	window.bind('3', lambda e: backgroundInit())
	window.bind('<Escape>', lambda e: close())

	# Unbind stop recording key
	window.unbind('4')


# Select next option in dropdown menu
def selectNextOption():
	currentOption = topicVar.get()
	currentIndex = options.index(currentOption)
	nextIndex = (currentIndex + 1) % len(options)
	nextOption = options[nextIndex]
	topicVar.set(nextOption)

	# Play audio for selected option
	if nextOption == '<1> Human Body':
		playAudioWithID(audioSelect['topicHumanBody'])
	elif nextOption == '<1> Biochem':
		playAudioWithID(audioSelect['topicBiochem'])
	# Add new topics here

def close():
	# Closing signal
	winsound.Beep(700, 200) 
	studyBot.time.sleep(0.01)
	winsound.Beep(600, 200)
	studyBot.time.sleep(0.01)
	winsound.Beep(500, 200)
	sys.exit()

def stopRecording():
	studyBot.stopRecording()
	winsound.Beep(700, 300)
	playAudioWithID(audioSelect['questionRecorded'])
	stopButton.config(state = 'disabled')
	window.unbind('4')

# Create main window
window = tkinter.Tk()
window.title('Study-Bot')
window.geometry('450x350')

# Set background color
window.configure(bg = '#3C3836')

# Create title label
titleLabel = tkinter.Label(
	window, 
	text = 'Study-Bot', 
	font = ('Leelawadee', 24, 'bold'), 
	bg = '#3C3836', 
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
    bg = '#3C3836',
    fg = '#FBF1C7',
    selectcolor = '#3C3836',
    activebackground = '#3C3836',
    activeforeground = '#FBF1C7',
    variable = audioInstructions
)

audioCheckBox.pack(pady = 7)

# Create topic frame
topicFrame = tkinter.Frame(window, bg = '#3C3836')
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

# Create buttons frame
buttonsFrame = tkinter.Frame(
	window, 
	bg = '#3C3836'
)
buttonsFrame.pack(pady = 15)

# Create 'Ask another question' button
askButton = tkinter.Button(
	buttonsFrame, 
	text = '<3> Ask Question', 
	command = backgroundInit, 
	bg = '#8EC07C', 
	font = ('Leelawadee', 12)
)
askButton.pack(
	side = 'left', 
	padx = 10
)

# Create stop recording button
stopButton = tkinter.Button(
	buttonsFrame,
	text = '<4> Stop Recording',
	command = stopRecording,
	bg = '#FE8019',
	font = ('Leelawadee', 12)
)

stopButton.pack(
	side = 'left',
	padx = 10
)

# Create 'Exit' button
exitButton = tkinter.Button(
	buttonsFrame, 
	text = '<esc> Exit', 
	command = close, 
	bg = '#FB4934', 
	font = ('Leelawadee', 12)
)
exitButton.pack(
	side = 'left', 
	padx = 10
)

# Create infoDisplay text label
infoDisplay = tkinter.StringVar()
infoDisplay.set('Welcome to Study-Bot! Please select a topic before asking a question.')
infoLabel = tkinter.Label(
	window, 
	textvariable=infoDisplay, 
	bg = '#83A598', 
	fg = '#282828',
	font = ('Leelawadee', 12), 
	wraplength = 400
)
infoLabel.pack()

# Access from_api() method from History class through studyBot module
audioHistory = studyBot.History.from_api()

menu = topicDropdown['menu']
numOptions = menu.index('end') + 1
options = []

for i in range(numOptions):
	optionLabel = menu.entrycget(i, 'label')
	options.append(optionLabel)

# Keyboard bindings for all functions with keys 1, 2, 3, 4 and Esc
window.bind('1', lambda e: selectNextOption())
window.bind('2', lambda e: checkSelection())
window.bind('<Escape>', lambda e: close())
window.bind('<space>', lambda e: toggleAudioDesc())

# Stop and ask buttons disabled by default
stopButton.config(state = 'disabled')
askButton.config(state = 'disabled')


# NOTE: System sounds are not always immediately enabled, which causes 
# the first sounds to be inaudible. This beep is used to 'wake up' the 
# system sounds.
winsound.Beep(37, 500) # Unaudible frequency in most speakers and by most people

# Boot-up signal
window.after(0, winsound.Beep, 500, 200)
studyBot.time.sleep(0.01)
window.after(310, winsound.Beep, 630, 200)
studyBot.time.sleep(0.01)
window.after(610, winsound.Beep, 750, 200)

window.after(1000, playAudioWithID, audioSelect['welcome']) # Play welcome audio
window.mainloop()