import tkinter as tk
from tkinter import messagebox
import os
# import unittest testing sequence allignment

# this program uses @staticmethod defines methods within class not needing access to or modifying class state. 
# overall benefit is to isolate and make use of not accessing class data unecessarily
# to run program be sure to install 
class SpellChecker:
    def __init__(self, master, dictionary_file):
        self.master = master
        self.master.title("Spell Checker")

        # Here we set up the layout for the GUI
        # Following mostly what was presented on PDF
        tk.Label(master, text="Enter Word:").pack()
        self.entry = tk.Entry(master)
        self.entry.pack()
        self.check_button = tk.Button(master, text="Check", command=self.on_check)
        self.check_button.pack()
        tk.Label(master, text="Suggestions:").pack()
        self.listbox = tk.Listbox(master)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Loads the dictionary file to be read
        self.dictionary = self.read_dictionary(dictionary_file)

    @staticmethod
    def read_dictionary(file_path):
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Dictionary file not found.") # Error checking
            return []
        with open(file_path, 'r') as file:
            return [line.strip().lower() for line in file if line.strip()]
        
    # Function alculates the penalty between two chars accordingly
    @staticmethod
    def penalty(a, b):
        vowels = 'aeiou'
        if a == b:
            return 0
        elif (a in vowels and b in vowels) or (a not in vowels and b not in vowels):
            return 1
        else:
            return 3

    # Implementation for the sequence alignment algorithm using dynamic programming (DP) 
    # to find the min penalty between two words. Using first_word and second_word as parameters.
    @staticmethod
    def sequence_alignment(first_word, second_word):
        n, m = len(first_word), len(second_word)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        
        for i in range(n + 1):
            dp[i][0] = i * 2
        for j in range(m + 1):
            dp[0][j] = j * 2
        
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                match = dp[i - 1][j - 1] + SpellChecker.penalty(first_word[i - 1], second_word[j - 1])
                delete = dp[i - 1][j] + 2
                insert = dp[i][j - 1] + 2
                dp[i][j] = min(match, delete, insert)
        
        return dp[n][m]

    # Here, function finds and returns the top 10 words from the dictionary that have the lowest penalty scores compared to the word inputted

    def find_suggestions(self, input_word):
        scores = [(self.sequence_alignment(input_word, word), word) for word in self.dictionary]
        scores.sort()
        return [word for score, word in scores[:10]]

    # Here, on_check reads the input word, finds suggestions, and updates our listbox with these suggestions
    def on_check(self):
        input_word = self.entry.get().lower() # Converting word received to lower case
        if input_word:
            suggestions = self.find_suggestions(input_word)
            self.listbox.delete(0, tk.END) # Essentialy clears the current contents of the listbox
            for suggestion in suggestions:
                self.listbox.insert(tk.END, suggestion)
        else:
            messagebox.showinfo("Error", "Please enter a word to check.") # More error checking

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellChecker(root, 'dictionary.txt')
    root.mainloop()
