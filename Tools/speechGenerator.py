# This script is used to generate audio for accesibility features, 
# to access history generated audio and playing specific files.

from elevenlabs import set_api_key, generate, History, play
import credentials

set_api_key(credentials.elevenLabsKey)

# 1 - Generate audio from text
text = 'BIOCHEMISTRY SELECTED. BEFORE PRESSING THE ASK BUTTON, BE READY TO PRESENT THE OBJECTS TO THE CAMERA AND TO ASK YOUR QUESTION RIGHT AFTER PRESSING THE BUTTON. BEFORE ASKING YOUR NEXT QUESTION, PLEASE WAIT FOR THE PREVIOUS RESPONSE TO BE READ OUT LOUD.'
generate(text = text, model = 'eleven_multilingual_v1')

# 2 - Check history to get history_item_id
history = History.from_api()
# print('First history item:', history[0].history_item_id)
# print(history) # Messy output, uncomment only when needed

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
		print('Playing history item with ID:', item.history_item_id)
		play(item.audio)
	else:
		print('History item not found')

# 3 - Play specific history item by history_item_id to check your work
select = history[0].history_item_id
playAudioWithID(history, select)