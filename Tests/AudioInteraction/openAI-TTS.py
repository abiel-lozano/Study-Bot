# Generate audio from text using OpenAI's speech endpoint
# Will not be used for now, spanish sounds terrible

from openai import OpenAI
import credentials
import warnings

# Ignore deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

client = OpenAI(api_key = credentials.openAIKey)

response = client.audio.speech.create(
  model="tts-1-hd",
  voice="echo",
  input="text"
)

response.stream_to_file("output.wav")