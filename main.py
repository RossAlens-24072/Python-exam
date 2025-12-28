from words_api import Api
from guesses import Guesses

def run_game(reveal=0): #parametrs reveal definē, cik pirmos burtus no vārda atklāj - 0 grūtāk, 1 vieglāk
    
    secret = Api().populate_words().lower() #atgriež vienu vārdu 5 ar burtiem.
    
    #TESTĒŠANAI izdrukā slepeno vārdu
    print("DEBUG secret:", secret) 

    required_prefix = secret[:reveal] #paņem pirmos burtus no slepenā vārda sākuma līdz reveal indeksam
    guesses = Guesses(max_tries=6, word_len=5)

    # TESTAM pagaidām rāda hintu terminālī 
    print("Hint:", required_prefix + "_" * (5 - reveal))


    while not guesses.is_over():
        g = input("Enter guess: ")
        try:
            guesses.add_attempt(g, required_prefix=required_prefix)
        except ValueError as e:
            print("Invalid:", e)
            continue 

        # Lietotāja pēdējais minējums ir vienāds ar slēpto vārdu
        last = guesses.attempts[-1]
        print("You guessed:", last)
        if last == secret:
            print("You won!")
            return

    print("You lost. The word was:", secret)

# TESTS
run_game(reveal=1) 