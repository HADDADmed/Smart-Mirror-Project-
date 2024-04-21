import serial
import speech_recognition as sr

# Set up serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust port as needed

# Initialize SpeechRecognition recognizer
recognizer = sr.Recognizer()

# Main loop
while True:
    # Read data from Arduino
    data = ser.read(1024)  # Adjust buffer size as needed
    if data:
        print("Received audio data:", len(data), "bytes")
        
        # Decode audio data (assuming it's in PCM format)
        audio_data = bytearray(data)
        
        # Recognize speech from audio data
        try:
            text = recognizer.recognize_google(audio_data)
            print("Recognized text:", text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))
