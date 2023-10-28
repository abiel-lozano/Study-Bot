# This script is used to generate audio for accesibility features, 
# to access history generated audio and playing specific files.

from elevenlabs import set_api_key, generate, History, play
import credentials

set_api_key(credentials.elevenLabsKey)

text = 'TOPIC SELECTED. BEFORE PRESSING THE ASK BUTTON, BE READY TO PRESENT THE OBJECTS TO THE CAMERA AND TO ASK YOUR QUESTION RIGHT AFTER PRESSING THE BUTTON. BEFORE ASKING YOUR NEXT QUESTION, PLEASE WAIT FOR THE PREVIOUS RESPONSE TO BE READ OUT LOUD.'

# generate(text = text, model = 'eleven_multilingual_v1')

history = History.from_api()
print(history)

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
		play(item.audio)
		print('Playing history item with ID:', item.history_item_id)
	else:
		print('History item not found')

desired_history_item_id = 'JazmI95H1YV0IxkutnpP'
# playAudioWithID(history, desired_history_item_id)