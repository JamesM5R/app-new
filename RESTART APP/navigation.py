import customtkinter as ctk
from PIL import Image
import os

class NavigationFrame(ctk.CTkFrame):
    def __init__(self, parent, select_frame_callback):
        super().__init__(parent, corner_radius=0)
        self.select_frame_callback = select_frame_callback

        # Configure rows to allow logo to stay at the bottom
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=0)

        image_path = os.path.join(os.path.dirname(__file__), "test_images")
        self.images = {
            "home": ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20)),
            "send_email": ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "email_light.png")),
                                       dark_image=Image.open(os.path.join(image_path, "email_dark.png")), size=(20, 20)),
            "analysis": ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "analytics_light.png")),
                                     dark_image=Image.open(os.path.join(image_path, "analytics_dark.png")), size=(20, 20)),
            "dashboard": ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "dashboard_light.png")),
                                       dark_image=Image.open(os.path.join(image_path, "dashboard_dark.png")), size=(20, 20)),
            "logo": ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "logo.png")),
                                 dark_image=Image.open(os.path.join(image_path, "logo.png")), size=(150, 30))  # Adjust size as needed
        }

        # Create navigation buttons
        self.buttons = {}
        self.create_buttons()

        # Add logo at the bottom
        self.logo_label = ctk.CTkLabel(self, text="", image=self.images["logo"])
        self.logo_label.grid(row=6, column=0, padx=40, pady=10, sticky="s")

        # Toggle button
        self.toggle_button = ctk.CTkButton(parent, text="X", width=40, height=40, command=self.toggle_navigation)
        self.toggle_button.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    def create_buttons(self):
        """Create navigation buttons."""
        self.buttons["home"] = ctk.CTkLabel(self, text="", height=70)
        self.buttons["home"].grid(row=0, column=0, sticky="ew")

        self.buttons["home"] = ctk.CTkButton(self, text="Home", font=("Arial", 14, "bold"), image=self.images["home"], fg_color="transparent", 
                                             text_color=("gray10", "gray90"), hover_color=("dodgerblue", "blue2"), 
                                             anchor="w", command=lambda: self.select_frame_callback("home"))
        self.buttons["home"].grid(row=1, column=0, sticky="ew")

        self.buttons["send_email"] = ctk.CTkButton(self, text="Send Email", font=("Arial", 14, "bold"), image=self.images["send_email"], fg_color="transparent",
                                                   text_color=("gray10", "gray90"), hover_color=("dodgerblue", "blue2"), 
                                                   anchor="w", command=lambda: self.select_frame_callback("send_email"))
        self.buttons["send_email"].grid(row=2, column=0, sticky="ew")

        self.buttons["analysis"] = ctk.CTkButton(self, text="Analysis", font=("Arial", 14, "bold"), image=self.images["analysis"], fg_color="transparent",
                                                 text_color=("gray10", "gray90"), hover_color=("dodgerblue", "blue2"), 
                                                 anchor="w", command=lambda: self.select_frame_callback("analysis"))
        self.buttons["analysis"].grid(row=3, column=0, sticky="ew")

        self.buttons["dashboard"] = ctk.CTkButton(self, text="Dashboard", font=("Arial", 14, "bold"), image=self.images["dashboard"], fg_color="transparent",
                                                  text_color=("gray10", "gray90"), hover_color=("dodgerblue", "blue2"), 
                                                  anchor="w", command=lambda: self.select_frame_callback("dashboard"))
        self.buttons["dashboard"].grid(row=4, column=0, sticky="ew")

    def update_button_colors(self, selected_frame):
        """Update the button colors based on the selected frame."""
        for name, button in self.buttons.items():
            button.configure(fg_color=("dodgerblue", "blue2") if name == selected_frame else "transparent")

    def toggle_navigation(self):
        """Toggle the visibility of the navigation frame."""
        if self.winfo_ismapped():
            self.grid_forget()  # Hide navigation
            self.toggle_button.configure(text="☰")
        else:
            self.grid(row=0, column=0, sticky="nsw")  # Show navigation
            self.toggle_button.configure(text="X")
