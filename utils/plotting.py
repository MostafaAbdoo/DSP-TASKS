import random


def plot_discrete_signal(ax, signal, color):
    """Helper function to plot discrete stem signals."""
    markerline, stemlines, baseline = ax.stem(
        signal.indices,
        signal.values,
        label=signal.name
    )

    markerline.set_markerfacecolor(color)
    markerline.set_markeredgecolor(color)
    stemlines.set_color(color)
    markerline.set_markersize(6)


def plot_continuous_signal(ax, signal, color):
    """Helper function to plot continuous line signals."""
    ax.plot(
        signal.indices,
        signal.values,
        label=signal.name,
        color=color,
        linewidth=2
    )


class Plotter:

    @staticmethod
    def plot_signal(
        ax,
        canvas,
        signal,
        title="Signal",
        xlabel="n",
        ylabel="Amplitude",
        signal_type="Discrete",
        clear=True
    ):

        if clear:
            ax.clear()

        # Generate a random color
        random_color = f"#{random.randint(0, 0xFFFFFF):06x}"

        # Plot according to the selected representation
        if signal_type.strip().lower() == "discrete":

            plot_discrete_signal(
                ax,
                signal,
                random_color
            )

        elif signal_type.strip().lower() == "continuous":

            plot_continuous_signal(
                ax,
                signal,
                random_color
            )

        else:
            raise ValueError(
                "signal_type must be either 'Discrete' or 'Continuous'"
            )

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.legend()

        canvas.draw()