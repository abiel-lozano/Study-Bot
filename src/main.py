import studyBot
import tkinter
import sys

# NOTE - There is chance this is not necessary
global answer
global messageHistory
global query
global firstQuestion
global source
answer = ''
studyBot.question = ''
studyBot.objects = ''
studyBot.topic = ''
source = ''
firstQuestion = True


# Find history item by history_item_id
def findAudioWithID(history, itemID):
	for item in history:
		if item.history_item_id == itemID:
			return item
	return None  # If the item is not found
		
# Play specific history item by history_item_id
def playAudioWithID(history, itemID):
	item = findAudioWithID(history, itemID)
	if item is not None:
		# studyBot.play(item.audio)
		threadAudio = studyBot.threading.Thread(target = studyBot.play, args = (item.audio,))
		threadAudio.start()
		# print('Playing history item with ID:', item.history_item_id)
	else:
		print('History item not found')

# Select the source material to be sent to GPT and select object ID function (not implemented yet)
def checkSelection():
	playAudioWithID(hist, 'JazmI95H1YV0IxkutnpP')

	global source
	topic = topicVar.get()
	infoDisplay.set(f'Selected topic: {topic}')
	
	if topic == 'Human Body':
		studyBot.topic = '1'
		source = studyBot.humanBodySource
	elif topic == 'Biochem':
		studyBot.topic = '2'
		source = studyBot.biochemSource

# NOTE: Not using this function, and calling startQuestionThreads directly from the button
# causes the UI to freeze while the threads are running.
def backgroundInit():
	threadStart = studyBot.threading.Thread(target = startQuestionThreads)
	threadStart.start()

	# Disable all the buttons
	askButton.config(state = 'disabled')
	exitButton.config(state = 'disabled')
	selectButton.config(state = 'disabled')

def startQuestionThreads():
	global firstQuestion
	global messageHistory
	# Start threads for object identification and question recording
	threadObjID = studyBot.threading.Thread(target = studyBot.lookForObjects, args = (studyBot.topic,))
	threadQuestionRec = studyBot.threading.Thread(target = studyBot.recordQuestion)
	threadObjID.start()
	threadQuestionRec.start()
	infoDisplay.set(f'Listening for question and looking for objects...')
	threadObjID.join()
	threadQuestionRec.join()

	playAudioWithID(hist, '7aNkMntxEq7M9IXZ6Vkv')

	# Display the recorded question and identified object
	infoDisplay.set(f'Question taken: {studyBot.question} \nObject identified: {studyBot.objects}')

	# Prepare messageHistory depending on whether this is the first question or not
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
	infoDisplay.set(f'Messaging GPT, please wait...')
	threadSendMessage = studyBot.threading.Thread(target = studyBot.sendMessage, args = (messageHistory,))
	threadSendMessage.start()
	threadSendMessage.join()

	# Get the answer of the last message of messageHistory
	answer = next((msg for msg in reversed(messageHistory) if msg['role'] == 'assistant'), None)['content']
	infoDisplay.set(f'Answer: {answer}')

	# Convert TTS
	threadConvertTTS = studyBot.threading.Thread(target = studyBot.convertTTS, args = (answer,))
	threadConvertTTS.start()
	threadConvertTTS.join()

	# Reenable all the buttons
	askButton.config(state = 'normal')
	exitButton.config(state = 'normal')
	selectButton.config(state = 'normal')

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

hist = studyBot.History.from_api()

window.after(0, playAudioWithID, hist, 'HNwmc11X0p23y77VLvOY')
window.mainloop()