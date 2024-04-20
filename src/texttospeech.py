from gtts import gTTS
import os

def text_to_speech(text, language='en'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language)

    # Save the audio file
    tts.save("output.mp3")

    # Play the audio file
    os.system("start output.mp3")

# Example usage
text = "Hello, how are you today?"
text_to_speech(text)
