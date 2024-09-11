import tkinter as tk
from tkinter import ttk, filedialog
import requests
import io
from PIL import Image, ImageTk
import tkinter.messagebox
import os
from dotenv import load_dotenv
import time
from requests.exceptions import RequestException

# Load environment variables
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

class TextToImageApp:
    def __init__(self, master):
        self.master = master
        master.title("AI Image Generator")
        master.geometry("600x700")
        master.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(input_frame, text="Enter prompt:", font=("Arial", 12)).pack(anchor="w")
        self.prompt_entry = ttk.Entry(input_frame, width=50, font=("Arial", 10))
        self.prompt_entry.pack(fill=tk.X, pady=(5, 10))

        # Aspect Ratio Frame
        aspect_frame = ttk.Frame(main_frame)
        aspect_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(aspect_frame, text="Select aspect ratio:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.aspect_ratio = ttk.Combobox(aspect_frame, values=["1:1", "16:9", "4:3", "3:2"], width=10, font=("Arial", 10))
        self.aspect_ratio.set("1:1")
        self.aspect_ratio.pack(side=tk.LEFT, padx=(10, 0))

        # Generate Button
        self.generate_button = ttk.Button(main_frame, text="Generate Image", command=self.generate_image, style="Accent.TButton")
        self.generate_button.pack(pady=(0, 20))

        # Image Display
        self.image_frame = ttk.Frame(main_frame, borderwidth=2, relief="groove")
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(padx=10, pady=10)

        # Save Button
        self.save_button = ttk.Button(main_frame, text="Save Image", command=self.save_image, state="disabled")
        self.save_button.pack(pady=(20, 0))

        # Configure styles
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("Accent.TButton", background="#4CAF50", foreground="white")
        self.style.map("Accent.TButton", background=[("active", "#45a049")])

    def generate_image(self):
        prompt = self.prompt_entry.get()
        aspect_ratio = self.aspect_ratio.get()

        # Set image dimensions based on aspect ratio
        if aspect_ratio == "1:1":
            width, height = 512, 512
        elif aspect_ratio == "16:9":
            width, height = 512, 288
        elif aspect_ratio == "4:3":
            width, height = 512, 384
        elif aspect_ratio == "3:2":
            width, height = 512, 341

        # Make API request
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        payload = {
            "inputs": prompt,
            "parameters": {"width": width, "height": height}
        }

        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 503:
                    if attempt < max_retries - 1:
                        tk.messagebox.showinfo("Server Busy", f"The server is busy. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        tk.messagebox.showerror("Server Error", "The server is currently unavailable. Please try again later.")
                        return

                if response.status_code == 404:
                    tk.messagebox.showerror("API Error", "404 Not Found: The API endpoint does not exist or is not accessible.")
                    return
                
                response.raise_for_status()  # Raise an exception for other bad status codes

                if response.headers.get('content-type') == 'application/json':
                    error_msg = response.json().get('error', 'Unknown error occurred')
                    tk.messagebox.showerror("API Error", f"Error from API: {error_msg}")
                    return

                image = Image.open(io.BytesIO(response.content))

                # Display the image
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo

                self.save_button["state"] = "normal"
                self.generated_image = image
                break  # Success, exit the retry loop

            except RequestException as e:
                if attempt < max_retries - 1:
                    tk.messagebox.showinfo("Connection Error", f"Error connecting to the server. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    tk.messagebox.showerror("Request Error", f"Error making request: {str(e)}")
            except PIL.UnidentifiedImageError:
                tk.messagebox.showerror("Image Error", "Received data is not a valid image")
                break  # Don't retry for image errors
            except Exception as e:
                tk.messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
                break  # Don't retry for unexpected errors

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.generated_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToImageApp(root)
    root.mainloop()
