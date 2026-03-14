import secrets
import string
import customtkinter as ctk
import tkinter as tk

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Secure Password Generator")
        self.geometry("500x480")
        self.resizable(False, False)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self, 
            text="Password Generator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(30, 20))

        # Password Entry / Output
        self.password_var = ctk.StringVar()
        self.password_entry = ctk.CTkEntry(
            self,
            textvariable=self.password_var,
            width=350,
            height=45,
            font=ctk.CTkFont(size=18),
            justify="center",
            state="readonly"
        )
        self.password_entry.pack(pady=10)

        # Main Frame for Controls
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(pady=10, padx=20, fill="x")

        # Length Controller
        self.length_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.length_frame.pack(pady=10)

        self.length_label = ctk.CTkLabel(
            self.length_frame,
            text="Password Length:",
            font=ctk.CTkFont(size=14)
        )
        self.length_label.pack(side="left", padx=10)

        self.length_slider = ctk.CTkSlider(
            self.length_frame,
            from_=6,
            to=32,
            number_of_steps=26,
            command=self.update_length_label
        )
        self.length_slider.set(12)
        self.length_slider.pack(side="left", padx=10)

        self.length_value_label = ctk.CTkLabel(
            self.length_frame,
            text="12",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.length_value_label.pack(side="left")

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.generate_btn = ctk.CTkButton(
            self.button_frame,
            text="Generate",
            command=self.generate_password,
            width=150,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.generate_btn.pack(side="left", padx=10)

        self.copy_btn = ctk.CTkButton(
            self.button_frame,
            text="Copy",
            command=self.copy_password,
            width=150,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#455A64",  # A different shade for copy
            hover_color="#37474F"
        )
        self.copy_btn.pack(side="left", padx=10)

        # Strength Indicator
        self.strength_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.strength_frame.pack(pady=(10, 20))

        self.progress = ctk.CTkProgressBar(self.strength_frame, width=300)
        self.progress.set(0)
        self.progress.pack(pady=5)

        self.strength_label = ctk.CTkLabel(
            self.strength_frame,
            text="Strength: None",
            font=ctk.CTkFont(size=14)
        )
        self.strength_label.pack()

    def update_length_label(self, value):
        self.length_value_label.configure(text=str(int(value)))

    def generate_password(self):
        length = int(self.length_slider.get())
        chars = string.ascii_letters + string.digits + string.punctuation
        
        # Make the entry temporarily editable to insert the password
        self.password_entry.configure(state="normal")
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        self.password_var.set(password)
        
        # Set back to readonly
        self.password_entry.configure(state="readonly")
        
        self.update_strength(password)

    def copy_password(self):
        if self.password_var.get():
            self.clipboard_clear()
            self.clipboard_append(self.password_var.get())

            # Temporarily change button text to indicate success
            original_text = self.copy_btn.cget("text")
            self.copy_btn.configure(text="Copied!")
            self.after(1500, lambda: self.copy_btn.configure(text=original_text))

    def update_strength(self, password):
        score = 0
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in string.punctuation for c in password): score += 1
        if len(password) >= 12: score += 1

        self.progress.set(score / 5.0)

        if score <= 2:
            self.strength_label.configure(text="Strength: Weak 🔴", text_color="#FF5252")
            self.progress.configure(progress_color="#FF5252")
        elif score == 3:
            self.strength_label.configure(text="Strength: Medium 🟡", text_color="#FFD740")
            self.progress.configure(progress_color="#FFD740")
        else:
            self.strength_label.configure(text="Strength: Strong 🟢", text_color="#69F0AE")
            self.progress.configure(progress_color="#69F0AE")

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()