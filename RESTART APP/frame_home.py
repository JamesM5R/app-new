import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from PIL import Image
import os


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="white")

        # Label for title
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")        
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "header1.png")), size=(500, 150))
        self.home_frame_large_image_label = ctk.CTkLabel(self, text="", image=self.large_test_image)
        self.home_frame_large_image_label.pack(padx=20, pady=10, side="top")

        # Add the plot to the frame
        self.add_plot()

        # Footer
        footer = ctk.CTkLabel(
            self,
            text="© 2024 Workspace Management Application. Capgemini Engineering.",
            font=("Arial", 10, "italic"),
            text_color="black",
            fg_color="white",
        )
        footer.pack(padx=20, pady=10, side="bottom", fill="x")

    def add_summary_card(self, data):
        # Calculate metrics
        last_week = data["WEEK"].max()
        total_absences = data["NB ABSENT"].sum()
        total_absence_percentage = data["absence"].mean()

        # Create a frame for the summary cards
        summary_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        summary_frame.pack(padx=20, pady=(10, 5), fill="x")

        # Left Card - Last Week
        last_week_frame = ctk.CTkFrame(summary_frame, fg_color="lightgray", corner_radius=10)
        last_week_frame.pack(side="left", padx=10, pady=5, expand=True, fill="both")
        last_week_label = ctk.CTkLabel(
            last_week_frame, 
            text=f"Last Week: {last_week}", 
            font=("Arial", 14, "bold"), 
            text_color="blue"
        )
        last_week_label.pack(padx=10, pady=10)

        # Center Card - Total Absences
        total_absences_frame = ctk.CTkFrame(summary_frame, fg_color="lightgray", corner_radius=10)
        total_absences_frame.pack(side="left", padx=10, pady=5, expand=True, fill="both")
        total_absences_label = ctk.CTkLabel(
            total_absences_frame, 
            text=f"Total Absences: {total_absences}", 
            font=("Arial", 14, "bold"), 
            text_color="red"
        )
        total_absences_label.pack(padx=10, pady=10)

        # Right Card - Avg Absence Percentage
        absence_percentage_frame = ctk.CTkFrame(summary_frame, fg_color="lightgray", corner_radius=10)
        absence_percentage_frame.pack(side="left", padx=10, pady=5, expand=True, fill="both")
        absence_percentage_label = ctk.CTkLabel(
            absence_percentage_frame, 
            text=f"Avg Absence (%): {total_absence_percentage:.2f}%", 
            font=("Arial", 14, "bold"), 
            text_color="purple"
        )
        absence_percentage_label.pack(padx=10, pady=10)

    def add_plot(self):
        # Load and process data
        file_path = "saved_data.xlsx"  # Update the path as needed

        try:
            # Load the data
            data = pd.read_excel(file_path)

            # Process WEEK: Remove "S" and convert to integers
            data["WEEK"] = data["WEEK"].str.replace("S", "").astype(int)

            # Process percentages: Remove "%" and convert to float
            data["Unplanned presence"] = data["Unplanned presence"].str.replace("%", "").astype(float)
            data["absence"] = data["absence"].str.replace("%", "").astype(float)

            # Reverse the data order by WEEK
            data = data.sort_values("WEEK", ascending=True)

            # Add summary card above the plot
            self.add_summary_card(data)

            # Define the size of the plot (width, height in inches)
            plot_width = 10
            plot_height = 8  # Adjust this value for height

            # Plotting
            fig = Figure(figsize=(plot_width, plot_height), dpi=100)
            ax1 = fig.add_subplot(111)

            # Bar plots
            bar_width = 0.25
            x = np.arange(len(data["WEEK"]))
            bars1 = ax1.bar(x - bar_width, data["Pplanifie"], width=bar_width, label="Pplanifie", color="blue")
            bars2 = ax1.bar(x, data["Npplanifie"], width=bar_width, label="Npplanifie", color="orange")
            bars3 = ax1.bar(x + bar_width, data["NB ABSENT"], width=bar_width, label="NB ABSENT", color="green")

            ax1.set_xlabel("WEEK")
            ax1.set_ylabel("Counts")
            ax1.set_title("Dual-Axis Combo Chart with Dynamic Data Labels")
            ax1.set_xticks(x)
            ax1.set_xticklabels(data["WEEK"])
            ax1.legend(loc="upper left")

            # Secondary Y-axis
            ax2 = ax1.twinx()
            line1, = ax2.plot(x, data["Unplanned presence"], label="Unplanned presence (%)", color="red", marker="o")
            line2, = ax2.plot(x, data["absence"], label="absence (%)", color="purple", marker="o")
            ax2.set_ylabel("Percentage (%)")
            ax2.legend(loc="upper right")

            # Embed plot in CustomTkinter frame
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(padx=20, pady=10, fill="both", expand=True)

            # Dynamic data label handling
            annot = ax1.annotate(
                "",
                xy=(0, 0),
                xytext=(10, 10),
                textcoords="offset points",
                bbox=dict(boxstyle="round", fc="w"),
                arrowprops=dict(arrowstyle="->"),
            )
            annot.set_visible(False)

            def update_annot(obj, text, x, y):
                """Update annotation position and text."""
                annot.xy = (x, y)
                annot.set_text(text)
                annot.get_bbox_patch().set_alpha(0.8)

            def hover(event):
                """Handle hover event."""
                visible = False
                # Check bars
                for bars in [bars1, bars2, bars3]:
                    for bar in bars:
                        if bar.contains(event)[0]:
                            value = bar.get_height()
                            update_annot(bar, f"{value}", bar.get_x() + bar.get_width() / 2, bar.get_height())
                            annot.set_visible(True)
                            visible = True
                # Check line points
                for line, label in zip([line1, line2], ["Unplanned presence", "absence"]):
                    if line.contains(event)[0]:
                        idx = line.contains(event)[1]["ind"][0]
                        x_val = x[idx]
                        y_val = line.get_ydata()[idx]
                        update_annot(line, f"{label}: {y_val:.2f}%", x_val, y_val)
                        annot.set_visible(True)
                        visible = True

                if not visible:
                    annot.set_visible(False)
                canvas.draw_idle()

            # Connect the hover event to the canvas
            canvas.mpl_connect("motion_notify_event", hover)

        except Exception as e:
            # Error handling
            error_label = ctk.CTkLabel(self, text=f"Error: {e}", text_color="red")
            error_label.pack(padx=20, pady=10)







