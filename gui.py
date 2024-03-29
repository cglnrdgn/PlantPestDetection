import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import tensorflow as tf
from keras.preprocessing import image
import numpy as np
import os

class ImageClassificationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome to the Application!")

        self.left_frame = tk.LabelFrame(self.master, width=400, height=500, bg="gray", text="Image Selection", font=("Helvetica", 12))
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.load_button = tk.Button(self.left_frame, text="Load Image", command=self.load_image, font=("Helvetica", 10))
        self.load_button.pack(pady=10)

        self.selected_image_label = tk.Label(self.left_frame, text="Selected Image: ", font=("Helvetica", 10))
        self.selected_image_label.pack(pady=10)

        self.right_frame = tk.LabelFrame(self.master, width=400, height=500, bg="orange", text="Model and Optimization", font=("Helvetica", 12))
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.load_button = tk.Button(self.right_frame, text="Load Model", command=self.load_model, font=("Helvetica", 10))
        self.load_button.pack(pady=10)

        self.model_combobox = ttk.Combobox(self.right_frame, values=["MobileNet", "ResNet", "GoogLeNet", "VGG16", "MyCNN"], font=("Helvetica"))
        self.model_combobox.pack(pady=10)

        self.optimization_label = tk.Label(self.right_frame, text="Optimization Selection:", font=("Helvetica", 10))
        self.optimization_label.pack(pady=10)

        self.optimization_combobox = ttk.Combobox(self.right_frame, values=["Adam", "RMSprop", "SGD"], font=("Helvetica"))
        self.optimization_combobox.pack(pady=10)

        self.bottom_frame = tk.LabelFrame(self.master, width=400, height=200, bg="blue", text="Prediction Section", font=("Helvetica", 12))
        self.bottom_frame.grid(row=1, column=0, padx=10, pady=(0, 10), columnspan=2, sticky="nsew")

        self.predict_button = tk.Button(self.bottom_frame, text="Make Prediction", command=self.predict_image, font=("Helvetica", 10))
        self.predict_button.pack(pady=10)

        self.result_label = tk.Label(self.bottom_frame, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.loaded_model = None

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.display_selected_image(file_path)

    def load_model(self):
        selected_model = self.model_combobox.get()
        selected_optimization = self.optimization_combobox.get()

        model_file_name = f"{selected_model}_{selected_optimization}.h5"

        try:
            base_path = "C://Users//cagla//OneDrive//MODELLER//"
            model_path = os.path.join(base_path, model_file_name)
            self.loaded_model = tf.keras.models.load_model(model_path)
            print(f"Model for {selected_model} with {selected_optimization} optimization loaded successfully.")
        except Exception as e:
            print(f"Error loading the model: {e}")

    def display_selected_image(self, file_path):
        image = Image.open(file_path)
        image = image.resize((300, 150), resample=Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)

        #self.selected_image_label.config(text="Selected Image" + file_path)

        selected_image_label = tk.Label(self.left_frame, image=tk_image)
        selected_image_label.image = tk_image
        selected_image_label.pack()

    def predict_image(self):
        if self.loaded_model is None:
            print("Please load a model first.")
            return

        file_path = self.selected_image_label.cget("text")[14:]

        img = image.load_img(file_path, target_size=(299, 299))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        predictions = self.loaded_model.predict(img_array)

        predicted_class = np.argmax(predictions)

        class_probabilities = predictions[0]

        class_names = ["Ants", "Bees", "Beetles", "Caterpillars", "Earthworms", "Earwigs", "Grasshoppers", "Moths", "Slugs", "Snails", "Wasps", "Weevils"]  # Bu listeyi modelinizin sınıf isimleriyle doldurun

        result_text = f"Predicted class: {class_names[predicted_class]}\n"
        for i, probability in enumerate(class_probabilities):
            result_text += f"{class_names[i]}: Probability: {probability * 100:.2f}%\n"

        highest_probability_class = np.argmax(class_probabilities)
        result_text += f"The highest probability class is: {class_names[highest_probability_class]}"

        self.result_label.config(text=result_text)


if __name__ == '__main__':
    root = tk.Tk()
    app = ImageClassificationApp(root)
    root.mainloop()
