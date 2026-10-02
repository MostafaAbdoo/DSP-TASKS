import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from dsp.reader import Reader
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from utils.plotting import Plotter


class DSPApp:

    def __init__(self, root):
        self.root = root
        self.root.title("DSP Signal Processing")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)

        self.signals = []
        self.create_gui()

    def create_gui(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        control_frame = ttk.Frame(self.root, padding=15)
        control_frame.grid(row=0, column=0, sticky="ns")

        title = ttk.Label(
            control_frame, text="DSP Signal Processing", font=("Arial", 16, "bold")
        )
        title.pack(pady=(0, 20))

        # Input Frame
        input_frame = ttk.LabelFrame(
            control_frame, text="Signal Input", padding=10
        )
        input_frame.pack(fill="x", pady=5)

        self.load_button = ttk.Button(
            input_frame, text="Load Signal", command=self.load_signal
        )
        self.load_button.pack(fill="x", pady=4)

        self.load_multiple_button = ttk.Button(
            input_frame,
            text="Load Multiple Signals",
            command=self.load_multiple_signals,
        )
        self.load_multiple_button.pack(fill="x", pady=4)

        ttk.Label(input_frame, text="Loaded Signals:").pack(
            anchor="w", pady=(10, 3)
        )

        self.signal_listbox = tk.Listbox(
            input_frame, height=7, width=28, selectmode=tk.EXTENDED
        )
        self.signal_listbox.pack(fill="x")

        # Operations Frame
        operations_frame = ttk.LabelFrame(
            control_frame, text="Operations", padding=10
        )
        operations_frame.pack(fill="x", pady=10)

        self.display_button = ttk.Button(
            operations_frame,
            text="Display Selected Signal",
            command=self.display_signal,
        )
        self.display_button.pack(fill="x", pady=3)

        self.add_button = ttk.Button(
            operations_frame, text="Add Signals", command=self.add_signals
        )
        self.add_button.pack(fill="x", pady=3)

        ttk.Label(operations_frame, text="Constant:").pack(
            anchor="w", pady=(10, 2)
        )
        self.constant_entry = ttk.Entry(operations_frame)
        self.constant_entry.pack(fill="x")

        self.multiply_button = ttk.Button(
            operations_frame,
            text="Multiply Signal",
            command=self.multiply_signal,
        )
        self.multiply_button.pack(fill="x", pady=3)

        self.subtract_button = ttk.Button(
            operations_frame,
            text="Subtract Signals",
            command=self.subtract_signals,
        )
        self.subtract_button.pack(fill="x", pady=3)

        ttk.Label(operations_frame, text="Shift (k):").pack(
            anchor="w", pady=(10, 2)
        )
        self.shift_entry = ttk.Entry(operations_frame)
        self.shift_entry.pack(fill="x")

        self.shift_button = ttk.Button(
            operations_frame,
            text="Delay / Advance",
            command=self.shift_signal,
        )
        self.shift_button.pack(fill="x", pady=3)

        self.fold_button = ttk.Button(
            operations_frame, text="Fold Signal", command=self.fold_signal
        )
        self.fold_button.pack(fill="x", pady=3)

        self.clear_button = ttk.Button(
            control_frame, text="Clear Plot", command=self.clear_plot
        )
        self.clear_button.pack(fill="x", pady=(15, 5))

        self.exit_button = ttk.Button(
            control_frame, text="Exit", command=self.root.destroy
        )
        self.exit_button.pack(fill="x")

        # Plot Frame
        plot_frame = ttk.Frame(self.root, padding=10)
        plot_frame.grid(row=0, column=1, sticky="nsew")
        plot_frame.rowconfigure(0, weight=1)
        plot_frame.columnconfigure(0, weight=1)

        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Signal")
        self.ax.set_xlabel("n")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def load_signal(self):
        file_path = filedialog.askopenfilename(
            title="Select Signal File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not file_path:
            return

        signal = Reader.read_signal(file_path)
        self.signals.append(signal)
        self.signal_listbox.insert(tk.END, signal.name)

    def load_multiple_signals(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Signal Files",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not file_paths:
            return

        for file_path in file_paths:
            signal = Reader.read_signal(file_path)
            self.signals.append(signal)
            self.signal_listbox.insert(tk.END, signal.name)

    def display_signal(self):
        selected_indices = self.signal_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning(
                "No Selection", "Please select a signal to display."
            )
            return

        selected_signal = self.signals[selected_indices[0]]
        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=selected_signal,
            title=selected_signal.name,
        )

    def add_signals(self):
        selected_indices = self.signal_listbox.curselection()
        if len(selected_indices) < 2:
            messagebox.showwarning(
                "Insufficient Selection",
                "Please select at least two signals to add.",
            )
            return

        result_signal = self.signals[selected_indices[0]]
        for idx in selected_indices[1:]:
            result_signal = result_signal.addition(self.signals[idx])

        # Save computed signal back to list and updated UI listbox
        self.signals.append(result_signal)
        self.signal_listbox.insert(tk.END, result_signal.name)

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
        )

    def multiply_signal(self):
        selected_indices = self.signal_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning(
                "No Selection", "Please select a signal to multiply."
            )
            return

        try:
            constant = float(self.constant_entry.get())
        except ValueError:
            messagebox.showwarning(
                "Invalid Constant", "Please enter a valid numeric constant."
            )
            return

        result_signal = self.signals[selected_indices[0]].multiply(constant)

        # Save computed signal back to list and updated UI listbox
        self.signals.append(result_signal)
        self.signal_listbox.insert(tk.END, result_signal.name)

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
        )

    def subtract_signals(self):
        selected_indices = self.signal_listbox.curselection()
        if len(selected_indices) < 2:
            messagebox.showwarning(
                "Insufficient Selection",
                "Please select two signals to subtract.",
            )
            return

        sig1 = self.signals[selected_indices[0]]
        sig2 = self.signals[selected_indices[1]]

        # EDITED: Fixed method call name to match dsp/signal.py (substract)
        result_signal = sig1.substract(sig2)

        # Save computed signal back to list and updated UI listbox
        self.signals.append(result_signal)
        self.signal_listbox.insert(tk.END, result_signal.name)

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
        )

    def shift_signal(self):
        selected_indices = self.signal_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning(
                "No Selection", "Please select a signal to shift."
            )
            return

        try:
            k = int(self.shift_entry.get())
        except ValueError:
            messagebox.showwarning(
                "Invalid Shift", "Please enter a valid integer for shift k."
            )
            return

        result_signal = self.signals[selected_indices[0]].shift_signal(k)

        # Save computed signal back to list and updated UI listbox
        self.signals.append(result_signal)
        self.signal_listbox.insert(tk.END, result_signal.name)

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
        )

    def fold_signal(self):
        selected_indices = self.signal_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning(
                "No Selection", "Please select a signal to fold."
            )
            return

        result_signal = self.signals[selected_indices[0]].fold()

        # Save computed signal back to list and updated UI listbox
        self.signals.append(result_signal)
        self.signal_listbox.insert(tk.END, result_signal.name)

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
        )

    def clear_plot(self):
        self.ax.clear()
        self.ax.set_title("Signal")
        self.ax.set_xlabel("n")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)
        self.canvas.draw()