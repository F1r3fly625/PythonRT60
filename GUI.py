import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import main  # Import the main processing code

class AudioVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Visualizer")
        self.root.geometry("800x600")

        # Initialize default values
        self.filename = "16bit4chan.wav"  # Default file
        self.samplerate, self.data, self.time = self.load_audio(self.filename)
        self.graph_mode = "Waveform"  # Default graph

        # Create GUI components
        self.create_widgets()

        # Display initial graphs
        self.update_graph()

    def load_audio(self, filename):
        """Loads and processes an audio file."""
        if filename.endswith(".mp3"):
            wav_file = filename.replace(".mp3", ".wav")
            AudioSegment.from_mp3(filename).export(wav_file, format="wav")
            filename = wav_file

        samplerate, data = main.wavfile.read(filename)
        if len(data.shape) == 2:
            left_channel = data[:, 0]
            right_channel = data[:, 1]
            data = (left_channel + right_channel) / 2
        time = np.linspace(0., len(data) / samplerate, len(data), endpoint=False)
        return samplerate, data, time

    def create_widgets(self):
        """Creates the GUI layout."""
        # Graph display area
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Dropdown menu for graph selection
        dropdown_frame = tk.Frame(self.root)
        dropdown_frame.pack(side=tk.TOP, fill=tk.X)

        graph_options = ["Waveform", "Low Frequency", "Mid Frequency", "High Frequency", "Combined Frequency"]
        self.graph_selector = ttk.Combobox(dropdown_frame, values=graph_options, state="readonly")
        self.graph_selector.set("Select Graph")
        self.graph_selector.pack(side=tk.LEFT, padx=10, pady=10)
        self.graph_selector.bind("<<ComboboxSelected>>", self.change_graph)

        # Load file button
        self.load_btn = ttk.Button(dropdown_frame, text="Load File", command=self.load_file)
        self.load_btn.pack(side=tk.RIGHT, padx=10)

    def change_graph(self, event):
        """Handles dropdown selection to change graph."""
        self.graph_mode = self.graph_selector.get()
        self.update_graph()

    def load_file(self):
        """Opens a file dialog and loads a new audio file."""
        filetypes = [
            ("WAV files", "*.wav"),
            ("MP3 files", "*.mp3"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(title="Open a File", initialdir="/", filetypes=filetypes)
        if filename:
            self.filename = filename
            self.samplerate, self.data, self.time = self.load_audio(filename)
            self.graph_mode = "Waveform"  # Reset to waveform view
            self.update_graph()

    def filter_data(self, lowcut, highcut):
        """Filters the audio data for the specified frequency range."""
        return main.filter(self.data, lowcut, highcut, self.samplerate)

    def update_graph(self):
        """Updates the graph based on the selected mode."""
        self.ax.clear()

        if self.graph_mode == "Waveform":
            self.ax.plot(self.time, self.data, label="Waveform", color="black")
            self.ax.set_title("Waveform")
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Amplitude")

        elif self.graph_mode in ["Low Frequency", "Mid Frequency", "High Frequency", "Combined Frequency"]:
            ranges = {
                "Low Frequency": (20, 200, "blue"),
                "Mid Frequency": (200, 2000, "green"),
                "High Frequency": (2000, 20000, "red")
            }

            if self.graph_mode == "Combined Frequency":
                for mode, (lowcut, highcut, color) in ranges.items():
                    filtered_data = self.filter_data(lowcut, highcut)
                    spectrum = np.abs(np.fft.fft(filtered_data))[:len(filtered_data)//2]
                    freqs = np.fft.fftfreq(len(filtered_data), d=1/self.samplerate)[:len(filtered_data)//2]
                    self.ax.plot(freqs, spectrum, label=f"{mode}", color=color)
                self.ax.set_title("Combined Frequency Spectrum")
            else:
                lowcut, highcut, color = ranges[self.graph_mode]
                filtered_data = self.filter_data(lowcut, highcut)
                spectrum = np.abs(np.fft.fft(filtered_data))[:len(filtered_data)//2]
                freqs = np.fft.fftfreq(len(filtered_data), d=1/self.samplerate)[:len(filtered_data)//2]
                self.ax.plot(freqs, spectrum, label=self.graph_mode, color=color)
                self.ax.set_title(f"{self.graph_mode} Spectrum")

            self.ax.set_xlabel("Frequency (Hz)")
            self.ax.set_ylabel("Amplitude")

        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioVisualizerApp(root)
    root.mainloop()
