# This script is used to generate audio for accesibility features, to
# accessing the history of generated audio, and playing specific files.

# from elevenlabs import set_api_key, generate, History, play
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import credentials

client = ElevenLabs(api_key=credentials.elevenLabsKey)

# 1 - Generate audio from text
text = input('Text: ')
audio = client.generate(
	text = text, 
	model = 'eleven_multilingual_v1', 
	voice_settings = {
		'stability': 0.5, 
		'similarity_boost': 0
		}
	)
play(audio, notebook=False, use_ffmpeg=False)


# 2 - Get history_item_id of the last generated audio
history = client.history.get_all().history
print('\n\nHistory item:', history[0].history_item_id + '\n\n')
# print(history) # Messy raw output, uncomment only when needed

# 3 - Play specific history item by history_item_id to check your work
# play(client.history.get_audio(history[0].history_item_id), notebook=False, use_ffmpeg=False)