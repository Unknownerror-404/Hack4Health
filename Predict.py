import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
from PIL import Image, ImageTk
from imutils import face_utils
import dlib
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model

class_labels = {
    0: "Normal",
    1: "Esotropia",
    2: "Exotropia",
    3: "Hypertropia",
    4: "Hypotropia",
}

model = load_model("eye_classifier_model.keras")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def extract_eye_region(img_path):
    if not os.path.exists(img_path):
        return None

    image = cv2.imread(img_path)
    if image is None:
        return None
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

    print("gray dtype:", gray.dtype, "shape:", gray.shape)
    print("image_rgb dtype:", image_rgb.dtype, "shape:", image_rgb.shape)

    if gray.dtype != np.uint8 or image_rgb.dtype != np.uint8:
        return None

    try:
        faces = detector(gray)
    except Exception as e:
        print("dlib error:", e)
        return None

    if len(faces) == 0:
        return None

    shape = predictor(gray, faces[0])
    shape_np = face_utils.shape_to_np(shape)

    left_eye = shape_np[36:42]
    right_eye = shape_np[42:48]

    x_min = max(0, min(np.min(left_eye[:, 0]), np.min(right_eye[:, 0])))
    y_min = max(0, min(np.min(left_eye[:, 1]), np.min(right_eye[:, 1])))
    x_max = min(image.shape[1], max(np.max(left_eye[:, 0]), np.max(right_eye[:, 0])))
    y_max = min(image.shape[0], max(np.max(left_eye[:, 1]), np.max(right_eye[:, 1])))

    if x_max <= x_min or y_max <= y_min:
        return None

    eye_crop = image[y_min:y_max, x_min:x_max]
    if eye_crop.size == 0:
        return None

    resized = cv2.resize(eye_crop, (300, 75))
    return resized


def predict_eye_class(img_path):
    try:
        eye_img = extract_eye_region(img_path)
        if eye_img is None:
            return "Eye region not found"

        eye_img = eye_img.astype(np.float32) / 255.0
        eye_img = np.expand_dims(eye_img, axis=0)

        pred = model.predict(eye_img)
        class_idx = int(np.argmax(pred))
        return class_labels.get(class_idx, f"Unknown class {class_idx}")
    except Exception as e:
        print("Prediction error:", e)
        return "Prediction failed"


def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        result = predict_eye_class(file_path)

        if result == "Eye region not found":
            messagebox.showerror("Error", "Could not detect eyes. Try another image.")
            return
        elif result == "Prediction failed":
            messagebox.showerror("Error", "Prediction failed. Check the console.")
            return

        result_label.config(text=f"Prediction: {result}")

        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

root = tk.Tk()
root.title("Eye Condition Predictor")

Button(root, text="Select Image", command=open_file).pack(pady=10)
image_label = Label(root)
image_label.pack()
result_label = Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()