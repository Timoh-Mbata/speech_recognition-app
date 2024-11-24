import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Function to detect faces and draw rectangles
def detect_faces(image, min_neighbors, scale_factor, rectangle_color):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load the pre-trained Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), rectangle_color, 2)

    return image

# Streamlit app layout
st.title('Face Detection App')

# Instructions for the user
st.write("""
    **Instructions:**
    1. Upload an image with faces.
    2. Adjust the sliders to modify the face detection parameters (`minNeighbors` and `scaleFactor`).
    3. Choose the color of the rectangles to highlight the detected faces.
    4. Press "Detect Faces" to process the image and view the result.
    5. Optionally, you can save the processed image by clicking the "Save Image" button.
""")

# File uploader to upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Parameters for face detection
min_neighbors = st.slider('minNeighbors', min_value=1, max_value=10, value=3, step=1)
scale_factor = st.slider('scaleFactor', min_value=1.01, max_value=2.0, value=1.1, step=0.01)
rectangle_color = st.color_picker("Pick a color for the rectangles", "#FF0000")

# Process and display the image with detected faces
if uploaded_file is not None:
    # Open the image using PIL and convert to numpy array
    image = Image.open(uploaded_file)
    image = np.array(image)

    # Detect faces and draw rectangles
    processed_image = detect_faces(image, min_neighbors, scale_factor, rectangle_color)

    # Convert the processed image back to PIL format for displaying
    processed_image_pil = Image.fromarray(processed_image)
    st.image(processed_image_pil, caption='Processed Image', use_column_width=True)

    # Button to save the image
    if st.button('Save Image'):
        # Save the image using OpenCV
        save_path = 'detected_faces.png'
        cv2.imwrite(save_path, processed_image)
        st.success(f"Image saved as {save_path}")
        st.markdown(f'<a href="data:file/{save_path}" download>Click here to download the image</a>', unsafe_allow_html=True)
