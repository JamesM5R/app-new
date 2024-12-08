import customtkinter as ctk
import pandas as pd
import random
import time
from threading import Thread
import tkinter.messagebox as messagebox

# Initialize app theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CANLoggerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CAN Diagnostic Logger")
        self.geometry("600x400")

        # Data storage
        self.data = []
        self.file_name = "can_data.csv"

        # UI Components
        self.setup_ui()

        # Start CAN simulation in a background thread
        self.running = True
        Thread(target=self.simulate_can_messages, daemon=True).start()

    def setup_ui(self):
        # Table for displaying CAN data
        self.table = ctk.CTkTextbox(self, width=500, height=250)
        self.table.pack(pady=10)

        # Start/Stop button
        self.start_button = ctk.CTkButton(self, text="Start Logging", command=self.start_logging)
        self.start_button.pack(pady=5)

        self.stop_button = ctk.CTkButton(self, text="Stop Logging", command=self.stop_logging)
        self.stop_button.pack(pady=5)

    def simulate_can_messages(self):
        can_ids = {
            "0x100": "Engine Speed",
            "0x101": "Temperature",
            "0x102": "Vehicle Speed"
        }
        thresholds = {"Engine Speed": 4000, "Temperature": 100, "Vehicle Speed": 120}

        while self.running:
            for can_id, signal_name in can_ids.items():
                value = random.randint(0, 5000) if "Speed" in signal_name else random.randint(0, 120)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                # Check for anomalies
                warning = value > thresholds.get(signal_name, float('inf'))
                entry = f"{timestamp} | {can_id} | {signal_name} | {value} {'(Warning!)' if warning else ''}\n"

                # Update table
                self.table.insert("0.0", entry)

                # Log to data
                self.data.append({"Timestamp": timestamp, "CAN ID": can_id, "Signal": signal_name, "Value": value, "Warning": warning})
                time.sleep(0.5)

    def start_logging(self):
        # Save to CSV
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_csv(self.file_name, index=False)
            messagebox.showinfo(title="Logging Saved", message=f"Data logged to {self.file_name}")

    def stop_logging(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = CANLoggerApp()
    app.mainloop()
