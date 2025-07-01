#pip install imutils tensorflow keras pillow opencv-python tkinterdnd2
#pip install dlib-19.24.1-cp310-cp310-win_amd64.whl #Must be installed manually and must be run from the same directory where the .whl file is located

import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
from PIL import Image, ImageTk
from imutils import face_utils
import dlib
import numpy as np
import cv2
import os
import tempfile
from tensorflow.keras.models import load_model

from Beads import launch_brock_string_app
from Trace import launch_eye_tracking_app

class_labels = {
    0: "Esotropia",
    1: "Exotropia",
    2: "Hypertropia",
    3: "Hypotropia",
    4: "Normal",
}

model = load_model("./cnn_eye_model.keras")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

is_dark_mode = False

themes = {
    "light": {
        "bg": "#f2f6f9", "fg": "#333", "button_bg": "#cfe2f3",
        "button_fg": "black", "instruction": "#888", "result_fg": "#2a3f5f"
    },
    "dark": {
        "bg": "#121212", "fg": "#eeeeee", "button_bg": "#333333",
        "button_fg": "white", "instruction": "#aaaaaa", "result_fg": "#33c4ff"
    }
}

def get_current_theme():
    return themes["dark"] if is_dark_mode else themes["light"]

def apply_theme():
    theme = get_current_theme()
    root.configure(bg=theme["bg"])
    title_label.configure(bg=theme["bg"], fg=theme["fg"])
    select_button.configure(bg=theme["button_bg"], fg=theme["button_fg"])
    camera_button.configure(bg=theme["button_bg"], fg=theme["button_fg"])
    toggle_theme_button.configure(bg=theme["button_bg"], fg=theme["button_fg"])
    result_label.configure(bg=theme["bg"], fg=theme["result_fg"])
    disclaimer_label.configure(bg=theme["bg"], fg="red")
    info_label.configure(bg=theme["bg"], fg=theme["instruction"])
    image_label.configure(bg=theme["bg"])

def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()

def extract_eye_region(img_path):
    if not os.path.exists(img_path):
        return None
    image = cv2.imread(img_path)
    if image is None:
        return None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
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

    return cv2.resize(eye_crop, (224, 224))

def predict_eye_class(img_path):
    try:
        eye_img = extract_eye_region(img_path)
        if eye_img is None:
            return "Eye region not found"
        eye_img = eye_img.astype(np.float32) / 255.0
        eye_img = np.expand_dims(eye_img, axis=0)
        pred = model.predict(eye_img)[0]
        return class_labels.get(np.argmax(pred), "Unknown class")
    except Exception as e:
        print("Prediction error:", e)
        return "Prediction failed"

def handle_prediction_and_ui(file_path):
    result = predict_eye_class(file_path)
    if result in ["Eye region not found", "Prediction failed"]:
        messagebox.showerror("Error", result)
        return

    result_label.config(text=f"Prediction: {result}")
    disclaimer_label.config(
        text="⚠️ This is a trained AI model and can produce varying predictions.\nPlease consult an ophthalmologist.",
        fg="red"
    )

    img = Image.open(file_path)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

    show_loading_and_launch(result)

def show_loading_and_launch(result):
    theme = get_current_theme()
    
    loading = tk.Toplevel(root)
    loading.title("Please Wait")
    loading.geometry("300x100")
    loading.configure(bg=theme["bg"])

    label = Label(loading, text="Analyzing results...", bg=theme["bg"], fg=theme["fg"], font=("Arial", 14))
    label.pack(expand=True, pady=30)
    loading.after(1000, lambda: proceed_to_exercise(result, loading))


def proceed_to_exercise(result, window):
    window.destroy()

    def delayed_trace():
        theme = get_current_theme()

        next_loading = tk.Tk()
        next_loading.title("Loading Next Exercise")
        next_loading.geometry("300x100")
        next_loading.configure(bg=theme["bg"])

        label = Label(
            next_loading,
            text="Loading next exercise...",
            bg=theme["bg"],
            fg=theme["fg"],
            font=("Arial", 14)
        )
        label.pack(expand=True, pady=30)
        next_loading.after(1500, lambda: (next_loading.destroy(), launch_eye_tracking_app()))
        next_loading.mainloop()

    if result == "Normal":
        launch_eye_tracking_app()
    elif result in ["Hypertropia", "Hypotropia"]:
        launch_brock_string_app(direction="vertical", on_complete=delayed_trace)
    elif result in ["Esotropia", "Exotropia"]:
        launch_brock_string_app(direction="horizontal", on_complete=delayed_trace)




def open_file(file_path=None):
    if not file_path:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        handle_prediction_and_ui(file_path)

def drop(event):
    file_path = event.data.strip('{').strip('}')
    open_file(file_path)

def load_placeholder():
    try:
        placeholder = Image.open("placeholder.png")
        placeholder.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(placeholder)
        image_label.config(image=img_tk)
        image_label.image = img_tk
    except Exception as e:
        print("Failed to load placeholder:", e)

def capture_from_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot access the camera.")
        return
    messagebox.showinfo("Instructions", "Press 'k' to capture image, 'x' to cancel.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Capture - Press 'k' to Save or 'x' to Quit", frame)
        key = cv2.waitKey(1)
        if key == ord('k'):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
                cv2.imwrite(temp.name, frame)
                cap.release()
                cv2.destroyAllWindows()
                handle_prediction_and_ui(temp.name)
                return
        elif key == ord('x'):
            break
    cap.release()
    cv2.destroyAllWindows()

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    root = TkinterDnD.Tk()
    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", drop)
except ImportError:
    root = tk.Tk()

root.title("Eye Condition Predictor")
root.geometry("520x700")
root.option_add("*Font", "Roboto 16")

title_label = Label(root, text="Eye Condition Classifier", font=("Arial", 22, "bold"))
title_label.pack(pady=20)

select_button = Button(root, text="📁 Select Image", command=open_file)
select_button.pack(pady=5)

camera_button = Button(root, text="📷 Use Camera", command=capture_from_camera)
camera_button.pack(pady=5)

toggle_theme_button = Button(root, text="🌓", command=toggle_theme, relief="flat", font=("Arial", 10), width=3)
toggle_theme_button.place(relx=0.95, rely=0.02, anchor="ne")

image_label = Label(root)
image_label.pack(pady=10)

result_label = Label(root, text="", font=("Arial", 18))
result_label.pack(pady=10)

disclaimer_label = Label(root, text="", font=("Arial", 12), wraplength=480, justify="center")
disclaimer_label.pack(pady=5)

info_label = Label(
    root,
    text="📁 Select or drag an image file\n📷 Or click 'Use Camera' to capture live",
    font=("Arial", 14), justify="center"
)
info_label.pack(pady=10)

apply_theme()
load_placeholder()
root.mainloop()
