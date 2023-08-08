from gtts import gTTS
import pydub
from pydub import AudioSegment
import pyaudio

def convertTTS(text, lang):
    tts = gTTS(text = text, lang = lang)
    tts.save('output.mp3')
    audio = AudioSegment.from_file('output.mp3', format='mp3')
    
    # Convert stereo audio to mono
    if audio.channels == 2:
        audio = audio.set_channels(1)
    
    # Convert the sample width to 2 bytes (16-bit)
    audio = audio.set_sample_width(2)
    
    # Get the raw audio data
    rawData = audio.raw_data
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    # Open a stream and play the audio
    stream = p.open(format = p.get_format_from_width(audio.sample_width), channels = audio.channels, rate = audio.frame_rate, output = True)
    
    stream.write(rawData)
    
    # Close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

# convertTTS('The stomach is an organ located in the upper abdomen that plays a vital role in the digestion of food. Its main function is to store and break down food into smaller particles through the process of mechanical and chemical digestion.', 'en')
convertTTS('El estómago es un órgano ubicado en la parte superior del abdomen que juega un papel vital en la digestión de los alimentos. Su función principal es almacenar y descomponer los alimentos en partículas más pequeñas a través del proceso de digestión mecánica y química.', 'es')