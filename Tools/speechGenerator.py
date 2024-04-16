# This script is used to generate audio for accesibility features, to
# accessing the history of generated audio, and playing specific files.

# from elevenlabs import set_api_key, generate, History, play
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import credentials

client = ElevenLabs(api_key=credentials.elevenLabsKey)

# 1 - Generate audio from text
text = ''
client.generate(text = text, model = 'eleven_multilingual_v2')

# 2 - Check history to get history_item_id
history = client.history.get_all().history
print('History item:', history[0].history_item_id)
# print(history) # Messy raw output, uncomment only when needed

# 3 - Play specific history item by history_item_id to check your work
play(client.history.get_audio(history[0].history_item_id), notebook=False, use_ffmpeg=False)
play(client.history.get_audio(''), notebook=False, use_ffmpeg=False)