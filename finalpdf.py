import tkinter as tk
from tkinter import scrolledtext, filedialog
import pygame
import pyttsx3
from threading import Thread
import fitz
import os

class TextPlayerApp(tk.Toplevel):
    def __init__(self, root):
        self.root = root
        self.audio_loaded = False
        self.is_paused = False
        self.audio_thread = None

    def create_window(self):
        self.root.attributes('-fullscreen', True)
        self.root.title("Text Player App")
        self.root.configure(bg="black")

        self.pdf_reader_label = tk.Label(self.root, text="PDF Reader:", font=("Helvetica", 20), bg="black", fg="white")
        self.pdf_reader_label.place(relx=0.47, rely=0.02)

        self.text_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=180, height=42, bg="white", fg="black")
        self.text_box.place(relx=0.022, rely=0.09)

        self.open_pdf_button = tk.Button(self.root, text="Open PDF", command=self.open_pdf, bg="white", fg="black", font="14")
        self.open_pdf_button.place(relx=0.078, rely=0.9)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_text, bg="green", fg="white", font="14", height="1", width="9")
        self.play_button.place(relx=0.48, rely=0.86)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_text, bg="blue", fg="white", font="14", height="1", width="9")
        self.pause_button.place(relx=0.48, rely=0.93)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_app, bg="red", fg="black", font="18", height="1", width="9")
        self.quit_button.place(relx=0.86, rely=0.9)

        pygame.mixer.init()

    def open_pdf(self):
        self.root.grab_set()
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.root.grab_release()

        if file_path:
            pdf_text = self.extract_text_from_pdf(file_path)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, pdf_text)

    def extract_text_from_pdf(self, file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def play_text(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        elif not self.audio_loaded:
            text_to_play = self.text_box.get("1.0", tk.END).strip()
            if text_to_play:
                self.audio_thread = Thread(target=self.play_audio, args=(text_to_play,))
                self.audio_thread.start()

    def play_audio(self, text_to_play):
        temp_file_path = "temp.wav"

        engine = pyttsx3.init()
        engine.save_to_file(text_to_play, temp_file_path)
        engine.runAndWait()

        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        self.audio_loaded = True

    def pause_text(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True

    def quit_app(self):
        try:
            # Stop music if playing
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print("Error stopping music:", e)

        # Remove temp.wav if it exists
        try:
            if os.path.exists("temp.wav"):
                os.remove("temp.wav")
        except Exception as e:
            print("Error deleting temp.wav:", e)

        # Properly shut down the app
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextPlayerApp(root)
    app.create_window()
    root.mainloop()
