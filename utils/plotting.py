class Plotter:

    @staticmethod
    def plot_signal(
        ax, canvas, signal, title="Signal", xlabel="n", ylabel="Amplitude"
    ):
        ax.clear()
        markerline, stemlines, baseline = ax.stem(
            signal.indices, signal.values, label=signal.name
        )
        markerline.set_markerfacecolor("blue")
        markerline.set_markersize(6)

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.legend()
        canvas.draw()