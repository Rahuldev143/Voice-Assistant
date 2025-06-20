import speech_recognition as sr
import pyttsx3
import subprocess
import sys
import datetime
import pywhatkit
import pyjokes
import logging
import webbrowser
import os
import tkinter as tk
from tkinter import messagebox
import openai


openai.api_key = "your-api-key"  

logging.basicConfig(filename='assistant.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class VoiceAssistant:
    def __init__(self, ui_callback, wake_word="rahul"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.running = False
        self.ui_callback = ui_callback

    def speak(self, text):
        logging.info(f"Speaking: {text}")
        self.ui_callback(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout=None, phrase_time_limit=5):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                self.ui_callback("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = self.recognizer.recognize_google(audio, language='en_US').lower()
                logging.info(f"Recognized speech: {text}")
                self.ui_callback(f"You: {text}")
                return text
            except Exception as e:
                logging.warning(f"Speech recognition error: {e}")
                self.ui_callback("Didn't catch that.")
                return ""

    def open_software(self, software_name):
        software_name = software_name.lower()
        try:
            if 'chrome' in software_name:
                self.speak('Opening Chrome...')
                subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])

            elif 'microsoft edge' in software_name or 'edge' in software_name:
                self.speak('Opening Microsoft Edge...')
                subprocess.Popen([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"])

            elif 'youtube' in software_name:
                self.speak('Opening YouTube...')
                pywhatkit.playonyt("youtube")

            elif 'play music' in software_name or 'music' in software_name:
                self.speak('Opening music...')
                music_path = r"C:\Users\user\Downloads\download-Rahul.mp3"
                if os.path.exists(music_path):
                    os.startfile(music_path)  
                else:
                    self.speak("Music file not found.")

            elif 'notepad' in software_name:
                self.speak('Opening Notepad...')
                subprocess.Popen(['notepad.exe'])

            elif 'calculator' in software_name:
                self.speak('Opening Calculator...')
                subprocess.Popen(['calc.exe'])

            else:
                self.speak(f"I couldn't find the software {software_name}")

        except Exception as e:
            logging.error(f"Error opening {software_name}: {e}")
            self.speak(f"Failed to open {software_name}")

    def close_software(self, software_name):
        software_name = software_name.lower()
        try:
            if 'chrome' in software_name:
                self.speak('Closing Chrome...')
                os.system("taskkill /f /im chrome.exe")

            elif 'edge' in software_name:
                self.speak('Closing Microsoft Edge...')
                os.system("taskkill /f /im msedge.exe")

            elif 'notepad' in software_name:
                self.speak('Closing Notepad...')
                os.system("taskkill /f /im notepad.exe")

            elif 'calculator' in software_name:
                self.speak('Closing Calculator...')
                os.system("taskkill /f /im calculator.exe")

            else:
                self.speak(f"I couldn't find any open software named {software_name}")

        except Exception as e:
            logging.error(f"Error closing {software_name}: {e}")
            self.speak(f"Failed to close {software_name}")

    def tell_time(self):
        now = datetime.datetime.now().strftime('%I:%M %p')
        self.speak(f"The current time is {now}")

    def tell_joke(self):
        joke = pyjokes.get_joke()
        self.speak(joke)

    def ask_openai(self, prompt):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
                n=1,
                stop=None,
            )
            answer = response.choices[0].text.strip()
            return answer
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return "Sorry, I couldn't get an answer from OpenAI."

    def process_command(self, command):
        if 'stop' in command or 'exit' in command or 'quit' in command:
            self.speak("Goodbye!")
            self.running = False
            sys.exit()

        elif 'open' in command:
            software = command.replace('open', '').strip()
            self.open_software(software)

        elif 'close' in command:
            software = command.replace('close', '').strip()
            self.close_software(software)

        elif 'time' in command:
            self.tell_time()

        elif 'joke' in command:
            self.tell_joke()

        elif 'who made you' in command:
            self.speak("I was made by Rahul dev.")

        elif 'how are you' in command or 'how r u' in command:
            self.speak("All good, and what about you?")

        elif 'what is your name' in command or 'what ise your name' in command:
            self.speak("My name is Rahul, your best friend.")

        elif 'which is your favourite ipl team' in command:
            self.speak("CSK is my favourite IPL team.")

        else:
            response = self.ask_openai(command)
            self.speak(response)

    def run(self):
        self.running = True
        self.speak("Voice assistant started. Say the wake word to begin.")

        while self.running:
            text = self.listen(timeout=5, phrase_time_limit=3)
            if self.wake_word in text:
                self.speak("Hello! I'm ready to help you.")
                break

        while self.running:
            command = self.listen(timeout=5, phrase_time_limit=5)
            if command:
                self.process_command(command)


    def stop(self):
        self.running = False
        self.speak("Voice assistant stopped.")


class AssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.assistant = None

        self.login_frame = tk.Frame(root)
        self.main_frame = tk.Frame(root)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.setup_login_ui()

    def setup_login_ui(self):
        self.login_frame.pack(padx=10, pady=10)
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0)
        tk.Entry(self.login_frame, textvariable=self.username_var).grid(row=0, column=1)
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0)
        tk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1)
        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)

    def setup_main_ui(self):
        self.login_frame.pack_forget()
        self.main_frame.pack(padx=10, pady=10)

        self.log_display = tk.Text(self.main_frame, width=60, height=15, state='disabled')
        self.log_display.pack(pady=10)

        tk.Button(self.main_frame, text="Start Assistant", command=self.start_assistant).pack(side=tk.LEFT, padx=10)
        tk.Button(self.main_frame, text="Stop Assistant", command=self.stop_assistant).pack(side=tk.RIGHT, padx=10)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username == "Dev" and password == "1234":
            logging.info("User Dev logged in successfully.")
            messagebox.showinfo("Login", "Login successful!")
            self.setup_main_ui()
        else:
            logging.warning("Login attempt failed.")
            messagebox.showerror("Login", "Invalid credentials!")

    def update_log(self, message):
        self.log_display.config(state='normal')
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.config(state='disabled')
        self.log_display.see(tk.END)

    def start_assistant(self):
        if not self.assistant or not self.assistant.running:
            self.assistant = VoiceAssistant(ui_callback=self.update_log)
            self.root.after(100, self.run_assistant)

    def run_assistant(self):
        import threading
        threading.Thread(target=self.assistant.run, daemon=True).start()

    def stop_assistant(self):
        if self.assistant:
            self.assistant.stop()


if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantApp(root)
    root.mainloop()
