class Guesses:
    """Klase glabā spēlētāja minējumus un maksimālo mēģinājumu limitu"""
    def __init__(self, max_tries=6, word_len=5):
        """ Funkcija inicializē klasi Guesses"""
        self.max_tries = max_tries
        self.word_len = word_len
        self.attempts = []        
        self.letter_status = {} 

    def add_attempt(self, guess: str, required_prefix: str = ""):
        """ Funkcija pievieno jaunu minējumu"""
        guess = guess.strip().lower()

        # Ja atļautie mēģinājumi ir beigušies, jaunu minējumu nevar pievienot
        if self.is_over():
            raise ValueError("No attempts left")

        # kļūda, ja minējums īsaks par 5 burtiem un sastāv no ne burtu simboliem.
        if len(guess) != self.word_len or not guess.isalpha():
            raise ValueError(f"Word consists of {self.word_len} letters")
        
        # Pievieno minējumu sarakstam.
        self.attempts.append(guess)

    def tries_left(self):
        """Funkcija atgriež atlikušo mēģinājumu skaitu"""
        return self.max_tries - len(self.attempts)

    def is_over(self):
        """Funkcija nosaka, vai ir sasniegt maksimālais mēģinājumu skaits"""
        return len(self.attempts) >= self.max_tries
