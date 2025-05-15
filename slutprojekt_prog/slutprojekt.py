from flask import Flask, render_template
import requests

app = Flask(__name__)

class Blackjack:
    def __init__(self, nr_decks=6):
        self._deck_id = None
        self._create_new_deck(nr_decks)
        
    def _create_new_deck (self,nr_decks):
        try:
            response = requests.get(f"https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count={nr_decks}")
            response.raise_for_status()
            data = response.json()
            self._deck_id = data["deck_id"]
        except requests.RequestException as e:
            print(f"[ERROR] Kunde inte skapa kortlek: {e}")
            
Blackjack_game = Blackjack(nr_decks=6)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/blackjack")
def blackjack():
    return render_template("blackjack.html")

if __name__ == '__main__':
    app.run(debug=True)
