import cv2
import time
import smbus2
import bme280

# Initialize the BME280 sensor for temperature measurement
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect if the person is too far from the camera
def check_distance(frame):
    # Dummy function to simulate checking distance, you can replace it with actual distance checking logic
    # Here, we're just checking if a face is detected or not
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        return False
    return True

# Function to measure temperature using BME280 sensor
def measure_temperature():
    data = bme280.sample(bus, address, calibration_params)
    temperature = data.temperature
    return temperature

# Function to perform temperature measurement when person is close enough
def perform_temperature_measurement():
    # Open the camera (assuming it's already open)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        return None
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read frame from camera")
            break
        
        # Check if the person is close enough
        if not check_distance(frame):
            print("Please come closer")  #tts
            time.sleep(2)  # Wait for a few seconds before checking again
            continue
        
        # Person is close enough, measure temperature
        temperature = measure_temperature()
        return temperature
    
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
