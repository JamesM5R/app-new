import os
import customtkinter as ctk
from navigation import NavigationFrame
from frame_home import HomeFrame
from frame_send_email import SendEmailFrame
from frame_analysis import AnalysisFrame
from frame_dashboard import DashboardFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App Window Configuration
        self.title("Workspace Management Application")
        self.geometry("1200x640")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        image_path = os.path.join(os.path.dirname(__file__), "test_images", "app_logo.ico")
        self.iconbitmap(image_path)

        # Navigation Frame
        self.navigation_frame = NavigationFrame(self, self.select_frame_by_name)
        self.navigation_frame.grid(row=0, column=0, sticky="nsw", padx=0, pady=0)

        # Frames
        self.frames = {
            "home": HomeFrame(self),  # Implement HomeFrame based on your requirements
            "send_email": SendEmailFrame(self, self.update_analysis_frame),
            "analysis": AnalysisFrame(self),
            "dashboard": DashboardFrame(self)  # Implement DashboardFrame based on your requirements
        }

        # Set the default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        """Switch and display the frame corresponding to the selected name."""
        # Update navigation button states
        self.navigation_frame.update_button_colors(name)

        # Hide all frames
        for frame in self.frames.values():
            frame.grid_forget()

        # Show the selected frame
        if name in self.frames:
            self.frames[name].grid(row=0, column=1, sticky="nsew")

    def update_analysis_frame(self, data):
        """Callback to update the AnalysisFrame with new data."""
        self.frames["analysis"].update_data(data)
        self.select_frame_by_name("analysis")

if __name__ == "__main__":
    app = App()
    app.mainloop()


