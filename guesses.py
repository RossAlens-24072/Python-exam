class Guesses:
    def __init__(self):
        self.guesses_made = set()
    
    def guessed(self, letter):
       return letter in self.guesses_made
    
    def record(self, guess, word):
        self.guesses_made.add(guess)
        return guess in word
    
    def made(self):
        guesses_list = list(self.guesses_made)
        guesses_list.sort()
        return ";".join(guesses_list)