from datetime import datetime
import sys
import pandas as pd
import win32com.client as win32
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pptx import Presentation
from pptx.util import Inches
import io
from PIL import Image
import os

class SendEmailFrame(ctk.CTkFrame):
    def __init__(self, parent, analysis_callback):
        super().__init__(parent, fg_color="white", corner_radius=10)
        self.grid_rowconfigure(0, weight=1)  # Expandable space
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=0) # Footer at the bottom        
        # Store the analysis callback to call when done
        self.analysis_callback = analysis_callback
        
        self.file_path = None
        self.date_of_send = None

        # Construct the image path
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")        
        # Load the image
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "header2.png")), size=(500, 150))
        self.home_frame_large_image_label = ctk.CTkLabel(self, text="", image=self.large_test_image)
        self.home_frame_large_image_label.pack(padx=20, pady=10)


        # Step 1: File upload
        step1_label = ctk.CTkLabel(self, text="Step 1: Upload an Excel file", font=("Arial", 18, "bold"), text_color=("dodgerblue", "blue2"))
        step1_label.pack(padx=20, pady=10)

        upload_button = ctk.CTkButton(self, text="Upload File", width=150, command=self.upload_file)
        upload_button.pack(padx=10, pady=5)

        self.upload_log = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.upload_log.pack(padx=10, pady=5)

        # Step 2: Email customization
        step2_label = ctk.CTkLabel(self, text="Step 2: Customize email subject and body:", font=("Arial", 18, "bold"), text_color=("dodgerblue", "blue2"))
        step2_label.pack(padx=20, pady=5)

        self.subject_input = ctk.CTkEntry(self, placeholder_text=">> Enter email subject...", text_color="black", fg_color="white", width=615, height=40, font=("Arial", 14))
        self.subject_input.pack(padx=20, pady=5)

        self.body_input = ctk.CTkTextbox(self, text_color="black", fg_color="white", width=615, height=220, font=("Arial", 12), border_width=2)
        self.body_input.insert("1.0", "Bonjour {name},\n\nVotre absence a été notée pour les dates suivantes : {dates}.\n\n\n\n\n\n\nMerci de fournir une justification.\n\n\n\nCordialement,\n")
        self.body_input.pack(padx=20, pady=10)

        send_button = ctk.CTkButton(self, text="Send Emails", width=150, command=self.send_emails)
        send_button.pack(padx=20, pady=10)

        self.email_log = ctk.CTkTextbox(self, width=600, height=200, text_color="black", fg_color="white", font=("Arial", 12), border_width=2)
        self.email_log.pack(padx=20, pady=10)

        # Footer
        footer = ctk.CTkLabel(self, text="© 2024 Workspace Management Application. Capgemini Engineering.", font=("Arial", 10, 'italic'), text_color="black", fg_color="white")
        footer.pack(padx=20, pady=10, side="bottom")

    def upload_file(self):
        """Handle file upload for the Send Emails section."""
        file_name = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if file_name:
            self.file_path = file_name
            self.upload_log.configure(text=f">> File uploaded: {file_name}", text_color="green", font=("Arial", 12, "bold"))
        else:
            self.upload_log.configure(text=">> No file selected.", text_color="red")

    def send_emails(self):
        """Send emails based on the uploaded Excel file."""
        if not self.file_path:
            self.email_log.insert("1.0", ">> No file uploaded!\n")
            return

        try:
            # Read Excel file
            data = pd.read_excel(self.file_path)
            outlook = win32.Dispatch("Outlook.Application")

            # Capture the date when emails are sent
            self.date_of_send = datetime.now().strftime("%Y-%m-%d")

            # Validate required columns
            required_columns = {"Name", "Email Name", "Dates of Absences", "Email Manager"}
            if not required_columns.issubset(data.columns):
                missing = required_columns - set(data.columns)
                self.email_log.insert("1.0", f">> Missing columns: {', '.join(missing)}\n")
                return

            # Calculate the Week based on "Dates of Absences"
            if "Dates of Absences" in data.columns:
                data["Week"] = pd.to_datetime(
                    data["Dates of Absences"], errors="coerce"
                ).apply(lambda x: x.isocalendar()[1] if pd.notnull(x) else None)
            else:
                self.email_log.insert("1.0", ">> Column 'Dates of Absences' not found in data. Skipping week calculation.\n")

            # Send emails and update the data
            for _, row in data.iterrows():
                try:
                    mail = outlook.CreateItem(0)
                    mail.Subject = self.subject_input.get()
                    mail.Body = self.body_input.get("1.0", "end-1c").format(name=row["Name"], dates=row["Dates of Absences"])
                    mail.To = row["Email Name"]
                    mail.CC = row["Email Manager"]
                    mail.Send()

                    # Update the data with the sent date
                    data.loc[data['Email Name'] == row['Email Name'], 'Date of Send'] = self.date_of_send
                    self.email_log.insert("1.0", f">> Email sent to {row['Email Name']}.\n")
                except Exception as e:
                    self.email_log.insert("1.0", f">> Failed to send email to {row['Email Name']}: {str(e)}\n")

            # After sending emails, pass the updated data to the analysis callback
            if self.analysis_callback:
                self.analysis_callback(data)

        except Exception as e:
            self.email_log.insert("1.0", f">> Error reading Excel file: {str(e)}\n")
