"""Class to represent a rotor on the simulated Enigma Machine."""
import string

ALPHABET = string.ascii_uppercase

class Rotor:
    def __init__(self, wiring: str, notch: str, position: int=0):
        self.wiring = wiring
        self.notch = notch
        self.position = position
        self.initial_position = position

    def get_letter(self):
        return ALPHABET[self.position]

    def reset(self):
        self.position = self.initial_position

    def step(self):
        self.position = (self.position + 1) % 26
        return self.position == ALPHABET.index(self.notch)

    def encode_forward(self, c):
        index = (ALPHABET.index(c) + self.position) % 26
        mapped = self.wiring[index]
        return ALPHABET[(ALPHABET.index(mapped) - self.position) % 26]

    def encode_backward(self, c):
        index = (ALPHABET.index(c) + self.position) % 26
        mapped_index = self.wiring.index(ALPHABET[index])
        return ALPHABET[(mapped_index - self.position) % 26]