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
source = ''
firstQuestion = True

def checkSelection():
	global source
	topic = topicVar.get()
	infoDisplay.set(f'Selected topic: {topic}')
	
	if topic == 'Human Body':
		source = studyBot.humanBodySource
	elif topic == 'Biochem':
		source = studyBot.biochemSource

def backgroundInit():
	threadStart = studyBot.threading.Thread(target = startQuestionThreads)
	threadStart.start()
	# threadStart.join()

def startQuestionThreads():
	global firstQuestion
	global messageHistory
	threadObjID = studyBot.threading.Thread(target = studyBot.lookForObjects)
	threadQuestionRec = studyBot.threading.Thread(target = studyBot.recordQuestion)
	threadObjID.start()
	threadQuestionRec.start()
	infoDisplay.set(f'Listening for question and looking for objects...')
	threadObjID.join()
	threadQuestionRec.join()

	# Display the recorded question and identified object
	infoDisplay.set(f'Question taken: {studyBot.question} \nObject identified: {studyBot.objects}')

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

	infoDisplay.set(f'Messaging GPT, please wait...')
	threadSendMessage = studyBot.threading.Thread(target = studyBot.sendMessage, args = (messageHistory,))
	threadSendMessage.start()
	threadSendMessage.join()

	answer = next((msg for msg in reversed(messageHistory) if msg['role'] == 'assistant'), None)['content']
	infoDisplay.set(f'Answer: {answer}')

	threadConvertTTS = studyBot.threading.Thread(target = studyBot.convertTTS, args = (answer,))
	threadConvertTTS.start()
	threadConvertTTS.join()

# Create the main window
window = tkinter.Tk()
window.title('Study-Bot')
window.geometry('450x350')

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
# askButton = tkinter.Button(buttonsFrame, text = 'Ask another question', command = question, bg = '#8EC07C', font = ('Leelawadee', 12))
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