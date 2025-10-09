import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os
import re

class AlponaGenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Alpona Generator")

        # Frame for controls
        control_frame = ttk.Frame(root)
        control_frame.pack(pady=10)

        self.generate_button = ttk.Button(control_frame, text="Generate Alpona", command=self.generate_alpona)
        self.generate_button.grid(row=0, column=0, padx=5)

        self.log_text = tk.Text(root, height=10, state="disabled")
        self.log_text.pack(pady=10, fill="x")

        # Frame for image navigation
        nav_frame = ttk.Frame(root)
        nav_frame.pack(pady=10)

        self.prev_button = ttk.Button(nav_frame, text="<< Previous", command=self.show_previous_image)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = ttk.Button(nav_frame, text="Next >>", command=self.show_next_image)
        self.next_button.grid(row=0, column=1, padx=5)

        # Canvas for displaying images
        self.image_canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.image_canvas.pack(pady=10)

        # Label for displaying image count or filename
        self.image_info_label = ttk.Label(root, text="No image loaded", anchor="center")
        self.image_info_label.pack(pady=5)

        self.image_list = []
        self.current_image_index = 0

        # Input fields for parameters
        ttk.Label(control_frame, text="Output Directory:").grid(row=1, column=0, padx=5, sticky="e")
        self.output_dir_entry = ttk.Entry(control_frame)
        self.output_dir_entry.grid(row=1, column=1, padx=5)
        self.output_dir_entry.insert(0, "output")

        ttk.Label(control_frame, text="Width:").grid(row=2, column=0, padx=5, sticky="e")
        self.width_entry = ttk.Entry(control_frame)
        self.width_entry.grid(row=2, column=1, padx=5)
        self.width_entry.insert(0, "500")

        ttk.Label(control_frame, text="Height:").grid(row=3, column=0, padx=5, sticky="e")
        self.height_entry = ttk.Entry(control_frame)
        self.height_entry.grid(row=3, column=1, padx=5)
        self.height_entry.insert(0, "500")

        ttk.Label(control_frame, text="Image Count:").grid(row=4, column=0, padx=5, sticky="e")
        self.count_entry = ttk.Entry(control_frame)
        self.count_entry.grid(row=4, column=1, padx=5)
        self.count_entry.insert(0, "10")

        self.delete_button = ttk.Button(root, text="Delete Generated Images", command=self.delete_generated_images)
        self.delete_button.pack(pady=5)
        self.delete_button.pack_forget()  # Initially hide the button

    def log(self, message):
        self.log_text["state"] = "normal"
        self.log_text.insert("end", message + "\n")
        self.log_text["state"] = "disabled"
        self.log_text.see("end")

    def validate_inputs(self):
        output_dir = self.output_dir_entry.get().strip()
        width = self.width_entry.get().strip()
        height = self.height_entry.get().strip()
        count = self.count_entry.get().strip()

        if not output_dir:
            self.log("Output directory cannot be empty.")
            return None

        if not width.isdigit() or int(width) <= 0:
            self.log("Width must be a positive integer.")
            return None

        if not height.isdigit() or int(height) <= 0:
            self.log("Height must be a positive integer.")
            return None

        if not count.isdigit() or int(count) <= 0:
            self.log("Image count must be a positive integer.")
            return None

        return output_dir, int(width), int(height), int(count)

    def generate_alpona(self):
        inputs = self.validate_inputs()
        if not inputs:
            return

        output_dir, width, height, count = inputs
        self.log(f"Starting Alpona generation with output_dir={output_dir}, width={width}, height={height}, count={count}...")
        try:
            subprocess.run(["python", "main.py", "-out", output_dir, "-w", str(width), "-ht", str(height), "-c", str(count)], check=True)
            self.log("Alpona generation completed.")
            self.load_images(output_dir)
            self.delete_button.pack()  # Show the delete button after generation
        except subprocess.CalledProcessError as e:
            self.log(f"Error during generation: {e}")

    def delete_generated_images(self):
        output_dir = self.output_dir_entry.get().strip()
        if os.path.exists(output_dir):
            try:
                for file in os.listdir(output_dir):
                    file_path = os.path.join(output_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(output_dir)
                self.log(f"Deleted directory: {output_dir}")
                self.image_list = []
                self.image_canvas.delete("all")
                self.image_info_label.config(text="No image loaded")
                self.delete_button.pack_forget()  # Hide the delete button after deletion
            except Exception as e:
                self.log(f"Error deleting directory: {e}")
        else:
            self.log("Output directory does not exist.")

    def load_images(self, output_dir):
        self.image_list = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".png")]
        if self.image_list:
            self.current_image_index = 0
            self.show_image()
        else:
            self.log("No images found in the output directory.")

    def show_image(self):
        if self.image_list:
            image_path = self.image_list[self.current_image_index]
            self.log(f"Displaying image: {image_path}")
            image = Image.open(image_path)
            image.thumbnail((500, 500))
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_canvas.create_image(250, 250, image=self.tk_image)

            # Update image info label
            self.image_info_label.config(text=f"{self.current_image_index + 1}/{len(self.image_list)}: {os.path.basename(image_path)}")

    def show_previous_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
            self.show_image()

    def show_next_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlponaGenGUI(root)
    root.mainloop()