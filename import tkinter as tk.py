import tkinter as tk
import numpy as np
import threading
from PIL import ImageGrab, Image, ImageOps, ImageFilter, ImageTk
import ctypes
import time

def apply_effect(image, effect, params):
    if effect == "blur":
        return apply_gaussian_blur(image, params)
    elif effect == "pixelate":
        return apply_pixelation(image, params)
    elif effect == "solarize":
        return apply_solarize(image, params)
    elif effect == "color_reduction":
        return apply_color_reduction(image, params)
    elif effect == "wave":
        return apply_wave_distortion(image, params)

def apply_gaussian_blur(image, sigma):
    return np.array(image.filter(ImageFilter.GaussianBlur(sigma)))

def apply_pixelation(image, pixel_size):
    return np.array(image.resize((image.width // pixel_size, image.height // pixel_size), Image.NEAREST).resize((image.width, image.height), Image.NEAREST))

def apply_solarize(image, threshold):
    return np.array(ImageOps.solarize(image, threshold=threshold))

def apply_color_reduction(image, colors):
    return np.array(image.quantize(colors=colors))

def apply_wave_distortion(image, amplitude):
    height, width = image.shape[:2]
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    x_shift = amplitude * np.sin(2 * np.pi * x / 128.0)
    y_shift = amplitude * np.cos(2 * np.pi * y / 128.0)
    distorted_coords = np.dstack((x + x_shift, y + y_shift))
    distorted_coords = distorted_coords.reshape(height, width, 2)
    distorted_image = np.zeros_like(image)
    mask = (distorted_coords[:, :, 0] >= 0) & (distorted_coords[:, :, 0] < width) & (distorted_coords[:, :, 1] >= 0) & (distorted_coords[:, :, 1] < height)
    distorted_coords = distorted_coords[mask].astype(int)
    distorted_image[mask] = image[distorted_coords[:, 1], distorted_coords[:, 0]]
    return distorted_image

def focus_window(event):
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.SetForegroundWindow(hwnd)

def update_effect(root, canvas, effect, params):
    original_image = np.array(ImageGrab.grab(bbox=(root.winfo_rootx(), root.winfo_rooty(), root.winfo_rootx() + root.winfo_width(), root.winfo_rooty() + root.winfo_height())))
    processed_image = apply_effect(original_image, effect, params)
    photo = ImageTk.PhotoImage(image=Image.fromarray(processed_image))
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.photo = photo  # Keep a reference to prevent garbage collection
    if effect == "wave":
        params = (params + 1) % 20
    elif effect == "blur":
        params = (params + 1) % 20
    elif effect == "pixelate":
        params = (params + 1) % 20
    elif effect == "solarize":
        params = (params + 10) % 256
    elif effect == "color_reduction":
        params = max(2, params - 10)
    root.after(5, update_effect, root, canvas, effect, params)  # Update every 50 milliseconds

def create_window(effect, params):
    root = tk.Tk()
    root.attributes("-transparentcolor", "white")
    root.configure(bg='white')
    root.attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.state('zoomed')
    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='white', highlightthickness=0)
    canvas.pack()
    root.overrideredirect(True)
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.bind("<Tab>", focus_window)
    update_effect(root, canvas, effect, params)
    root.mainloop()

create_window("wave", 0)
