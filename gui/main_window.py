import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from dsp.reader import Reader
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from utils.plotting import Plotter
from dsp.signal import Signal


class DSPApp:

    def __init__(self, root):
        self.root = root
        self.root.title("DSP Signal Processing")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)

        self.signals = []


        self.display_mode = tk.StringVar(value="Discrete")

        self.create_gui()

    def create_gui(self):

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)


        menu_bar = tk.Menu(self.root)

        signal_generation_menu = tk.Menu(
            menu_bar,
            tearoff=0
        )

        signal_generation_menu.add_command(
            label="Sine Wave",
            command=self.open_sine_generation
        )

        signal_generation_menu.add_command(
            label="Cosine Wave",
            command=self.open_cosine_generation
        )

        menu_bar.add_cascade(
            label="Signal Generation",
            menu=signal_generation_menu
        )

        self.root.config(menu=menu_bar)


        control_frame = ttk.Frame(
            self.root,
            padding=15
        )

        control_frame.grid(
            row=0,
            column=0,
            sticky="ns"
        )


        title = ttk.Label(
            control_frame,
            text="DSP Signal Processing",
            font=("Arial", 16, "bold")
        )

        title.pack(
            pady=(0, 20)
        )


        input_frame = ttk.LabelFrame(
            control_frame,
            text="Signal Input",
            padding=10
        )

        input_frame.pack(
            fill="x",
            pady=5
        )

        self.load_button = ttk.Button(
            input_frame,
            text="Load Signal",
            command=self.load_signal
        )

        self.load_button.pack(
            fill="x",
            pady=4
        )

        self.load_multiple_button = ttk.Button(
            input_frame,
            text="Load Multiple Signals",
            command=self.load_multiple_signals
        )

        self.load_multiple_button.pack(
            fill="x",
            pady=4
        )

        ttk.Label(
            input_frame,
            text="Loaded Signals:"
        ).pack(
            anchor="w",
            pady=(10, 3)
        )

        self.signal_listbox = tk.Listbox(
            input_frame,
            height=7,
            width=28,
            selectmode=tk.EXTENDED
        )

        self.signal_listbox.pack(
            fill="x"
        )


        display_frame = ttk.LabelFrame(
            control_frame,
            text="Display Representation",
            padding=10
        )

        display_frame.pack(
            fill="x",
            pady=10
        )

        self.discrete_radio = ttk.Radiobutton(
            display_frame,
            text="Discrete",
            variable=self.display_mode,
            value="Discrete"
        )

        self.discrete_radio.pack(
            anchor="w",
            pady=2
        )

        self.continuous_radio = ttk.Radiobutton(
            display_frame,
            text="Continuous",
            variable=self.display_mode,
            value="Continuous"
        )

        self.continuous_radio.pack(
            anchor="w",
            pady=2
        )


        operations_frame = ttk.LabelFrame(
            control_frame,
            text="Operations",
            padding=10
        )

        operations_frame.pack(
            fill="x",
            pady=10
        )


        self.display_button = ttk.Button(
            operations_frame,
            text="Display Selected Signal",
            command=self.display_signal
        )

        self.display_button.pack(
            fill="x",
            pady=3
        )


        self.add_button = ttk.Button(
            operations_frame,
            text="Add Signals",
            command=self.add_signals
        )

        self.add_button.pack(
            fill="x",
            pady=3
        )


        ttk.Label(
            operations_frame,
            text="Constant:"
        ).pack(
            anchor="w",
            pady=(10, 2)
        )

        self.constant_entry = ttk.Entry(
            operations_frame
        )

        self.constant_entry.pack(
            fill="x"
        )

        self.multiply_button = ttk.Button(
            operations_frame,
            text="Multiply Signal",
            command=self.multiply_signal
        )

        self.multiply_button.pack(
            fill="x",
            pady=3
        )


        self.subtract_button = ttk.Button(
            operations_frame,
            text="Subtract Signals",
            command=self.subtract_signals
        )

        self.subtract_button.pack(
            fill="x",
            pady=3
        )


        ttk.Label(
            operations_frame,
            text="Shift (k):"
        ).pack(
            anchor="w",
            pady=(10, 2)
        )

        self.shift_entry = ttk.Entry(
            operations_frame
        )

        self.shift_entry.pack(
            fill="x"
        )

        self.shift_button = ttk.Button(
            operations_frame,
            text="Delay / Advance",
            command=self.shift_signal
        )

        self.shift_button.pack(
            fill="x",
            pady=3
        )


        self.fold_button = ttk.Button(
            operations_frame,
            text="Fold Signal",
            command=self.fold_signal
        )

        self.fold_button.pack(
            fill="x",
            pady=3
        )


        self.clear_button = ttk.Button(
            control_frame,
            text="Clear Plot",
            command=self.clear_plot
        )

        self.clear_button.pack(
            fill="x",
            pady=(15, 5)
        )


        self.exit_button = ttk.Button(
            control_frame,
            text="Exit",
            command=self.root.destroy
        )

        self.exit_button.pack(
            fill="x"
        )

        plot_frame = ttk.Frame(
            self.root,
            padding=10
        )

        plot_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        plot_frame.rowconfigure(
            0,
            weight=1
        )

        plot_frame.columnconfigure(
            0,
            weight=1
        )

        self.figure = Figure(
            figsize=(8, 6),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)

        self.ax.set_title(
            "Signal"
        )

        self.ax.set_xlabel(
            "n"
        )

        self.ax.set_ylabel(
            "Amplitude"
        )

        self.ax.grid(
            True
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=plot_frame
        )

        self.canvas.get_tk_widget().grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # ================================================================
    # TASK 1 - LOAD SIGNAL
    # ================================================================

    def load_signal(self):

        file_path = filedialog.askopenfilename(
            title="Select Signal File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        signal = Reader.read_signal(file_path)

        self.signals.append(signal)

        self.signal_listbox.insert(
            tk.END,
            signal.name
        )

    # ================================================================
    # TASK 1 - LOAD MULTIPLE SIGNALS
    # ================================================================

    def load_multiple_signals(self):

        file_paths = filedialog.askopenfilenames(
            title="Select Signal Files",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if not file_paths:
            return

        for file_path in file_paths:

            signal = Reader.read_signal(file_path)

            self.signals.append(signal)

            self.signal_listbox.insert(
                tk.END,
                signal.name
            )

    # ================================================================
    # TASK 1 + TASK 2 - DISPLAY SIGNAL
    # ================================================================

    def display_signal(self):

        selected_indices = self.signal_listbox.curselection()

        if not selected_indices:

            messagebox.showwarning(
                "No Selection",
                "Please select one or two signals."
            )

            return


        if len(selected_indices) > 2:

            messagebox.showwarning(
                "Too Many Signals",
                "Please select a maximum of two signals."
            )

            return

        selected_signals = [
            self.signals[index]
            for index in selected_indices
        ]

        # Clear once before displaying the selected signals
        self.ax.clear()

        # Display selected signals
        for signal in selected_signals:

            Plotter.plot_signal(
                ax=self.ax,
                canvas=self.canvas,
                signal=signal,
                title="Signals",
                signal_type=self.display_mode.get(),
                clear=False
            )

        self.ax.set_title("Signal")
        self.ax.set_xlabel("n")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)
        self.ax.legend()

        self.canvas.draw()

    # ================================================================
    # TASK 1 - ADD SIGNALS
    # ================================================================

    def add_signals(self):

        selected_indices = self.signal_listbox.curselection()

        if len(selected_indices) < 2:

            messagebox.showwarning(
                "Insufficient Selection",
                "Please select at least two signals to add."
            )

            return

        result_signal = self.signals[
            selected_indices[0]
        ]

        for idx in selected_indices[1:]:

            result_signal = result_signal.addition(
                self.signals[idx]
            )

        self.signals.append(
            result_signal
        )

        self.signal_listbox.insert(
            tk.END,
            result_signal.name
        )

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
            signal_type=self.display_mode.get()
        )

    # ================================================================
    # TASK 1 - MULTIPLY SIGNAL
    # ================================================================

    def multiply_signal(self):

        selected_indices = self.signal_listbox.curselection()

        if not selected_indices:

            messagebox.showwarning(
                "No Selection",
                "Please select a signal to multiply."
            )

            return

        try:

            constant = float(
                self.constant_entry.get()
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Constant",
                "Please enter a valid numeric constant."
            )

            return

        result_signal = self.signals[
            selected_indices[0]
        ].multiply(constant)

        self.signals.append(
            result_signal
        )

        self.signal_listbox.insert(
            tk.END,
            result_signal.name
        )

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
            signal_type=self.display_mode.get()
        )

    # ================================================================
    # TASK 1 - SUBTRACT SIGNALS
    # ================================================================

    def subtract_signals(self):

        selected_indices = self.signal_listbox.curselection()

        if len(selected_indices) < 2:

            messagebox.showwarning(
                "Insufficient Selection",
                "Please select two signals to subtract."
            )

            return

        sig1 = self.signals[
            selected_indices[0]
        ]

        sig2 = self.signals[
            selected_indices[1]
        ]

        # EDITED:
        # Fixed method call name to match dsp/signal.py
        result_signal = sig1.substract(sig2)

        self.signals.append(
            result_signal
        )

        self.signal_listbox.insert(
            tk.END,
            result_signal.name
        )

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
            signal_type=self.display_mode.get()
        )

    # ================================================================
    # TASK 1 - SHIFT SIGNAL
    # ================================================================

    def shift_signal(self):

        selected_indices = self.signal_listbox.curselection()

        if not selected_indices:

            messagebox.showwarning(
                "No Selection",
                "Please select a signal to shift."
            )

            return

        try:

            k = int(
                self.shift_entry.get()
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Shift",
                "Please enter a valid integer for shift k."
            )

            return

        result_signal = self.signals[
            selected_indices[0]
        ].shift_signal(k)

        self.signals.append(
            result_signal
        )

        self.signal_listbox.insert(
            tk.END,
            result_signal.name
        )

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
            signal_type=self.display_mode.get()
        )

    # ================================================================
    # TASK 1 - FOLD SIGNAL
    # ================================================================

    def fold_signal(self):

        selected_indices = self.signal_listbox.curselection()

        if not selected_indices:

            messagebox.showwarning(
                "No Selection",
                "Please select a signal to fold."
            )

            return

        result_signal = self.signals[
            selected_indices[0]
        ].fold()

        self.signals.append(
            result_signal
        )

        self.signal_listbox.insert(
            tk.END,
            result_signal.name
        )

        Plotter.plot_signal(
            ax=self.ax,
            canvas=self.canvas,
            signal=result_signal,
            title=result_signal.name,
            signal_type=self.display_mode.get()
        )


    def open_sine_generation(self):

        self.open_generation_window(
            "Sine"
        )


    def open_cosine_generation(self):

        self.open_generation_window(
            "Cosine"
        )



    def open_generation_window(self, signal_type):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            f"Generate {signal_type} Wave"
        )

        window.geometry(
            "400x500"
        )

        window.resizable(
            False,
            False
        )


        ttk.Label(
            window,
            text="Signal Generation",
            font=("Arial", 15, "bold")
        ).pack(
            pady=(15, 5)
        )



        type_frame = ttk.LabelFrame(
            window,
            text="Signal Type",
            padding=10
        )

        type_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        signal_type_var = tk.StringVar(
            value=signal_type
        )

        ttk.Radiobutton(
            type_frame,
            text="Sine",
            variable=signal_type_var,
            value="Sine"
        ).pack(
            side="left",
            padx=30
        )

        ttk.Radiobutton(
            type_frame,
            text="Cosine",
            variable=signal_type_var,
            value="Cosine"
        ).pack(
            side="left",
            padx=30
        )



        ttk.Label(
            window,
            text="Amplitude (A):"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 3)
        )

        amplitude_entry = ttk.Entry(
            window
        )

        amplitude_entry.pack(
            fill="x",
            padx=20
        )


        ttk.Label(
            window,
            text="Phase Shift (θ) in radians:"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 3)
        )

        phase_entry = ttk.Entry(
            window
        )

        phase_entry.pack(
            fill="x",
            padx=20
        )


        ttk.Label(
            window,
            text="Analog Frequency (F) Hz:"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 3)
        )

        frequency_entry = ttk.Entry(
            window
        )

        frequency_entry.pack(
            fill="x",
            padx=20
        )


        ttk.Label(
            window,
            text="Sampling Frequency (Fs) Hz:"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 3)
        )

        sampling_frequency_entry = ttk.Entry(
            window
        )

        sampling_frequency_entry.pack(
            fill="x",
            padx=20
        )

        # ============================================================
        # GENERATE BUTTON
        # ============================================================

        def generate():


            try:

                a = float(
                    amplitude_entry.get()
                )

                theta = float(
                    phase_entry.get()
                )

                f = float(
                    frequency_entry.get()
                )

                fs = float(
                    sampling_frequency_entry.get()
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Input",
                    "Please enter valid numeric values."
                )

                return


            if fs < 2 * f:

                messagebox.showerror(
                    "Sampling Theorem Violation",
                    "Sampling frequency Fs must be at least twice the analog frequency F."
                )

                return


            selected_type = signal_type_var.get()

            if selected_type == "Sine":

                signal = Signal.sine_signal(
                    amplitude=a,
                    phase=theta,
                    frequency=f,
                    sampling_frequency=fs,
                    duration=1
                )

            elif selected_type == "Cosine":

                signal = Signal.cosine_signal(
                    amplitude=a,
                    phase=theta,
                    frequency=f,
                    sampling_frequency=fs,
                    duration=1
                )

            self.signals.append(
                signal
            )

            self.signal_listbox.insert(
                tk.END,
                signal.name
            )

            Plotter.plot_signal(
                ax=self.ax,
                canvas=self.canvas,
                signal=signal,
                title=signal.name,
                signal_type=self.display_mode.get()
            )

            window.destroy()

        ttk.Button(
            window,
            text="Generate",
            command=generate
        ).pack(
            pady=25
        )


    def clear_plot(self):

        self.ax.clear()

        self.ax.set_title(
            "Signal"
        )

        self.ax.set_xlabel(
            "n"
        )

        self.ax.set_ylabel(
            "Amplitude"
        )

        self.ax.grid(
            True
        )

        self.canvas.draw()