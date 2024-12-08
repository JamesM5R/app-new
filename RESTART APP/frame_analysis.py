import customtkinter as ctk
import pandas as pd
from tkinter import ttk, filedialog
from PIL import Image
import os

class AnalysisFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white", corner_radius=10)
        self.grid_rowconfigure(0, weight=1)  # Expandable space
        self.grid_columnconfigure(0, weight=1)

        # Initialize data and file path
        self.data = None
        self.data_file = "saved_data.csv"  # File to persist data locally

        # Justificative to Category Mapping
        self.category_mapping = {
            "Absence pour raisons de santé": "Absence",
            "Mise à jour manquante": "Mise à jour planning",
            "Autorisation du responsable direct": "Mise à jour planning",
            "Congé planifié": "Mise à jour planning",
            "Décalage de planning": "A verifier",
            "Absence excepionnelle non prévu": "Absence",
            "Intervention chez un client/autre emplacement": "Mise à jour planning",
            "Probléme de badge d'accès": "A verifier",
            "Attente d'information": "Attente d'information",
            "Démission": "Mise à jour planning"
        }

        # Construct the image path
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")        
        # Load the image
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "header3.png")), size=(500, 150))
        self.home_frame_large_image_label = ctk.CTkLabel(self, text="", image=self.large_test_image)
        self.home_frame_large_image_label.pack(padx=20, pady=10)

        # Treeview for data table
        # Configure the style for Treeview headings
        style = ttk.Style()
        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold"),  # Set the font to bold
            foreground="black"  # Set text color
        )
        self.tree = ttk.Treeview(self, columns=(), show="headings", height=10)
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # Configure scrollbar
        tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="right", fill="y")

        # CTkTextbox for logs
        self.log_textbox = ctk.CTkTextbox(
            self,
            width=500,
            height=150,
            text_color="black",
            fg_color="white",
            font=("Arial", 12),
            border_width=2
        )
        self.log_textbox.pack(padx=20, pady=10, fill="x", expand=False)

        # Input fields and buttons
        self.date_entry = ctk.CTkEntry(
            self, placeholder_text="YYYY-MM-DD", width=200, fg_color="white", text_color="black"
        )
        self.date_entry.pack(side="left", padx=10, pady=20)

        self.justificative_combo = ttk.Combobox(
            self, values=list(self.category_mapping.keys()), width=20, state="readonly"
        )
        self.justificative_combo.pack(side="left", padx=10, pady=20)

        add_button = ctk.CTkButton(self, text="Add to Row", command=self.add_to_row)
        add_button.pack(side="left", padx=50, pady=20)

        save_button = ctk.CTkButton(self, text="Save Responses", command=self.save_responses)
        save_button.pack(side="right", padx=10, pady=20)

        # Load existing data if available
        self.load_data_from_file()

    def log_message(self, message):
        """Log messages to the CTkTextbox."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.see("end")  # Auto-scroll to the latest log

    def add_to_row(self):
        """Add Date of Response and Justificative to the selected row."""
        selected_item = self.tree.focus()  # Get selected item in Treeview
        if not selected_item:
            self.log_message(">> No row selected.")
            return

        date_response = self.date_entry.get()
        justificative = self.justificative_combo.get()

        if not date_response or not justificative:
            self.log_message(">> Both Date of Response and Justificative are required.")
            return

        row_values = self.tree.item(selected_item, "values")
        row_idx = self.data.index[self.data["Dates of Absences"] == row_values[0]].tolist()

        if row_idx:
            row_idx = row_idx[0]
            self.data.at[row_idx, "Date of Response"] = date_response
            self.data.at[row_idx, "Justificative"] = justificative
            self.data.at[row_idx, "Category"] = self.category_mapping.get(justificative, "Unknown")
            self.tree.item(selected_item, values=self.data.iloc[row_idx].tolist())
            self.log_message(f">> Updated row {row_idx} with Date: {date_response}, Justificative: {justificative}")

    def save_responses(self):
        """Save the responses and justificative data back to the dataframe."""
        self.save_data_to_file()
        self.log_message(f">> Data saved to {self.data_file}")

    def save_data_to_file(self):
        """Save the current data to a CSV file."""
        if self.data is not None:
            self.data.to_csv(self.data_file, index=False)

    def load_data_from_file(self):
        """Load data from the CSV file if it exists."""
        if os.path.exists(self.data_file):
            self.data = pd.read_csv(self.data_file)
            self.update_data(self.data)
            self.log_message(">> Loaded data from file.")
        else:
            self.log_message(">> No existing data file found.")

    def update_data(self, new_data):
        existing_data = None
        if os.path.exists(self.data_file):
            existing_data = pd.read_csv(self.data_file)

        if existing_data is not None:
            self.data = pd.concat([new_data, existing_data], ignore_index=True)
        else:
            self.data = new_data

        # Add Category column based on Justificative
        if "Category" not in self.data.columns:
            self.data.insert(self.data.columns.get_loc("Justificative"), "Category", "")

        self.data["Category"] = self.data["Justificative"].map(self.category_mapping)

        self.data.drop_duplicates(inplace=True, keep="first")
        self.data.reset_index(drop=True, inplace=True)

        # Update the Treeview
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.data.columns)
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        for _, row in self.data.iterrows():
            self.tree.insert("", "end", values=row.tolist())

        self.save_data_to_file()
        self.log_message(">> Data updated and saved.")
