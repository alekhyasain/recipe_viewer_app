import logging

# import Image from pillow to open images
import streamlit as st
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    st.set_page_config(layout="wide")
    st.title("Recipes for different meals")
    st.write("Get different ingredients and links for recipes under meals and sub categories.")
    img = Image.open("recipe.jpg")

    # Display image using streamlit
    # Width is used to set the width of an image
    st.image(img, width=600)
except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
    st.error("Error: Required file not found.")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    st.error("An unexpected error occurred.")