# import Image from pillow to open images
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")
st.title("Recipes for different meals")
st.write("Get different ingredients and links for recipes under meals and sub categories.")
img = Image.open("recipe.jpg")
 
# display image using streamlit
# width is used to set the width of an image
st.image(img, width=200)