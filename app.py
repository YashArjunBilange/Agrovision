# app.py
import streamlit as st
from PIL import Image
import torch
import remedies  # your remedies.py file

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Plant Disease Detector",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🌿 Plant Disease Detection")
st.write("Upload a leaf image or take a photo with your webcam to get disease prediction along with remedies.")

# ---------------------------
# Load Model
# ---------------------------
@st.cache_resource
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
    model.eval()
    return model

model = load_model()

# ---------------------------
# Image Input
# ---------------------------
choice = st.radio("Select input method:", ["Upload Image", "Use Webcam"])

image = None
if choice == "Upload Image":
    uploaded_file = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
elif choice == "Use Webcam":
    webcam_image = st.camera_input("Take a picture of the leaf")
    if webcam_image:
        image = Image.open(webcam_image).convert("RGB")

# ---------------------------
# Display Image & Predict
# ---------------------------
if image:
    st.image(image, caption="Input Image", use_column_width=True)

    with st.spinner("Predicting..."):
        results = model([image])
        class_id = int(results.pred[0][0, -1])
        prediction = results.names[class_id]
        st.success(f"**Prediction:** {prediction}")

        # Remedies
        if hasattr(remedies, prediction):
            remedy_text = getattr(remedies, prediction)
            st.markdown(f"### Remedies for {prediction}:")
            st.write(remedy_text)
        else:
            st.write("Remedy not found for this disease.")

# ---------------------------
# Footer
# ---------------------------
st.write("---")
st.write("Model trained with YOLOv5. Classification only, no bounding boxes.")