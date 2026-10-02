class Signal:

    def __init__(self, indices, values, name="Signal"):
        self.indices = list(indices)
        self.values = list(values)
        self.name = name

    def addition(self, other_signal):
        # Align indices by finding the union of index ranges
        combined = {}
        for idx, val in zip(self.indices, self.values):
            combined[idx] = combined.get(idx, 0.0) + val
        for idx, val in zip(other_signal.indices, other_signal.values):
            combined[idx] = combined.get(idx, 0.0) + val

        sorted_indices = sorted(combined.keys())
        new_values = [combined[i] for i in sorted_indices]
        return Signal(
            indices=sorted_indices,
            values=new_values,
            name=f"({self.name} + {other_signal.name})",
        )

    def multiply(self, constant):
        new_values = [value * constant for value in self.values]
        return Signal(
            indices=self.indices,
            values=new_values,
            name=f"({self.name} * {constant})",
        )

    def substract(self, other_signal):
        # Subtracting is adding the negated signal
        negated = other_signal.multiply(-1)
        res = self.addition(negated)
        res.name = f"({self.name} - {other_signal.name})"
        return res

    def shift_signal(self, k):
        # Delay (k > 0) shifts signal right: n -> n + k
        # Advance (k < 0) shifts signal left: n -> n + k
        shifted_indices = [index + k for index in self.indices]
        return Signal(
            indices=shifted_indices,
            values=self.values,
            name=f"Shifted({self.name}, {k})",
        )

    def fold(self):
        # Fold negates the indices: x(-n)
        # Reversing indices and values keeps the indices sorted
        folded_indices = [-index for index in reversed(self.indices)]
        folded_values = list(reversed(self.values))
        return Signal(
            indices=folded_indices,
            values=folded_values,
            name=f"Folded({self.name})",
        )