import tkinter as tk
from tkinter import messagebox
import string


# Function for Frequency Analysis
def frequency_analysis(ciphertext):
    frequency = {}
    for letter in ciphertext:
        if letter.isalpha():
            letter = letter.lower()
            frequency[letter] = frequency.get(letter, 0) + 1
    most_frequent = sorted(frequency, key=frequency.get, reverse=True)
    return most_frequent[:3]  # Return top 3 letters


# Function for Shift Detection
def shift_detection(most_frequent_letter):
    position_e = ord('e') - ord('a')
    position_most_frequent = ord(most_frequent_letter) - ord('a')
    shift = (position_most_frequent - position_e) % 26
    return shift


# Function for Decryption
def decrypt_caesar_cipher(ciphertext, shift):
    decrypted_text = ""
    for letter in ciphertext:
        if letter.isalpha():
            shifted = ord(letter) - shift
            if letter.islower():
                if shifted < ord('a'):
                    shifted += 26
            elif letter.isupper():
                if shifted < ord('A'):
                    shifted += 26
            decrypted_letter = chr(shifted)
        else:
            decrypted_letter = letter
        decrypted_text += decrypted_letter
    return decrypted_text


# Function for Likelihood Estimation
def likelihood_estimation(decrypted_text):
    # English letter frequency (normalized)
    english_freq = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97,
                    'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25,
                    'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36,
                    'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.49,
                    'v': 0.98, 'k': 0.77, 'x': 0.15, 'j': 0.15, 'q': 0.10, 'z': 0.07}
    # Count letters in decrypted text
    total_letters = sum(letter.isalpha() for letter in decrypted_text)
    frequency = {letter: decrypted_text.lower().count(letter) * 100 / total_letters
                 for letter in string.ascii_lowercase}
    # Frequency match score
    frequency_match_score = sum(min(frequency.get(letter, 0), english_freq.get(letter, 0))
                                for letter in string.ascii_lowercase)
    # Common words presence
    common_words = ['the', 'of', 'and', 'to', 'in', 'a', 'is', 'that', 'for', 'it']
    common_word_score = sum(decrypted_text.lower().count(word) for word in common_words)
    # Overall likelihood (considering both frequency match and common words, with some weighting)
    likelihood_percentage = (frequency_match_score * 0.7) + (common_word_score * 0.3)
    return min(100, likelihood_percentage)  # Ensure it doesn't exceed 100%


# GUI Functions
def decrypt_and_display():
    ciphertext = text_input.get("1.0", "end-1c")
    if not ciphertext:
        messagebox.showinfo("Error", "Please enter ciphertext")
        return

    most_frequent_letters = frequency_analysis(ciphertext)
    results = []

    for letter in most_frequent_letters:
        shift = shift_detection(letter)
        decrypted_text = decrypt_caesar_cipher(ciphertext, shift)
        likelihood_score = likelihood_estimation(decrypted_text)
        results.append((decrypted_text, likelihood_score))

    result_label.config(text="\n".join(f"Decrypted Text: {res[0]}\nLikelihood Score: {res[1]}" for res in results))
# Setting up the window
root = tk.Tk()
root.title("Caesar Cipher Decryption Tool")
# Text input
text_input_label = tk.Label(root, text="Enter Ciphertext:")
text_input_label.pack()
text_input = tk.Text(root, height=5, width=50)
text_input.pack()
# Decrypt button
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_and_display)
decrypt_button.pack()
# Result label
result_label = tk.Label(root, text="")
result_label.pack()
# Run the application
root.mainloop()
