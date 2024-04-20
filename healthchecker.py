import cv2
import dlib
import numpy as np

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load pre-trained facial landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Function to analyze mouth appearance for signs of fatigue or dehydration
def mouth_analysis(shape):
    # Extract mouth region from facial landmarks
    mouth_pts = shape.parts()[48:68]
    mouth_region = np.array([(pt.x, pt.y) for pt in mouth_pts], dtype=np.int32)
    # Calculate mouth aspect ratio
    mouth_aspect_ratio = mouth_aspect_ratio(mouth_pts)
    print("Mouth aspect ratio:", mouth_aspect_ratio)
    # Analyze mouth aspect ratio for signs of fatigue or dehydration
    if mouth_aspect_ratio < 0.3:
        print("The person's mouth may appear dry or chapped.")

# Function to calculate mouth aspect ratio
def mouth_aspect_ratio(mouth_pts):
    # Compute euclidean distances between vertical mouth landmarks
    a = np.linalg.norm(mouth_pts[2] - mouth_pts[10])
    b = np.linalg.norm(mouth_pts[3] - mouth_pts[9])
    c = np.linalg.norm(mouth_pts[4] - mouth_pts[8])
    # Compute euclidean distance between horizontal mouth landmarks
    d = np.linalg.norm(mouth_pts[0] - mouth_pts[6])
    # Compute mouth aspect ratio
    mar = (a + b + c) / (3 * d)
    return mar

# Function to analyze forehead temperature using infrared or thermal imaging
def forehead_temperature_analysis(image):
    # Implement forehead temperature analysis using appropriate hardware and techniques
    pass

# Function to analyze pupil size and responsiveness
def pupil_analysis(image):
    # Implement pupil analysis using appropriate image processing techniques
    pass

# Function to analyze facial expressions for signs of pain, discomfort, or fatigue
def facial_expression_analysis(image):
    # Implement facial expression analysis using machine learning-based methods
    pass

# Function to analyze skin texture for signs of inflammation, irritation, or dryness
def skin_texture_analysis(image):
    # Implement skin texture analysis using image processing techniques
    pass

# Function to analyze breathing rate based on chest movements or facial cues
def breathing_rate_analysis(image):
    # Implement breathing rate analysis using appropriate methods
    pass

def health_checker(image_path):
    # Load image
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces using OpenCV face detection
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If no faces are detected, return None
    if len(faces) == 0:
        print("No faces detected in the image.")
        return None

    # Extract facial features for each detected face
    for (x, y, w, h) in faces:
        # Crop face region from the image
        face_region = gray_image[y:y+h, x:x+w]

        # Resize face region to a fixed size
        resized_face = cv2.resize(face_region, (100, 100))

        # Normalize pixel values to range [0, 1]
        normalized_face = resized_face / 255.0

        # Detect facial landmarks using dlib
        shape = predictor(gray_image, dlib.rectangle(x, y, x+w, y+h))
        points = np.array([[p.x, p.y] for p in shape.parts()])

        # Measure facial symmetry
        symmetry_score = measure_symmetry([points[:17], points[17:]])
        print("Facial symmetry score:", symmetry_score)

        # Analyze skin color for signs of paleness or redness
        mean_lightness = skin_color_analysis(normalized_face)

        # Analyze eye appearance for signs of tiredness
        left_eye_aspect_ratio, right_eye_aspect_ratio = eye_analysis(shape, gray_image)

        # Assess overall health based on collected data
        health_status = assess_health(symmetry_score, mean_lightness, left_eye_aspect_ratio, right_eye_aspect_ratio)
        print("Health Status:", health_status)

    print(f"Found {len(faces)} faces in the image.")

# Function to assess overall health based on facial analysis
def assess_health(facial_symmetry_score, mean_lightness, left_eye_aspect_ratio, right_eye_aspect_ratio):
    # Define threshold values
    threshold_symmetry = 70.0
    min_lightness_threshold = 100
    max_lightness_threshold = 150
    min_eye_aspect_ratio = 0.2

    # Check if all parameters meet criteria for good health
    if (facial_symmetry_score > threshold_symmetry and
        mean_lightness > min_lightness_threshold and mean_lightness < max_lightness_threshold and
        left_eye_aspect_ratio > min_eye_aspect_ratio and right_eye_aspect_ratio > min_eye_aspect_ratio):
        return "Good Health"
    else:
        return "Potential Health Concern"
# Function to measure facial symmetry
def measure_symmetry(landmarks):
    if len(landmarks) < 2:
        return None
    left_landmarks = landmarks[0]
    right_landmarks = landmarks[1]
    left_side = np.mean(left_landmarks, axis=0)
    right_side = np.mean(right_landmarks, axis=0)
    symmetry_score = np.linalg.norm(left_side - right_side)
    return symmetry_score

# Function to analyze skin color for signs of paleness or redness
def skin_color_analysis(face):
    # Convert face to 8-bit unsigned integer format
    face_uint8 = (face * 255).astype(np.uint8)
    
    # Convert face to BGR color space
    bgr_face = cv2.cvtColor(face_uint8, cv2.COLOR_GRAY2BGR)
    
    # Convert BGR to LAB color space
    lab_face = cv2.cvtColor(bgr_face, cv2.COLOR_BGR2LAB)
    
    # Extract L (lightness) channel
    l_channel = lab_face[:,:,0]
    
    # Compute mean lightness
    mean_lightness = np.mean(l_channel)
    print("Mean lightness:", mean_lightness)
    
    # Analyze lightness for signs of paleness or redness
    if mean_lightness < 100:
        print("The person may appear pale.")
    elif mean_lightness > 150:
        print("The person may appear red.")

    return mean_lightness




# Function to analyze eye appearance for signs of tiredness
def eye_analysis(shape, image):
    # Extract eye regions from facial landmarks
    left_eye_pts = shape.parts()[36:42]
    right_eye_pts = shape.parts()[42:48]
    
    # Check if both left and right eye points are detected
    if len(left_eye_pts) != 6 or len(right_eye_pts) != 6:
        print("Could not detect both eyes.")
        return 0.5, 0.5  # Default aspect ratios
    
    left_eye_region = np.array([(pt.x, pt.y) for pt in left_eye_pts], dtype=np.int32)
    right_eye_region = np.array([(pt.x, pt.y) for pt in right_eye_pts], dtype=np.int32)
    # Draw eye regions for visualization (optional)
    cv2.polylines(image, [left_eye_region], True, (0, 255, 0), 1)
    cv2.polylines(image, [right_eye_region], True, (0, 255, 0), 1)
    # Calculate eye aspect ratios for each eye
    left_eye_aspect_ratio = eye_aspect_ratio(left_eye_pts)
    right_eye_aspect_ratio = eye_aspect_ratio(right_eye_pts)
    print("Left eye aspect ratio:", left_eye_aspect_ratio)
    print("Right eye aspect ratio:", right_eye_aspect_ratio)
    # Analyze eye aspect ratios for signs of tiredness
    if left_eye_aspect_ratio < 0.2 and right_eye_aspect_ratio < 0.2:
        print("The person may appear tired.")
    
    return left_eye_aspect_ratio, right_eye_aspect_ratio

# Function to calculate eye aspect ratio
def eye_aspect_ratio(eye_pts):
    # Convert Dlib points to NumPy arrays
    eye_pts = np.array([(pt.x, pt.y) for pt in eye_pts])
    # Compute euclidean distances between vertical eye landmarks
    a = np.linalg.norm(eye_pts[1] - eye_pts[5])
    b = np.linalg.norm(eye_pts[2] - eye_pts[4])
    # Compute euclidean distance between horizontal eye landmarks
    c = np.linalg.norm(eye_pts[0] - eye_pts[3])
    # Compute eye aspect ratio
    ear = (a + b) / (2 * c)
    return ear


# Example usage
image_path = "image.jpg"
health_checker(image_path)
