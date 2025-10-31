import os
import threading
import tkinter as tk
from gtts import gTTS
from tkinter import ttk
import speech_recognition as sr
from playsound import playsound
from deep_translator import GoogleTranslator
from google.transliteration import transliterate_text

# Create main window
win = tk.Tk()
win.geometry("700x500")
win.title("Real-Time Voice🎙️ Translator🔊")
icon = tk.PhotoImage(file="icon.png")
win.iconphoto(False, icon)

# Labels and text boxes
input_label = tk.Label(win, text="Input / Recognized Text ⮯")
input_label.pack()
input_text = tk.Text(win, height=5, width=50)
input_text.pack()

output_label = tk.Label(win, text="Translated Text ⮯")
output_label.pack()
output_text = tk.Text(win, height=5, width=50)
output_text.pack()

# Languages
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "French": "fr",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Punjabi": "pa"
}
language_names = list(language_codes.keys())

# Input Language
input_lang_label = tk.Label(win, text="Select Input Language:")
input_lang_label.pack()
input_lang = ttk.Combobox(win, values=language_names)
input_lang.set("English")
input_lang.pack()

# Output Language
output_lang_label = tk.Label(win, text="Select Output Language:")
output_lang_label.pack()
output_lang = ttk.Combobox(win, values=language_names)
output_lang.set("Hindi")
output_lang.pack()

# Mode selection
mode_label = tk.Label(win, text="Select Mode:")
mode_label.pack()
mode_var = tk.StringVar(value="Voice")
mode_dropdown = ttk.Combobox(win, textvariable=mode_var, values=["Voice", "Text"])
mode_dropdown.pack()

blank_space = tk.Label(win, text="")
blank_space.pack()

keep_running = False

# --- Main translation function ---
def update_translation():
    global keep_running
    if not keep_running:
        return

    mode = mode_var.get()
    source_lang = language_codes[input_lang.get()]
    target_lang = language_codes[output_lang.get()]

    if mode == "Voice":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            output_text.insert(tk.END, "🎤 Speak Now...\n")
            win.update()
            audio = r.listen(source)

        try:
            speech_text = r.recognize_google(audio)
            input_text.insert(tk.END, f"{speech_text}\n")

            if speech_text.lower() in {'exit', 'stop'}:
                keep_running = False
                return

            translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(speech_text)
            output_text.insert(tk.END, translated_text + "\n")

            voice = gTTS(translated_text, lang=target_lang)
            voice.save("voice.mp3")
            playsound("voice.mp3")
            os.remove("voice.mp3")

        except sr.UnknownValueError:
            output_text.insert(tk.END, "Could not understand audio.\n")
        except sr.RequestError:
            output_text.insert(tk.END, "Translation service error.\n")

    elif mode == "Text":
        user_text = input_text.get("1.0", tk.END).strip()
        if user_text:
            translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(user_text)
            output_text.insert(tk.END, translated_text + "\n")

            voice = gTTS(translated_text, lang=target_lang)
            voice.save("voice.mp3")
            playsound("voice.mp3")
            os.remove("voice.mp3")
        else:
            output_text.insert(tk.END, "⚠️ Please enter some text to translate.\n")

    if keep_running:
        win.after(100, update_translation)

def run_translator():
    global keep_running
    if not keep_running:
        keep_running = True
        threading.Thread(target=update_translation).start()

def kill_execution():
    global keep_running
    keep_running = False
    output_text.insert(tk.END, "🛑 Translation stopped.\n")

# ---- ABOUT SECTION ----
def open_about_page():
    about_window = tk.Toplevel()
    about_window.title("About Project")
    about_window.geometry("400x200")
    about_window.configure(bg="#f0f0f0")
    about_window.iconphoto(False, icon)

    title_label = tk.Label(
        about_window,
        text="Real-Time Voice Translator",
        font=("Arial", 14, "bold"),
        bg="#f0f0f0",
        fg="#2c3e50"
    )
    title_label.pack(pady=8)

    info_label = tk.Label(
        about_window,
        text=("This project is based on machine learning and ai .\n"
              "It is a Real-Time Voice Translator made using Python.\n"
              "It converts spoken or written text from one language to another instantly."),
        font=("Arial", 10),
        bg="#f0f0f0",
        fg="#34495e",
        justify="center"
    )
    info_label.pack(pady=6)

    close_btn = tk.Button(
        about_window,
        text="Close",
        command=about_window.destroy,
        bg="#2980b9",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="raised",
        padx=10,
        pady=3
    )
    close_btn.pack(pady=10)

# --- Buttons ---
run_button = tk.Button(win, text="Start Translation", command=run_translator)
run_button.place(relx=0.25, rely=0.9, anchor="c")

kill_button = tk.Button(win, text="Kill Execution", command=kill_execution)
kill_button.place(relx=0.5, rely=0.9, anchor="c")

about_button = tk.Button(win, text="About this project", command=open_about_page)
about_button.place(relx=0.75, rely=0.9, anchor="c")

# Run the app
win.mainloop()
