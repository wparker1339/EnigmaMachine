"""Code to represent the internals of a simplified Enigma Machine."""
# Enigma rotor and reflector settings
WIRING_I    = {"letters": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "turnover": "Y"}
WIRING_II   = {"letters": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "turnover": "M"}
WIRING_III  = {"letters": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "turnover": "V"}
WIRING_IV   = {"letters": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "turnover": "J"}
WIRING_V    = {"letters": "VZBRGITYUPSDNHLXAWMJQOFECK", "turnover": "Z"}
WIRING_VI   = {"letters": "JPGVOUMFYQBENHZRDKASXLICTW", "turnover": ["Z", "M"]}
WIRING_VII  = {"letters": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "turnover": ["Z", "M"]}
WIRING_VIII = {"letters": "FKQHTLXOCBJSPDZRAMEWNIUYGV", "turnover": ["Z", "M"]}
REFLECTOR   = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


class Enigma:
    def __init__(self, rotor1: int, rotor2: int, rotor3: int):
        pass