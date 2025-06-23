import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
import time
import numpy as np
import threading


class VideoStreamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Video source
        self.vid = cv2.VideoCapture(0)

        # Video Display Canvas
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.grid(row=0, column=0, columnspan=5)

        # Buttons
        self.start_button = tk.Button(window, text="Start Recording", command=self.start_recording)
        self.start_button.grid(row=1, column=0)
        self.stop_button = tk.Button(window, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1)
        self.snapshot_button = tk.Button(window, text="Take Snapshot", command=self.take_snapshot)
        self.snapshot_button.grid(row=1, column=2)
        self.fullscreen_button = tk.Button(window, text="Full Screen", command=self.toggle_fullscreen)
        self.fullscreen_button.grid(row=1, column=3)

        # Filter Menu
        self.filter_var = tk.StringVar()
        self.filter_var.set("None")
        self.filter_menu = tk.OptionMenu(window, self.filter_var, "None", "Gray", "Sepia", "Blur", "Edge Detection",
                                         "Invert", "Cartoon")
        self.filter_menu.grid(row=1, column=4)

        # Timer for Recording
        self.timer_label = tk.Label(window, text="00:00", font=("Helvetica", 16))
        self.timer_label.grid(row=2, column=0, columnspan=5)

        self.is_recording = False
        self.video_writer = None
        self.start_time = None
        self.fullscreen = False

        self.update()
        self.window.mainloop()

    def apply_filter(self, frame):
        filter_selected = self.filter_var.get()
        if filter_selected == "Gray":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif filter_selected == "Sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            frame = cv2.transform(frame, kernel)
            frame = np.clip(frame, 0, 255)
        elif filter_selected == "Blur":
            frame = cv2.GaussianBlur(frame, (15, 15), 0)
        elif filter_selected == "Edge Detection":
            frame = cv2.Canny(frame, 100, 200)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif filter_selected == "Invert":
            frame = cv2.bitwise_not(frame)
        elif filter_selected == "Cartoon":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.medianBlur(gray, 7)
            edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)
            color = cv2.bilateralFilter(frame, 9, 300, 300)
            frame = cv2.bitwise_and(color, color, mask=edges)
        return frame

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = self.apply_filter(frame)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            if self.is_recording:
                self.video_writer.write(frame)
                self.update_timer()

        self.window.after(10, self.update)

    def start_recording(self):
        os.makedirs("recordings", exist_ok=True)
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        self.video_filename = os.path.join("recordings", f"video_{timestamp}.avi")

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.video_writer = cv2.VideoWriter(self.video_filename, fourcc, 20.0,
                                            (int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                             int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        self.is_recording = True
        self.start_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.is_recording = False
        self.video_writer.release()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.timer_label.config(text="00:00")

    def take_snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            frame = self.apply_filter(frame)
            snapshot_path = os.path.join("recordings", f"snapshot_{time.strftime('%Y-%m-%d_%H-%M-%S')}.jpg")
            cv2.imwrite(snapshot_path, frame)
            print(f"Snapshot saved to {snapshot_path}")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.window.attributes("-fullscreen", self.fullscreen)

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoStreamApp(root, "Video Streaming App")