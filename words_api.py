import requests
# Vārdu dabūšana spēlei ar API
class Api:
    def __init__(self):
        self.words = []

    def populate_words(self):
        url = "https://random-word-api.herokuapp.com/word"
        response = requests.get(f"{url}?length=5&number=1")
        self.words = response.json()
        return self.words[0]

    def print_word(self):
        print(self.words)