from flask import Flask, render_template, request
import requests

Casino = Flask(__name__)

class Blackjack: 
    def __init__(self, nr_decks):
        try:
            # Updated API endpoint URL
            response = requests.get(f"https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count={nr_decks}")
            
            # Print out the full response for debugging
            print("Response status code:", response.status_code)
            print("Response content:", response.text)
            
            # Ensure successful response
            response.raise_for_status()
            
            data = response.json()
            self.deck_id = data["deck_id"]
            print(f"Ny kortlek skapad! Deck ID: {self.deck_id}")
        except requests.RequestException as e:
            self.deck_id = None
            print(f"Fel vid skapande av kortlek: {e}")

@Casino.route('/')
def home():
    # Placeholder route to demonstrate Flask is working
    return "Casino projekt startat!"

if __name__ == '__main__':
    # Initialize a Blackjack game with 1 deck to test API
    test_game = Blackjack(1)
    Casino.run(debug=True)