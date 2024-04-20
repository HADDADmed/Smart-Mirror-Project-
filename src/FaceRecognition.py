import cv2

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to recognize faces
def recognize_faces():
    # Open the camera (assuming it's already open from Arduino)
    cap = cv2.VideoCapture(0)
    
    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Loop to continuously read frames from the camera
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read frame from camera")
            break
        
        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Here you can add the logic to recognize the person's name
            # For simplicity, let's just display "Hello"
            cv2.putText(frame, "Hello", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        
        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)
        
        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()