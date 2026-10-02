import os
from dsp.signal import Signal


class Reader(Signal):

    def __init__(self, indices, values, name="Signal"):
        super().__init__(indices, values, name)

    @staticmethod
    def read_signal(file_path):
        indices = []
        values = []

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.split()
                # Skip blank lines or single-number header lines
                if len(parts) < 2:
                    continue

                try:
                    indices.append(float(parts[0]))
                    values.append(float(parts[1]))
                except ValueError:
                    continue

        name = os.path.basename(file_path)
        return Reader(indices, values, name=name)