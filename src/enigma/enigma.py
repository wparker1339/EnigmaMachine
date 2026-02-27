"""Code to represent the internals of a simplified Enigma Machine."""
from enigma.rotor import Rotor, ALPHABET

# Enigma rotor and reflector settings
WIRING = [
    {"letters": "PLACEHOLDER FOR INDEX 0", "turnover": "ZZZ"},          # Placeholder for index 0
    {"letters": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "turnover": "Q"},         # Rotor I
    {"letters": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "turnover": "E"},         # Rotor II
    {"letters": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "turnover": "V"},         # Rotor III
    {"letters": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "turnover": "J"},         # Rotor IV
    {"letters": "VZBRGITYUPSDNHLXAWMJQOFECK", "turnover": "Z"},         # Rotor V
    {"letters": "JPGVOUMFYQBENHZRDKASXLICTW", "turnover": ["Z", "M"]},  # Rotor VI
    {"letters": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "turnover": ["Z", "M"]},  # Rotor VII
    {"letters": "FKQHTLXOCBJSPDZRAMEWNIUYGV", "turnover": ["Z", "M"]}   # Rotor VIII
]
REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT"  # Reflector B only modeled


class Enigma:
    def __init__(self, rotor1: int, rotor2: int, rotor3: int):
        rotor_configs = [rotor1, rotor2, rotor3]
        self.rotors = []
        for rotor in rotor_configs:
            if rotor == 0:
                raise ValueError("Cannot index to 0 of the rotor wirings!")
            letters = WIRING[rotor]['letters']
            turnover = WIRING[rotor]['turnover']
            self.rotors.append(Rotor(letters, turnover))
        self.reflector = REFLECTOR

    def reset(self):
        for rotor in self.rotors:
            rotor.reset()

    def encrypt_char(self, c: str):
        if c not in ALPHABET:
            return c

        # Step the rotors (odometer carry)
        if self.rotors[0].step():
            if self.rotors[1].step():
                self.rotors[2].step()

        # Signal travels forward through all 3 rotors
        for rotor in self.rotors:
            c = rotor.encode_forward(c)

        # Hits the reflector — bounces back
        c = self.reflector[ALPHABET.index(c)]

        # Signal travels backward through all 3 rotors
        for rotor in reversed(self.rotors):
            c = rotor.encode_backward(c)

        return c