import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.dashboard_label = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Arial", 20, "bold"),
            text_color=("dodgerblue", "blue2"),
        )
        self.dashboard_label.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        # Plot Frame
        self.plot_frame = ctk.CTkFrame(self, fg_color="white")
        self.plot_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Navigation Buttons
        self.prev_button = ctk.CTkButton(self, text="Back", command=self.show_previous_plot)
        self.prev_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.next_button = ctk.CTkButton(self, text="Next", command=self.show_next_plot)
        self.next_button.grid(row=2, column=0, padx=20, pady=10, sticky="e")

        # Initialize the current plot index
        self.current_plot_index = 0

        # Load the plot data (same for all pages)
        self.plot_data = self.load_plot_data()

        # Display the initial plot
        self.display_plot()

        footer = ctk.CTkLabel(
            self,
            text="© 2024 Workspace Management Application. Capgemini Engineering.",
            font=("Arial", 10, "italic"),
            text_color="black",
            fg_color="white",
        )
        footer.grid(row=10, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def load_plot_data(self):
        # Load data from 'saved_data.csv'
        file_path = 'saved_data.csv'  # Replace with your actual file path
        data = pd.read_csv(file_path)

        # Count occurrences of each combination of Category and Justificative
        category_justificative_counts = data.groupby(['Category', 'Justificative']).size().reset_index(name='Count')

        return category_justificative_counts

    def display_plot(self):
        # Clear existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Use the same plot data for all pages
        data = self.plot_data

        # Calculate total counts per Category
        category_totals = data.groupby('Category')['Count'].sum()

        # Prepare data for plotting
        categories = category_totals.index.tolist()
        justificatives = data['Justificative'].tolist()

        # Pie chart configuration
        outer_sizes = data['Count']
        inner_sizes = category_totals.values

        # Colors
        cmap = plt.get_cmap("tab20c")
        inner_colors = cmap(np.arange(len(categories)) * 4)
        outer_colors = cmap(np.repeat(np.arange(len(categories)), len(justificatives) // len(categories)))

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(10, 8))  # Adjusted figure size

        # Adjust space around the plot
        fig.subplots_adjust(left=0.1, right=0.75)  # Added space to the right for the legend

        # Inner pie (categories with percentages)
        wedges_inner, texts_inner, autotexts_inner = ax.pie(
            inner_sizes,
            radius=1,
            labels=None,  # No labels (only percentages)
            autopct=lambda pct: f"{pct:.1f}%",  # Percentages
            pctdistance=0.5,
            colors=inner_colors,
            wedgeprops=dict(width=0.3, edgecolor='w'),
            textprops=dict(color="black", fontsize=10),
        )

        # Outer pie (justificatives with labels and percentages)
        wedges_outer, texts_outer, autotexts_outer = ax.pie(
            outer_sizes,
            radius=1.3,
            labels=justificatives,
            autopct=lambda pct: f"{pct:.1f}%",
            pctdistance=0.85,
            colors=outer_colors,
            wedgeprops=dict(width=0.3, edgecolor='w'),
            textprops=dict(color="black", fontsize=8),
        )

        # Add legend for categories
        ax.legend(
            loc="center left",
            bbox_to_anchor=(1.05, 0.5),  # Adjusted position to the right
            labels=[f"{cat}" for cat in categories],
            title="Categories",
            fontsize=10,
            title_fontsize=12,
        )

        # Embed the plot into the tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas.draw()

        # Update button states based on current plot
        self.update_buttons()

    def update_buttons(self):
        if self.current_plot_index == 0:
            # First plot: Only Next is active
            self.next_button.configure(state="normal")
            self.prev_button.configure(state="disabled")
        elif self.current_plot_index == 2:
            # Last plot: Only Back is active
            self.prev_button.configure(state="normal")
            self.next_button.configure(state="disabled")
        else:
            # Middle plot: Both buttons are active
            self.prev_button.configure(state="normal")
            self.next_button.configure(state="normal")

    def show_next_plot(self):
        # Move to the next plot
        if self.current_plot_index < 2:  # Maximum 3 plots (0, 1, 2)
            self.current_plot_index += 1
            self.display_plot()

    def show_previous_plot(self):
        # Move to the previous plot
        if self.current_plot_index > 0:
            self.current_plot_index -= 1
            self.display_plot()