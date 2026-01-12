import guesses
import words_api

class Words:
    def __init__(self):
        self.api = words_api.Api()
        self.word = self.api.populate_words()
        self.letters_in_word = list(self.word) # sadala vārdu pa burtiem
    
    def guessed(self, guesses_obj):
        # letters_guessed = self.letters_in_word.intersection(guesses_obj.guesses.made)
        # return letters_guessed == self.letters_in_word

        for char in self.word:
            if not guesses_obj.guessed(char):
                return False
            return True

    def progress(self, guesses_obj):
        progress_string = ""
        for char in self.word:
            if guesses_obj.guessed(char):
                progress_string += f"f {char} "
            else:
                progress_string += " _ "
            
        return progress_string