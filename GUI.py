import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import main  # Import the main module


class AudioVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Visualizer")

        # Initialize the audio data
        self.filename = "16bit2chan.wav"  # Default audio file
        self.samplerate, self.data, self.time = self.load_audio(self.filename)
        self.graph_mode = "low"  # Default graph to display

        # Create GUI components
        self.create_widgets()

        # Display initial graphs
        self.update_graphs()

    def load_audio(self, filename):
        """Loads audio file and processes it using main.py logic."""
        samplerate, data = main.wavfile.read(filename)

        if len(data.shape) == 2:
            left_channel = data[:, 0]
            right_channel = data[:, 1]
            data = (left_channel + right_channel) / 2
        time = np.linspace(0., len(data) / samplerate, len(data), endpoint=False)
        return samplerate, data, time

    def create_widgets(self):
        """Sets up the GUI layout."""
        # Graph area
        self.figure, self.ax = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.low_btn = tk.Button(btn_frame, text="Low Frequency", command=lambda: self.set_graph_mode("low"))
        self.low_btn.pack(side=tk.LEFT)

        self.mid_btn = tk.Button(btn_frame, text="Mid Frequency", command=lambda: self.set_graph_mode("mid"))
        self.mid_btn.pack(side=tk.LEFT)

        self.high_btn = tk.Button(btn_frame, text="High Frequency", command=lambda: self.set_graph_mode("high"))
        self.high_btn.pack(side=tk.LEFT)

        self.load_btn = tk.Button(btn_frame, text="Load File", command=self.load_file)
        self.load_btn.pack(side=tk.RIGHT)

    def set_graph_mode(self, mode):
        """Switches between low, mid, and high frequency graphs."""
        self.graph_mode = mode
        self.update_graphs()

    def load_file(self):
        """Opens a file dialog to select a new audio file."""
        filename = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if filename:
            self.filename = filename
            self.samplerate, self.data, self.time = self.load_audio(filename)
            self.update_graphs()

    def filter_data(self, lowcut, highcut):
        """Filters the audio data for the specified frequency range."""
        return main.filter(self.data, lowcut, highcut, self.samplerate)

    def update_graphs(self):
        """Updates the graphs based on the selected mode."""
        # Clear previous graphs
        self.ax[0].clear()
        self.ax[1].clear()

        # Frequency ranges
        ranges = {"low": (20, 200), "mid": (200, 2000), "high": (2000, 20000)}
        lowcut, highcut = ranges[self.graph_mode]

        # Filter data for the selected frequency range
        filtered_data = self.filter_data(lowcut, highcut)
        spectrum = np.abs(np.fft.fft(filtered_data))[:len(filtered_data) // 2]
        freqs = np.fft.fftfreq(len(filtered_data), d=1 / self.samplerate)[:len(filtered_data) // 2]

        # Plot the filtered frequency graph
        self.ax[0].plot(freqs, spectrum, label=f"{self.graph_mode.capitalize()} Frequency")
        self.ax[0].set_title("Frequency Spectrum")
        self.ax[0].set_xlabel("Frequency (Hz)")
        self.ax[0].set_ylabel("Amplitude")
        self.ax[0].legend()

        # Plot the waveform graph
        self.ax[1].plot(self.time, self.data, label="Waveform")
        self.ax[1].set_title("Waveform")
        self.ax[1].set_xlabel("Time (s)")
        self.ax[1].set_ylabel("Amplitude")
        self.ax[1].legend()

        # Redraw the canvas
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioVisualizerApp(root)
    root.mainloop()
