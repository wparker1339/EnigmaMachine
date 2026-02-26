"""Tkinter GUI for a simplified Enigma Machine."""
import platform

import string
import tkinter as tk

PLATFORM = platform.system()

if PLATFORM == "Darwin":
    from tkmacosx import Button
else:
    from tkinter import Button

from enigma.enigma import Enigma

ALPHABET = string.ascii_uppercase

# Enigma keyboard / lightboard layout  (9 + 8 + 9 = 26 keys)
KEY_ROWS = [
    list("QWERTZUIO"),
    list("ASDFGHJK"),
    list("PYXCVBNML"),
]

HOLD_MS = 500   # how long each key/light stays lit
GAP_MS  = 150   # pause between letters


class EnigmaUI:
    def __init__(self, root):
        self.machine = Enigma(1, 2, 3)
        self.root = root
        self.root.title("Enigma Machine Demo")

        # ── Rotor display ──────────────────────────────────────────
        tk.Label(root, text="Rotors", font=("Courier", 24)).pack(pady=(10, 0))
        self.rotor_frame = tk.Frame(root)
        self.rotor_frame.pack(pady=4)

        self.rotor_labels = []
        for _ in range(3):
            lbl = tk.Label(
                self.rotor_frame, text="A",
                font=("Courier", 24, "bold"), width=3,
                bg="#444444", fg="#ffff00", relief="ridge", bd=4
            )
            lbl.pack(side="left", padx=8)
            self.rotor_labels.append(lbl)

        # ── Lightboard ─────────────────────────────────────────────
        tk.Label(root, text="Lightboard", font=("Courier", 24)).pack(pady=(10, 0))
        lightboard_frame = tk.Frame(root)
        lightboard_frame.pack(pady=4)

        self.light_labels = {}          # letter -> Label
        for row in KEY_ROWS:
            row_frame = tk.Frame(lightboard_frame)
            row_frame.pack()
            for letter in row:
                lbl = tk.Label(
                    row_frame, text=letter,
                    font=("Courier", 20, "bold"),
                    width=3, height=1,
                    bg="#222222", fg="#555555", relief="flat"
                )
                lbl.pack(side="left", padx=3, pady=2)
                self.light_labels[letter] = lbl

        # ── Input ──────────────────────────────────────────────────
        tk.Label(root, text="Input Message", font=("Courier", 24),).pack(pady=(10, 0))
        self.input_box = tk.Entry(root, width=50)
        self.input_box.pack()

        self.encrypt_btn = Button(
            root, text="Encrypt", command=self.start_encryption
        )

        self.encrypt_btn.pack(pady=5)
        Button(
            root, text="Reset Rotors", command=self.reset_machine
        ).pack(pady=5)

        # ── Keyboard ───────────────────────────────────────────────
        tk.Label(root, text="Keyboard", font=("Courier", 24)).pack(pady=(10, 0))
        keyboard_frame = tk.Frame(root)
        keyboard_frame.pack(pady=4)

        self.key_buttons = {}           # letter -> Button
        for row in KEY_ROWS:
            row_frame = tk.Frame(keyboard_frame)
            row_frame.pack()
            for letter in row:
                btn = Button(
                    row_frame, text=letter,
                    font=("Courier", 20, "bold"),
                    bg="#d4d0c8", fg="#1a1a1a",
                    width=50, height=25,
                    relief="raised", bd=3, state="disabled"
                )
                btn.pack(side="left", padx=3, pady=2)
                self.key_buttons[letter] = btn

        # ── Output ─────────────────────────────────────────────────
        tk.Label(root, text="Encrypted Output", font=("Courier", 24)).pack(pady=(10, 0))
        self.output_box = tk.Text(root, height=5, width=75)
        self.output_box.pack(pady=(0, 10))

        self.update_rotor_display()

    # ---------------------------------------------------------------
    # Rotor display
    # ---------------------------------------------------------------
    def update_rotor_display(self):
        self.rotor_labels[0]["text"] = self.machine.rotor3.get_letter()
        self.rotor_labels[1]["text"] = self.machine.rotor2.get_letter()
        self.rotor_labels[2]["text"] = self.machine.rotor1.get_letter()

    # ---------------------------------------------------------------
    # Animation helpers
    # ---------------------------------------------------------------
    def _light_key(self, letter):
        self.key_buttons[letter].config(bg="#ffff00", fg="#1a1a1a", relief="sunken")

    def _dim_key(self, letter):
        self.key_buttons[letter].config(bg="#d4d0c8", fg="#1a1a1a", relief="raised")

    def _light_lamp(self, letter):
        self.light_labels[letter].config(bg="#ffff00", fg="#1a1a1a")

    def _dim_lamp(self, letter):
        self.light_labels[letter].config(bg="#222222", fg="#555555")

    # ---------------------------------------------------------------
    # Step-through encryption
    # ---------------------------------------------------------------
    def start_encryption(self):
        text = self.input_box.get().upper()
        if not text:
            return
        self.output_box.delete("1.0", tk.END)
        self.encrypt_btn.config(state="disabled")   # prevent re-entry
        self._step_encrypt(text, 0)

    def _step_encrypt(self, text, index):
        """Process one character then schedule the next."""
        if index >= len(text):
            self.encrypt_btn.config(state="normal")  # re-enable when done
            return

        c = text[index]

        if c not in ALPHABET:
            # Pass non-alpha through immediately; move to next character
            self.output_box.insert(tk.END, c)
            self.root.after(GAP_MS, self._step_encrypt, text, index + 1)
            return

        # 1. Light up the keyboard key for this input letter
        self._light_key(c)

        # 2. Encrypt, advance rotors, light up lightboard
        encrypted = self.machine.encrypt_char(c)
        self.update_rotor_display()
        self._light_lamp(encrypted)

        # 3. Append encrypted character to output
        self.output_box.insert(tk.END, encrypted)

        # 4. After HOLD_MS, dim both key and lamp, then move to next letter
        def finish():
            self._dim_key(c)
            self._dim_lamp(encrypted)
            self.root.after(GAP_MS, self._step_encrypt, text, index + 1)

        self.root.after(HOLD_MS, finish)

    # ---------------------------------------------------------------
    # Reset
    # ---------------------------------------------------------------
    def reset_machine(self):
        self.machine.reset()
        self.update_rotor_display()
        self.output_box.delete("1.0", tk.END)