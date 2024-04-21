import serial

# Set up serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust port as needed

# Function to send text data to Arduino
def send_text_data(text_data):
    ser.write(b"d" + text_data.encode())  # Prefix text data with "T" marker

# Example: Send "Hello, Arduino!" as text data
text_data = "Hello, Arduino!"
send_text_data(text_data)
