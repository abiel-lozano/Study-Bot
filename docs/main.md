# Study Bot - main.py

## Contents

- [Description](#description)
- [Usage](#usage)
- [Code Walkthrough](#code-walkthrough)
  - [Imports](#imports)
  - [Source material selection: ```checkSelection()```](#source-material-selection-checkselection)
  - [Question processing: ```backgroundInit()``` and `startQuestionThreads()`](#question-processing-backgroundinit-and-startquestionthreads)
  - [GUI](#gui)

## Description

This script contains all of StudyBot's functionalities adapted to a GUI using Tkinter. Consider that this document is meant to be read after the [studyBot.md](../studyBot.md) document. To learn about the functionality behind the studyBot module, dependencies, and installation, please refer to the studyBot.md file.

## Usage

To run this version, run this command within the root directory of the project.

```bash
python src/main.py
```

## Code Walkthrough

### Imports

```python
import studyBot
import tkinter
import sys
```

- ```studyBot```: Import all of Study-Bot's functionalities.
- ```tkinter```: Used to create simple GUIs for Python scripts.
- ```sys```: Provides access system-specific parameters and functions, used to exit the program.

### Source material selection: ```checkSelection()```

At the time, topic selection, and by extension, source material selection, is not fully implemented. An information source could be selected using the dropdown, but the program would still look for the colors of the Human Body models. In the future, the program will switch between functions to switch between different sets of accepted color ranges or even different object identification methods.

```python
def checkSelection():
	global source
	topic = topicVar.get()
	infoDisplay.set(f'Selected topic: {topic}')
	
	if topic == 'Human Body':
		source = studyBot.humanBodySource
	elif topic == 'Biochem':
		source = studyBot.biochemSource
```

Note that ```infoDisplay``` is a variable that is used to display information to the user. It is updated using the ```set()``` method and is used as a replacement for printing to the console the current task being performed by the program.

### Question processing: ```backgroundInit()``` and ```startQuestionThreads()```

To allow the GUI to run while the program is processing the question, multithreading is necessary to perform any and all tasks that may take a while to complete, otherwise the GUI would freeze while the question is being processed.

This is achieved by calling this function that starts a new thread to run the functions that process the question and generate the answer. The ```startQuestionThreads()``` function creates threads for each of the required processes that call functions from the studyBot module.

>Note: Since the ```threading``` module is imported in studyBot, it is not necessary to import it again in this script and we can use it through the studyBot module.

```python
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
```

Notice how the flow of this script for the GUI version is quite similar to the CLI version. The main difference other than the heavier use of threads and the use of ```infoDisplay``` is the handling of the conversation. The initial query and source injection only occurs in the first message, otherwise we only send the question and objects to the ```studyBot.sendMessage()``` function, and we check this using a simple boolean variable.

### GUI

The rest is quite simple and the code is self-explanatory. The GUI is created using basic elements from the ```tkinter``` module. What we must pay close attention to is the ```command``` parameter of the button elements, this will be the function that is called when the button is pressed.

```python
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
```