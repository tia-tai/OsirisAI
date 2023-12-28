import stat
import customtkinter
import speech_recognition as sr
import pyttsx3


customtkinter.set_appearance_mode("System")
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


class OsirisUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # New Window
        self.title("Osiris")
        self.geometry("1100x580")
        self.iconbitmap("gui/icon.ico")
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
            command=self.record,
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
            self, width=200, state="disabled", wrap="word", activate_scrollbars="n"
        )
        self.recordbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.responsebox = customtkinter.CTkTextbox(
            self, width=200, state="disabled", wrap="word", activate_scrollbars="n"
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
        try:
            self.recordbox.insert("0.0", text=r.recognize_google(audio))
        except sr.UnknownValueError:
            self.recordbox.insert("0.0", text="Unknown")
        except sr.RequestError as e:
            self.responsebox.insert("0.0", text=e)

    def change_appearance_mode(self, appearance_mode: str):
        customtkinter.set_appearance_mode(appearance_mode)

    def change_scaling(self, scale: str):
        scale_rate = int(scale.replace("%", "")) / 100
        customtkinter.set_widget_scaling(scale_rate)


app = OsirisUI()
app.mainloop()