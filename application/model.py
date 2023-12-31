import customtkinter
import pyttsx3
import threading
import speech_recognition as sr
from core import gpt_response_generator  # noqa: E402

customtkinter.set_appearance_mode("System")
engine = pyttsx3.init('sapi5')
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0")
engine.setProperty("rate", 250)


class OsirisUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # New Window
        self.title("Osiris")
        self.geometry("1100x580")
        self.iconbitmap("application/icon.ico")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Osiris",
            font=customtkinter.CTkFont(size=30, weight="bold"),
        )
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.speech_btn = customtkinter.CTkButton(
            self.sidebar_frame,
            command=lambda: self.start_record(None),
            text="Speak",
        )
        self.speech_btn.grid(row=1, column=0, padx=20, pady=10)

        self.progressbar = customtkinter.CTkProgressBar(self.sidebar_frame)
        self.progressbar.grid(
            row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew"
        )
        self.progressbar.set(1)

        self.appearance_mode = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Theme:",
            anchor="w",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.appearance_mode.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode,
        )
        self.appearance_mode_option.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_option.set("System")

        self.scaling = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Scaling",
            anchor="w",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.scaling.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_option = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling,
        )
        self.scaling_option.set("100%")
        self.scaling_option.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.recordbox = customtkinter.CTkTextbox(
            self, width=200, wrap="word", activate_scrollbars="n", state="disabled"
        )
        self.recordbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.responsebox = customtkinter.CTkTextbox(
            self, width=200, wrap="word", activate_scrollbars="n", state="disabled"
        )
        self.responsebox.grid(
            row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )

    # Record Voice to String

    def speak(self, audio):
        engine.say(audio)
        engine.runAndWait()

    def record(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Listening...")
            audio = r.listen(source)
            self.recordbox.configure(state="normal")
            self.recordbox.delete("0.0", "end")
            self.responsebox.configure(state="normal")
            self.responsebox.delete("0.0", "end")

        try:
            self.recordbox.insert("0.0", text=r.recognize_google(audio))
            self.recordbox.configure(state="disabled")
            response = gpt_response_generator(r.recognize_google(audio))
            self.responsebox.insert("0.0", text=response)
            self.responsebox.configure(state="disabled")
            self.speak(response)
        except sr.UnknownValueError:
            self.recordbox.insert("0.0", text="Unknown")
            self.recordbox.configure(state="disabled")
        except sr.RequestError as e:
            self.responsebox.insert("0.0", text=e)
            self.responsebox.configure(state="disabled")

    # Run record in a seperate thread to prevent the application from freezing
    def start_record(self, event):
        global record_thread
        record_thread = threading.Thread(target=self.record)
        record_thread.daemon = True
        self.progressbar.configure(mode="indeterminate")
        self.progressbar.start()
        record_thread.start()
        self.after(20, self.stop_record)

    # Checks if the record thread is still alive and runs the function again if it is
    def stop_record(self):
        if record_thread.is_alive():
            self.after(20, self.stop_record)
        else:
            self.progressbar.configure(mode="determinate")
            self.progressbar.set(1)
            self.progressbar.stop()

    def change_appearance_mode(self, appearance_mode: str):
        customtkinter.set_appearance_mode(appearance_mode)

    def change_scaling(self, scale: str):
        scale_rate = int(scale.replace("%", "")) / 100
        customtkinter.set_widget_scaling(scale_rate)


app = OsirisUI()
app.mainloop()
