import streamlit as st
from PIL import Image
import subprocess
import os
import io

def generate_alpona(width, height):
    """Generate an Alpona image with the given width and height."""
    output_dir = "temp_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        subprocess.run([
            "python", "main.py", "-w", str(width), "-ht", str(height), "-out", output_dir, "-c", "1"
        ], check=True)

        # Load the generated image
        image_path = os.path.join(output_dir, "image_0.png")
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return img_file.read()
        else:
            st.error("Failed to generate the image.")
            return None
    except subprocess.CalledProcessError as e:
        st.error(f"Error during generation: {e}")
        return None
    finally:
        # Clean up the temporary output directory
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(output_dir)

# Streamlit UI
st.set_page_config(page_title="Alpona Generator", layout="centered")

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["Generate Alpona", "About"])

if menu == "Generate Alpona":
    st.title("Alpona Generator")
    st.write("Generate beautiful Alpona designs by specifying the dimensions.")

    # Input fields for width and height
    width = st.number_input("Width", min_value=100, max_value=2000, value=500, step=50)
    height = st.number_input("Height", min_value=100, max_value=2000, value=500, step=50)

    if st.button("Generate"):
        st.write("Generating Alpona...")
        image_data = generate_alpona(width, height)
        if image_data:
            st.image(Image.open(io.BytesIO(image_data)), caption="Generated Alpona", width=width)

elif menu == "About":
    st.title("About Alpona Generator")
    st.markdown(
        """
        # AlponaGen 🎨

        **Version:** 1.0  
        **Author:** Aritro Shome  
        **Date:** October 9, 2025  

        ## Overview
        AlponaGen is a fractal-based generative art engine designed to create intricate alpona/mandala-style images. The project uses mathematical patterns and modular design principles to produce stunning visuals. The main motive was to create a dataset of images of Alpona-s to potentially train models on them.

        ## Features ✨
        - **Modular Design:** Separate files for generation engine and pattern drawing functions.
        - **Customizable Output:** Specify width, height, and output directory via command-line arguments.
        - **Multiple Styles:** Includes built-in styles like `alpona` and supports custom styles.
        - **Layered Patterns:** Generate layers with triangles, circles, petals, spirals, and dots.
        - **Randomized Art:** Each image is unique, thanks to randomization.

        ## GitHub Repository
        [View the project on GitHub](https://github.com/sortira/alpona-gen)
        """
    )