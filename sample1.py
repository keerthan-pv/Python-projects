import tkinter as tk
from deep_translator import GoogleTranslator
from tkinter import ttk
from gtts import gTTS
import tempfile
import os
import pygame


class SpeechifyApp:
    def __init__(self, master):
        self.master = master
        master.title("Speechify App")
        master.configure(bg="black")

        for i in range(10):
            master.grid_rowconfigure(i, weight=1)
        for i in range(8):
            master.grid_columnconfigure(i, weight=1)

        style = ttk.Style()
        style.configure("TScale", troughcolor="black", sliderthickness=20, sliderlength=20, troughrelief='flat')

        self.label = tk.Label(master, text="ENTER TEXT:", font=("Arial", 20), bg="black", fg="white")
        self.label.place(relx=0.5, rely=0.03, anchor='n')

        self.text_entry = tk.Text(master, height=19, width=111, font=("Arial", 17), bg="white", fg="black")
        self.text_entry.place(relx=0.5, rely=0.1, anchor='n')

        self.language_label = tk.Label(master, text="Select Language :", bg="black", fg="white", font=("Arial", 20))
        self.language_label.place(relx=0.05, rely=0.73, anchor='w')

        self.language_var = tk.StringVar(master)
        self.language_var.set("English")

        languages = ["English", "Kannada", "Hindi", "Tamil", "Telugu"]
        self.language_menu = tk.OptionMenu(master, self.language_var, *languages)
        self.language_menu.config(font=("Arial", 20), width=8)
        self.language_menu.place(relx=0.2, rely=0.73, anchor='w')

        self.translate_button = tk.Button(master, text="Translate and Speak", command=self.translate_and_speak,
                                          bg="#4CAF50", fg="white", font=("Arial", 20))
        self.translate_button.place(relx=0.915, rely=0.73, anchor='e')

        self.voice_label = tk.Label(master, text="Select Voice:", bg="black", fg="white", font=("Arial", 20))
        self.voice_label.place(relx=0.089, rely=0.8, anchor='w')

        self.voice_var = tk.StringVar(master)
        self.voice_var.set("Default")

        voices = ["Default", "Male", "Female"]
        self.voice_menu = tk.OptionMenu(master, self.voice_var, *voices)
        self.voice_menu.config(font=("Arial", 20), width=8)
        self.voice_menu.place(relx=0.2, rely=0.8, anchor='w')

        self.speed_label = tk.Label(master, text="Select Speed :", bg="black", fg="white", font=("Arial", 20))
        self.speed_label.place(relx=0.076, rely=0.87, anchor='w')

        speed_values = ["0.5x", "0.6x", "0.7x", "0.8x", "0.9x", "1.0x", "1.1x", "1.2x", "1.3x", "1.4x", "1.5x", "1.6x",
                        "1.7x", "1.8x", "1.9x", "2.0x"]
        self.speed_var = tk.StringVar()
        self.speed_var.set("1.0x")

        self.speed_menu = ttk.Combobox(master, textvariable=self.speed_var, values=speed_values, font=("Arial", 20), width=10)
        self.speed_menu.place(relx=0.2, rely=0.87, anchor='w')

        self.quit_button = tk.Button(master, text="Quit", command=master.destroy, bg="#2E86C1", fg="white",
                                     font=("Arial", 20))
        self.quit_button.place(relx=0.85, rely=0.87, anchor='e')

    def translate_and_speak(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        selected_language = self.language_var.get()
        selected_voice = self.voice_var.get()

        language_names = {
            "English": "en",
            "Kannada": "kn",
            "Hindi": "hi",
            "Tamil": "ta",
            "Telugu": "te"
        }

        lang_code = language_names.get(selected_language, "en")
        speed_str = self.speed_var.get()
        speed_value = float(speed_str[:-1])
        slow = speed_value < 1.0

        if not text:
            return

        translated_text = text
        if selected_language != "English":
            translated_text = GoogleTranslator(source='en', target=lang_code).translate(text)

        try:
            if selected_language == "English":
                import pyttsx3
                engine = pyttsx3.init()

                # Set rate (pyttsx3 default is ~200)
                engine.setProperty('rate', int(200 * speed_value))

                # Set voice
                voices = engine.getProperty('voices')
                if selected_voice == "Male":
                    engine.setProperty('voice', voices[0].id)
                elif selected_voice == "Female" and len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)

                engine.say(translated_text)
                engine.runAndWait()
            else:
                tts = gTTS(text=translated_text, lang=lang_code, slow=slow)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    temp_path = fp.name
                    tts.save(temp_path)

                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                pygame.mixer.quit()
                os.remove(temp_path)

        except Exception as e:
            print("Error in TTS:", e)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = SpeechifyApp(root)
    root.mainloop()
