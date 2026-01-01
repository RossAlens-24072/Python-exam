from words_api import Api
from guesses import Guesses

class Wordle:
    def __init__(self, difficulty ='standard'):
        # Veidojam klašu objektus inicializatorā
        self.answer = Api().populate_words().lower()
        self.guesses = Guesses()
        self.game_won = False
        self.difficulty = difficulty.lower()

        print(f"\nGrūtības pakāpe: {self.difficulty.upper()}")

    def evaluate_guess(self, guess):
        """Funkcija, kas glabās minētā vārda burtu statusu attiecībā pret pareizo atbildi"""
        if self.difficulty == 'hard':
            return ['_' for _ in range(len(guess))]
        
        result = []
        # Glabājam sarakstā pareizā vārda burtus
        answer_letters = list(self.answer)

        # pārbaudam vai kāds burts ir pareizs un atrodas pareizajā vietā
        for char in range(len(guess)):
            if guess[char] == self.answer[char]:
                result.append('Green')
                answer_letters[char] = None # Burts tiek atzīmēts kā lietots
            else:
                result.append('_') # Ja burts nav derīgs, tad ir '_'

        # pārbaudam vai ir kāds pareizs burts, bet nepareizajā vietā.
        for char in range(len(guess)):
            if result[char] == 'Green':
                continue # Burts jau ir pareizajā vietā

            letter = guess[char]
            if letter in answer_letters:
                result[char] = 'Yellow'
                idx = answer_letters.index(letter)
                answer_letters[idx] = None
            else:
                # Burts vispār nav pareizajā vārdā
                result[char] = '_'
        return result
    
    def get_hint(self):
        """Padara pirmo burtu redzamu priekš vieglā režīma"""
        if self.difficulty == 'easy' and not self.guesses.attempts:
            return self.answer[0]
        return None
    
    def display_hint(self):
        """Pārāda minamā vārda pirmo burtu"""
        if self.difficulty == 'easy':
            hint = self.get_hint()
            print(f"Vārds sākas ar burtu '{hint.upper()}'")

    def display_guess_result(self, guess, result):
        """Minēto vārdu saraksts"""
        if self.difficulty == 'hard':
            print("Informācija par minējumu netiks rādīta!!!")
            return

        for char in range(len(guess)):
            if result[char] == 'Green':
                print(f"Green - {guess[char].upper()}")
            elif result[char] == 'Yellow':
                print(f"Yellow - {guess[char].upper()}")
            else:
                print(f"Gray - {guess[char].upper()}")
        print("\n")

    # def get_diff_info(self):
    #     """Parāda informāciju par grūtības pakāpi"""
    #     info = {'easy': "Tiks dots pirmais vārds",
    #             'standard': "Legacy spēles noteikumi",
    #             'hard': "Netiks dots nekāds info par ievadītā vārda saistību ar atbildi"}
    #     return info.get(self.difficulty, "")


    def enter_word(self):
        """Vārda ievades funkcija spēlei"""
        while True:
            word = input("Veic vārda minējumu: ").strip().lower()
            if len(word) == 0:
                print("\nJūs neievadījāt vārdu!")
                continue
            if len(word) != 5:
                print("\nVārdam jābūt tieši 5 burtu lielumā!")
                continue
            if not word.isalpha():
                print("\nTikai alfabēta burti ir atļauti!")
                continue
            # Pārbauda, vai vārds jau ticis minēts
            if word in self.guesses.attempts:
                print(f"\nŠis vārds jau tika minēts: {word}")
                continue
            try:
                self.guesses.add_attempt(word)
                return word
            except ValueError as e:
                print(e)
                continue

    def display_progress(self):
        """Parāda visus minētos vārdus un to burtu statusu"""
        print("Minējumi: ")

        if not self.guesses.attempts:
            print("Nav neviena minējuma")
        else:
            for i, guess in enumerate(self.guesses.attempts):
                print(f"Minējums {i+1}: ",end="")
                result = self.evaluate_guess(guess)
                self.display_guess_result(guess, result)

        print(f"Atlikušie minējumi: {self.guesses.tries_left()}")

    def update_letter_status(self, guess, result):
        """Funkcija, kas atjaunina burtu statusu"""
        if self.difficulty == 'hard':
            return
        
        for i, letter in enumerate(guess):
            if letter not in self.guesses.letter_status:
                self.guesses.letter_status[letter] = result[i]
            elif result[i] == 'Green':
                self.guesses.letter_status[letter] = 'Green'
            elif result[i] == 'Yellow' and self.guesses.letter_status[letter] != 'Green':
                self.guesses.letter_status[letter] = 'Yellow'
    
    def display_letter_status(self):
        """Parāda kādi burti jau ir minēti un kāds viņu statuss"""
        if self.difficulty == 'hard':
            return
        
        if self.guesses.letter_status:
            print("\nBurtu statusi:")
            for letter, status in sorted(self.guesses.letter_status.items()):
                if status == 'Green':
                    print(f"{letter.upper()}: Green (Burts ir pareizs un ir pareizā vietā)")
                elif status == 'Yellow':
                    print(f"{letter.upper()}: Yellow (Burts ir vārdā, bet nepareizā vietā)")
                else:
                    print(f"{letter.upper()}: Gray (nav vārdā)")

    def play(self):
        """Pašas spēles darbības cikls"""
        print("mini vārdu")
        print(f"Tev ir {self.guesses.max_tries} mēģinājumi")
        print(self.difficulty)
        self.display_hint()

        while not self.guesses.is_over() and not self.game_won:
            self.display_progress()

            if self.difficulty != 'hard':
                self.display_letter_status()

            guess = self.enter_word()
            result = self.evaluate_guess(guess)

            print("Rezultāts: ")
            self.display_guess_result(guess, result)

            self.update_letter_status(guess, result)

            if guess == self.answer:
                self.game_won = True
                break
                
        print("Spēle ir beigusies!!!")
        if self.game_won:
            print("Vārds ir uzminēts")
            print(f"Tas prasīja {len(self.guesses.attempts)} mēģinājumus.")
        else:
            print("Vārds netika uzminēts!!!")
            print(f"Pareizā atbilde bija {self.answer}")

            #lietotāja minējumu parādīšana
            print("Jūsu minējumi: ")
            for i, guess in enumerate(self.guesses.attempts):
                print(f"{i+1}. {guess.upper()}")

# Testēšana, lai mainītu diff iedod to objektam!
obj = Wordle('easy')
print(f"DEBUG - pareizais spēles atminējums: {obj.answer}")
obj.play()