from io import BytesIO
import streamlit as st
import numpy as np
from PIL import Image, ImageColor
import cv2

# Set page configs. Get emoji names from WebFx
st.set_page_config(page_title="Real-time Face Detection", page_icon="./assets/faceman_cropped.png", layout="centered")

# -------------Header Section------------------------------------------------

title = '<p style="text-align: center;font-size: 40px;font-weight: 550; "> Realtime Frontal Face Detection</p>'
st.markdown(title, unsafe_allow_html=True)

st.markdown(
    "Frontal-face detection using *Haar-Cascade Algorithm* which is one of the oldest face detection algorithms "
    "invented. It is based on the sliding window approach,giving a real-time experience with 30-40 FPS on any average CPU.")

# -------------Sidebar Section------------------------------------------------

detection_mode = None
# Haar-Cascade Parameters
minimum_neighbors = 4
# Minimum possible object size
min_object_size = (20, 20)
# bounding box thickness
bbox_thickness = 3
# bounding box color
bbox_color = (0, 255, 0)

with st.sidebar:
    st.image("./assets/faceman_cropped.png", width=260)

    title = '<p style="font-size: 25px;font-weight: 550;">Face Detection Settings</p>'
    st.markdown(title, unsafe_allow_html=True)

    # choose the mode for detection
    mode = st.radio("Choose Face Detection Mode", ('Image Upload',
                                                   'Webcam Image Capture',
                                                   'Webcam Realtime'), index=0)
    if mode == 'Image Upload':
        detection_mode = mode
    elif mode == 'Video Upload':
        detection_mode = mode
    elif mode == "Webcam Image Capture":
        detection_mode = mode
    elif mode == 'Webcam Realtime':
        detection_mode = mode

    # slider for choosing parameter values
    minimum_neighbors = st.slider("Mininum Neighbors", min_value=0, max_value=10,
                                  help="Parameter specifying how many neighbors each candidate "
                                       "rectangle should have to retain it. This parameter will affect "
                                       "the quality of the detected faces. Higher value results in less "
                                       "detections but with higher quality.",
                                  value=minimum_neighbors)

    # slider for choosing parameter values

    min_size = st.slider(f"Mininum Object Size, Eg-{min_object_size} ", min_value=3, max_value=500,
                         help="Minimum possible object size. Objects smaller than that are ignored.",
                         value=20)

    min_object_size = (min_size, min_size)

    # Get bbox color and convert from hex to rgb
    bbox_color = ImageColor.getcolor(str(st.color_picker(label="Bounding Box Color", value="#00FF00")), "RGB")

    # ste bbox thickness
    bbox_thickness = st.slider("Bounding Box Thickness", min_value=1, max_value=30,
                               help="Sets the thickness of bounding boxes",
                               value=bbox_thickness)

    st.info("NOTE : The quality of detection will depend on above paramters."
            " Try adjusting them as needed to get the most optimal output")

    # line break
    st.markdown(" ")

    # About the programmer
    st.markdown("## Made by **Deepesh Mhatre** \U0001F609")
    st.markdown("Contribute to this project at "
                "[*github.com/deepeshdm*](https://github.com/deepeshdm/Realtime_Face_Detection)")

# -------------Image Upload Section------------------------------------------------


if detection_mode == "Image Upload":

    # line break
    st.markdown(" ")

    # Example Images
    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/example_2.png")
    with col2:
        st.image(image="./assets/example_3.png")

    # line break
    st.markdown(" ")
    uploaded_file = st.file_uploader("Upload Image (Only PNG & JPG images allowed)", type=['png', 'jpg'])

    if uploaded_file is not None:

        with st.spinner("Detecting faces..."):
            img = Image.open(uploaded_file)

            # To convert PIL Image to numpy array:
            img = np.array(img)

            # Load the cascade
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            # Convert into grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, minNeighbors=minimum_neighbors, minSize=min_object_size)

            if len(faces) == 0:
                st.warning(
                    "No Face Detected in Image. Make sure your face is visible in the camera with proper lighting."
                    " Also try adjusting detection parameters")
            else:
                # Draw rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), color=bbox_color, thickness=bbox_thickness)

                # Display the output
                st.image(img)

                if len(faces) > 1:
                    st.success("Total of " + str(len(faces)) + " faces detected inside the image.")

                    # convert to pillow image
                    img = Image.fromarray(img)
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")

                    # Creating columns to center button
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        pass
                    with col3:
                        pass
                    with col2:
                        st.download_button(
                            label="Download image",
                            data=buffered.getvalue(),
                            file_name="output.png",
                            mime="image/png")
                else:
                    st.success("Only 1 face detected inside the image.")

                    # convert to pillow image
                    img = Image.fromarray(img)
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")

                    # Creating columns to center button
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        pass
                    with col3:
                        pass
                    with col2:
                        st.download_button(
                            label="Download image",
                            data=buffered.getvalue(),
                            file_name="output.png",
                            mime="image/png")

# -------------Webcam Image Capture Section------------------------------------------------

if detection_mode == "Webcam Image Capture":

    st.info("NOTE : In order to use this mode, you need to give webcam access.")

    img_file_buffer = st.camera_input("Capture an Image from Webcam", disabled=False, key=1,
                                      help="Make sure you have given webcam permission to the site")

    if img_file_buffer is not None:

        with st.spinner("Detecting faces ..."):
            # To read image file buffer as a PIL Image:
            img = Image.open(img_file_buffer)

            # To convert PIL Image to numpy array:
            img = np.array(img)

            # Load the cascade
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            # Convert into grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, minNeighbors=minimum_neighbors,
                                                  minSize=min_object_size)

            if len(faces) == 0:
                st.warning(
                    "No Face Detected in Image. Make sure your face is visible in the camera with proper lighting. "
                    "Also try adjusting detection parameters")
            else:
                # Draw rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), color=bbox_color, thickness=bbox_thickness)

                # Display the output
                st.image(img)

                if len(faces) > 1:
                    st.success("Total of " + str(len(faces)) + " faces detected inside the image.")
                else:
                    st.success("Only 1 face detected inside the image.")

                # Download the image
                img = Image.fromarray(img)
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                # Creating columns to center button
                col1, col2, col3 = st.columns(3)
                with col1:
                    pass
                with col3:
                    pass
                with col2:
                    st.download_button(
                        label="Download image",
                        data=buffered.getvalue(),
                        file_name="output.png",
                        mime="image/png")

# -------------Webcam Realtime Section------------------------------------------------


if detection_mode == "Webcam Realtime":

    st.info("NOTE : In order to use this mode, you need to give webcam access. "
            "It takes few seconds for webcam to start or close.")

    st.warning("NOTE : To stop the webcam detection,press any key on your keyboard.")

    spinner_message = "Wait a sec, getting some things done..."

    with st.spinner(spinner_message):
        # To capture video from webcam.
        cap = cv2.VideoCapture(0)


        def start_webcam_detection():

            # Load the cascade
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            while True:
                # Read the frame
                _, img = cap.read()
                # Convert to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Detect the faces
                faces = face_cascade.detectMultiScale(gray, 1.1, minNeighbors=minimum_neighbors,
                                                      minSize=min_object_size)
                # Draw the rectangle around each face
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), color=bbox_color, thickness=bbox_thickness)
                    # Putting text on bbox
                    cv2.putText(img, 'Human Face', (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.4, bbox_color, thickness=1)

                # Display
                cv2.imshow('Press ANY key on keyboard to close window', img)

                # Stop if any key is pressed
                k = cv2.waitKey(30)
                if k != -1:
                    break
            # Release the VideoCapture object
            cv2.destroyAllWindows()
            cap.release()

    # Creating columns to center button
    col1, col2, col3 = st.columns(3)
    with col1:
        pass
    with col3:
        pass
    with col2:
        st.button("START WEBCAM", on_click=start_webcam_detection)

# -------------Hide Streamlit Watermark------------------------------------------------
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)