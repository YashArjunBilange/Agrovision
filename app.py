import streamlit as st
from PIL import Image
from ultralytics import YOLO
import torch
import remedies  # your remedies.py file
import numpy as np

# Page config
st.set_page_config(page_title="Plant Disease Detector", layout="centered")
st.title("🌿 Plant Disease Detection")
st.write("Upload a leaf image or take a photo to get disease prediction and remedies.")

# Load model
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# Image input
choice = st.radio("Select input method:", ["Upload Image", "Use Webcam"])
image = None
if choice == "Upload Image":
    uploaded_file = st.file_uploader("Upload a leaf image", type=["jpg","jpeg","png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
elif choice == "Use Webcam":
    webcam_image = st.camera_input("Take a picture of the leaf")
    if webcam_image:
        image = Image.open(webcam_image).convert("RGB")

# Prediction
if image:
    st.image(image, caption="Input Image", use_column_width=True)
    with st.spinner("Predicting..."):
        results = model.predict(image, verbose=False)

        # Convert results to numpy array (works for all YOLOv8 classification models)
        try:
            pred_array = results[0].numpy()
        except AttributeError:
            st.error("Cannot extract prediction. Ensure this is a YOLOv8 classification model.")
            pred_array = None

        if pred_array is not None:
            pred_array = pred_array.flatten()  # shape: [num_classes]
            top_idxs = np.argsort(pred_array)[::-1][:3]  # top-3 indices
            top_probs = np.exp(pred_array[top_idxs]) / np.sum(np.exp(pred_array))  # softmax
            top_classes = [results[0].names[int(i)] for i in top_idxs]

            # Top-1 prediction
            st.success(f"**Prediction:** {top_classes[0]} ({top_probs[0]*100:.2f}%)")

            # Remedies
            if hasattr(remedies, top_classes[0]):
                st.markdown(f"### Remedies for {top_classes[0]}:")
                st.write(getattr(remedies, top_classes[0]))
            else:
                st.write("Remedy not found for this disease.")

            # Top-3 predictions
            st.markdown("### Top 3 Predictions:")
            for cls, prob in zip(top_classes, top_probs):
                st.write(f"{cls}: {prob*100:.2f}%")

# ---------------------------
# Footer
# ---------------------------
st.write("---")
st.write("Model trained with YOLOv8. Classification only, no bounding boxes.")
