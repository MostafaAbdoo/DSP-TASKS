import numpy as np


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

    # ================================================================
    # TASK 2 - SINE GENERATION
    # ================================================================

    @staticmethod
    def sine_signal(amplitude, phase, frequency, sampling_frequency, duration):
     

        t = np.arange(
            0,
            duration,
            1 / sampling_frequency
        )

        values = amplitude * np.sin(
            2 * np.pi * frequency * t + phase
        )

        return Signal(
            indices=t,
            values=values,
            name=f"Sine({frequency}Hz)",
        )

    # ================================================================
    # TASK 2 - COSINE GENERATION
    # ================================================================

    @staticmethod
    def cosine_signal(amplitude, phase, frequency, sampling_frequency, duration):
        
        t = np.arange(
            0,
            duration,
            1 / sampling_frequency
        )

        values = amplitude * np.cos(
            2 * np.pi * frequency * t + phase
        )

        return Signal(
            indices=t,
            values=values,
            name=f"Cosine({frequency}Hz)",
        )
    # ================================================================
    # TASK 3 - Quantization
    # ================================================================

    def quantize(self, num_levels=None, num_bits=None):
        # input: number of levels or number of bits
        # output: quantized_signal ,error signal ,encoded_values
        # num_levels = 2 power num_bits
        if num_levels is None and num_bits is None:
            raise ValueError("must enter a number ")
        if num_bits is not None:
            num_levels = 2 ** num_bits
        else:
            num_bits=int(np.ceil(np.log2(num_levels)))
        min_value = min(self.values)
        max_value = max(self.values)
        delta =(max_value-min_value)/num_levels
        quantized_values = []
        error_values = []
        encoded_values = []
        for x in self.values:
            #determine interval index
            if x ==max_value:
                level_idx = num_levels-1
            else:
                level_idx = int((x-min_value)/delta)
            #midpoint
            q_value = min_value +(level_idx + 0.5)*delta

            quantized_values.append(q_value)
            error_values.append(q_value-x)

            #binary encoding
            binary_code =format(level_idx,f"0{num_bits}b")
            encoded_values.append(binary_code)

        quantized_signal=Signal(self.indices,quantized_values,name=f"Quantized({self.name},L={num_levels})")
        error_signal=Signal(self.indices,error_values,name=f"Quantization Error({self.name})")
        return  quantized_signal,error_signal,encoded_values
