import requests
import json

# Vārdu dabūšana spēlei ar API
class Api:
    def __init__(self):
        self.words = []

    def populate_words(self):
        url = "https://random-word-api.herokuapp.com/word"
        response = requests.get(f"{url}?length=5&number=10")
        self.words = response.json()

    def print_word(self):
        print(self.words)

#api testēšana - vēlāk jāizņem

vards = Api()
vards.populate_words()
vards.print_word()