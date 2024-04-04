from openai import OpenAI
client = OpenAI()

audioFile = 'response.wav'

response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Today is a wonderful day to build something people love!"
)

response.stream_to_file(audioFile)
# response.stream_to_file("output.wav")
# response.with_streaming_response.method()

# Play MP3 file

import pygame

pygame.mixer.init()
pygame.mixer.music.load(audioFile)
pygame.mixer.music.play()
pygame.time.wait(5000) # Play for 5 seconds
pygame.mixer.music.stop() # Stop playing