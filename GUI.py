import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import main  # Import the main processing code


class AudioVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Visualizer")
        self.audio_file = None
        self.samplerate = None
        self.data = None
        self.time = None

        # State to track current frequency plot
        self.current_frequency = "Low Frequency"

        # Create UI components
        self.create_ui()

    def create_ui(self):
        """Sets up the UI components."""
        # Create file open button
        open_button = ttk.Button(self.root, text="Open File", command=self.select_file)
        open_button.pack(pady=10)

        # Create frequency toggle button
        self.toggle_button = ttk.Button(self.root, text="Show Mid Frequency", command=self.toggle_frequency)
        self.toggle_button.pack(pady=10)

        # Create matplotlib figure and canvas
        self.figure, (self.ax_waveform, self.ax_frequency) = plt.subplots(2, 1, figsize=(8, 6))
        self.figure.tight_layout(pad=4)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def select_file(self):
        """Opens a file dialog to select an audio file."""
        filetypes = (("Audio files", "*.wav *.mp3"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Open a file", initialdir="/", filetypes=filetypes)

        if filename:  # If a file is selected
            self.audio_file = filename
            self.samplerate, self.data, self.time = main.process_file(filename)
            self.update_plots()

    def toggle_frequency(self):
        """Cycles through Low, Mid, High, and Combined Frequency plots."""
        if self.current_frequency == "Low Frequency":
            self.current_frequency = "Mid Frequency"
            self.toggle_button.config(text="Show High Frequency")
        elif self.current_frequency == "Mid Frequency":
            self.current_frequency = "High Frequency"
            self.toggle_button.config(text="Show Combined Frequency")
        elif self.current_frequency == "High Frequency":
            self.current_frequency = "Combined Frequency"
            self.toggle_button.config(text="Show Low Frequency")
        else:  # Combined Frequency
            self.current_frequency = "Low Frequency"
            self.toggle_button.config(text="Show Mid Frequency")

        self.update_plots()

    def update_plots(self):
        """Updates the waveform and frequency plots based on the current state."""
        if not self.audio_file:
            return  # Do nothing if no file is loaded

        # Clear axes
        self.ax_waveform.clear()
        self.ax_frequency.clear()

        # Draw the waveform (always visible)
        self.ax_waveform.plot(self.time, self.data, color="black")
        self.ax_waveform.set_title("Waveform")
        self.ax_waveform.set_xlabel("Time (s)")
        self.ax_waveform.set_ylabel("Amplitude")

        # Draw the current frequency plot
        freqs, spectrum = main.calculate_spectrum(self.data, self.samplerate)

        if self.current_frequency == "Low Frequency":
            low_spectrum = main.filter(spectrum, 20, 250, self.samplerate)
            self.ax_frequency.plot(freqs, low_spectrum, color="blue", label="Low Frequency")
        elif self.current_frequency == "Mid Frequency":
            mid_spectrum = main.filter(spectrum, 250, 2000, self.samplerate)
            self.ax_frequency.plot(freqs, mid_spectrum, color="green", label="Mid Frequency")
        elif self.current_frequency == "High Frequency":
            high_spectrum = main.filter(spectrum, 2000, 20000, self.samplerate)
            self.ax_frequency.plot(freqs, high_spectrum, color="red", label="High Frequency")
        elif self.current_frequency == "Combined Frequency":
            self.ax_frequency.plot(freqs, spectrum, color="purple", label="Combined Frequency")

        self.ax_frequency.set_title(f"{self.current_frequency}")
        self.ax_frequency.set_xlabel("Frequency (Hz)")
        self.ax_frequency.set_ylabel("Amplitude")
        self.ax_frequency.legend()

        # Redraw the canvas
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioVisualizerApp(root)
    root.mainloop()
