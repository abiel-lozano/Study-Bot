# Study-Bot - main.py

>This documentation was created for version 1.0 of Study-Bot, in December 2023

## Description

This script has all of **StudyBot's** functionalities adapted to a GUI using `tkinter`. Consider that this document is meant to be read after the [studyBot.md](studyBot.md) document.

## Usage

To run this version, run this command from the root directory of the project.

```bash
python src/main.py
```

## Code Walkthrough

### Imports

```python
import studyBot
import tkinter
import sys
import winsound
```

- `studyBot`: Import all functions, variables, and modulues imported in `studyBot.py`.
- `tkinter`: Used to create simple GUIs for Python scripts.
- `sys`: Provides access system-specific parameters and functions, used to exit the program.
- `winsound`: Allows control of **Windows** system sounds, used to play beeps as signals to the user.

### Global Variables, studyBot Variables, and Audio Assistance

These dictionaries contain the IDs of audio generated with **Elevenlabs**. The audio recordings are used to play audio instructions and feedback to the user. The IDs come from the generation history of a specific **Elevenlabs** account, so you will need to generate *your own audio files* and replace the IDs in the dictionaries. See [Tools/speechGenerator.py](../Tools/speechGenerator.py) for more information on how to obtain these IDs.

```python
# NOTE - There is a chance this is not necessary
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
	'welcome': 	    'HNwmc11X0p23y77VLvOY',
	'topicHumanBody':   'ppXHdy46xuZtg3ysNoxu',
	'topicBiochem':     'IjsDkrqkOCQ64XyqL5ZV',
	'confirmHumanBody': 'OCE5HysrlHaX1AoGDd1j',
	'confirmBiochem':   'CPjy6303qpWpSUEl07xz',
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
```	

### Audio Assistance: `playPatch()`, `toggleAudioDesc`, and `playAudioWithID()`

The `playPatch()` function is a patch of the `play()` function from `elevenlabs`. This was necessary because the default `play()` function would create a blank window while playing audio when **Study-Bot** runs as a compiled executable. 

This is fixed by simply adding the `CREATE_NO_WINDOW` flag to the `subprocess.Popen()` function. The `subprocess` module and `is_installed()` are used through the `studyBot` module to avoid double imports.

```python
# NOTE: This is a patch for elevenlabs' play function, to avoid showing an
# empty black window when playing audio in the compiled version. The lack of
# this flag is not an issue when using the Python interpreter. The specific 
# playback method for Jupiter Notebooks was removed, as it is not necessary
# for this application.
def playPatch(audio: bytes) -> None:
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
```	

Play a specific audio file from your **Elevenlabs** history with this. Create a new thread for `playPatch()` so that it can run in the background without freezing the UI. Consider that this function assumes that your `History` has been fetched from the API, and that the audio ID exists.

```python
# Play specific history item ID
def playAudioWithID(itemID):
	global audioHistory
	global audioInstructions

	# Check if user disabled audio instructions
	if audioInstructions.get():
		# Find item with matching ID
		for item in audioHistory:
			if item.history_item_id == itemID:
				threadAudio = studyBot.threading.Thread(target = playPatch, args = (item.audio,))
				threadAudio.start()
```

Toggle audio instructions with the  spacebar. This function is called when the spacebar is pressed, and it toggles the value of the `audioInstructions` variable, which is a `tkinter.BooleanVar()`, distinct from a regular boolean variable. This is because `tkinter` variables can be linked to UI elements, such as the *checkbox*, and they will update automatically when the variable is changed and vice versa.

```python
def toggleAudioDesc(event = None):
	global audioInstructions
	# Invert boolean value
	audioInstructions.set(not audioInstructions.get())

	if audioInstructions.get():
		winsound.Beep(700, 300)
	else:
		winsound.Beep(500, 300)
```

### Topic Selector: `selectNextOption()` and `checkSelection()`

The topic selector is a simple dropdown menu that allows the user to select the topic they want to ask questions about. 

The `selectNextOption()` function is only needed when using the keyboard to interact with the program. It is called when the user presses the `1` key, which causes the dropdown menu to select the next option in the topic list.

```python
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
```

The `checkSelection()` function is called when the user presses the `Select Topic` button or the `2` key. It checks the value of the dropdown menu and sets the `source` variable to the corresponding source text, sets the `studyBot.topic` variable for choosing the object identification method, and plays the audio that tells the user what they just selected. 

It also updates the `infoDisplay` variable to show the selected topic, which is displayed in the UI, and used as a replacement for `print()` in the CLI version for showing the program's status.

```python
# Select source material to be sent to GPT and select object ID function
def checkSelection():
	global source
	global messageHistory
	global firstQuestion
	global query

	winsound.Beep(600, 800) # frequency, duration
	
	topic = topicVar.get()
	# Remove the first 4 characters of topic string for cleaner display
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
		window.bind('3', lambda e: backgroundInit())
		askButton.config(state = 'normal')

	# Resets message history, firstQuestion, and query if the topic is changed
	messageHistory = []
	firstQuestion = True
	query = ''
```

Note that this action also binds the `3` key to the `backgroundInit()` function, and enables the `Ask Question` button because the user is not allowed to ask a question before selecting a topic, and it also resets the `messageHistory`, `firstQuestion`, and `query` variables, just in case the topic is changed after asking a question from a different topic.


### Question processing: `backgroundInit()` and `startQuestionThreads()`

To allow the GUI to run while the program is processing the question, **multithreading** is necessary to perform any and all tasks that take more than a few miliseconds to complete, otherwise the GUI would freeze while the question is being processed.

This is achieved by calling `backgroundInit()`, which starts a new thread with `startQuestionThreads()` that calls the functions that process the question and generate the answer. It will create threads for each of the required processes that call functions from the studyBot module.

From `backgroundInit()`, the topic selector, 'Select Topic' button, and the 'Ask Question' button are disabled, and the keys to those functions are unbinded, since the user is not supposed to ask another question or change the topic during question processing.

The button for `stopRecording()` and its key binding are enabled during this time, which allows the user to stop the recording of their question when they are done speaking.

>Note: Since the `threading` module is imported in studyBot, it is not necessary to import it again in this script and it can be used through the studyBot module.

```python
def backgroundInit():
	# Gets the show running by calling all the study-Bot functions
	threadStart = studyBot.threading.Thread(target = startQuestionThreads)
	threadStart.start()

	# Disable buttons while question is being processed
	topicDropdown.config(state = 'disabled')
	selectButton.config(state = 'disabled')
	askButton.config(state = 'disabled')
	# Enable stop button
	stopButton.config(state = 'normal')

	# Unbind keys while question is being processed
	window.unbind('1')
	window.unbind('2')
	window.unbind('3')
	# Bind stop recording key
	window.bind('4', lambda e: stopRecording())

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

	# Assemble prompt for GPT
	# Prepare messageHistory if this is the first question
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
	# Otherwise, just add the question to the messageHistory
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

	# Rebind keys
	window.bind('1', lambda e: selectNextOption())
	window.bind('2', lambda e: checkSelection())
	window.bind('3', lambda e: backgroundInit())

	# Unbind stop recording key
	window.unbind('4')
```

After the answer was read out loud, the state of the buttons and binding is reverted, and Study-Bot is ready to take another question.

Notice how the flow of this script for the GUI version is quite similar to the CLI version. The main difference other than the heavier use of threads and the use of `infoDisplay` is the handling of the conversation. 

The source and custom instructions are only included in the first message, otherwise only the question and objects are sent to the `studyBot.sendMessage()` function, and this is checked using a simple boolean variable.

### Other Functions: `stopRecording()`, `close()`

This just calls the `studyBot.stopRecording()` function to change the boolean value that controls the recording loop, plays a beep and an audio message to the user to let them know that the recording has stopped, and disables the stop button and unbinds the stop key.

```python
def stopRecording():
	studyBot.stopRecording() # Access stopRecording() method from studyBot module
	winsound.Beep(700, 300) # Stop signal
	playAudioWithID(audioSelect['questionRecorded']) # Play audio confirmation
	# Disable stop button and unbind stop key
	stopButton.config(state = 'disabled')
	window.unbind('4')
```

This is called when the user clicks the 'Exit' button or presses the `ESC` key. It was added with the purpose of playing the closing signal to the user, since the `sys.exit()` could be called by these events instead.

### GUI

The GUI is created using basic elements from the `tkinter` module. Pay close attention to the `command` parameter of the button elements, this will be the function that is called when the button is pressed.

```python
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
```

### Setup Before Start

Fetch the audio history from **Elevenlabs** for the audio assistance, and get the options from the dropdown menu and add them to a list so that they can be cycled through with the `selectNextOption()` function.

Disable the `Stop Recording` and `Ask Question` buttons by default, and add the keyboard bindings for all the functions that are available by default.  

Play the boot-up signal and the `welcome` message with instructions to the user. This happens automatically when the program is opened.

```python
# Access from_api() method from History class through studyBot module
audioHistory = studyBot.History.from_api()

options = []

# For each option in the dropdown menu, add it to the options list
for i in range(topicDropdown['menu'].index('end') + 1): # Size of dropdown menu
	optionLabel = topicDropdown['menu'].entrycget(i, 'label')
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
studyBot.time.sleep(0.01) # Avoid overlapping sounds and popping
window.after(310, winsound.Beep, 630, 200)
studyBot.time.sleep(0.01)
window.after(610, winsound.Beep, 750, 200)

window.after(1000, playAudioWithID, audioSelect['welcome']) # Play welcome audio
window.mainloop()
```
