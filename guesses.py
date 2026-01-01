class Guesses:
    def __init__(self, max_tries=6, word_len=5):
        self.max_tries = max_tries
        self.word_len = word_len
        self.attempts = []          # saraksts, kurā glabāsies secīgi minējumi (vārdi)
        self.letter_status = {}     # pēc izvēles: burts -> "G/Y/_"

    def add_attempt(self, guess: str, required_prefix: str = ""): #requred_prefix nepieciešams, ja jānosaka, cik burti jau doti.
        guess = guess.strip().lower()

        if self.is_over():
            raise ValueError("No attempts left")

        # kļūda, ja minējums īsaks par 5 burtiem un sastāv no ne burtu simboliem.
        if len(guess) != self.word_len or not guess.isalpha():
            raise ValueError(f"Word consists of {self.word_len} letters")

        # Šo var nelikt. Kļūda, ja vārds nesākas ar atklātajiem sākuma burtiem
        if required_prefix and not guess.startswith(required_prefix):
            raise ValueError(f"Guess must start with: {required_prefix}")
        
        # Pievieno minējumu sarakstam.
        self.attempts.append(guess)

    def tries_left(self):
        return self.max_tries - len(self.attempts)

    def is_over(self):
        return len(self.attempts) >= self.max_tries