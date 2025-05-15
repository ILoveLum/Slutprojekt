from flask import Flask, redirect, url_for, render_template
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
            
    def draw_cards(self,count=2):
        if not self._deck_id:
            return None
        try:
            response = requests.get(f"https://www.deckofcardsapi.com/api/deck/{self._deck_id}/draw/?count={count}")
            response.raise_for_status()
            return response.json().get("cards", [])
        except requests.RequestException as e:
            print(f"[ERROR] Kunde inte dra kort: {e}")
            return None
            
blackjack_game = Blackjack(nr_decks=6)

@app.route('/blackjack/draw', methods=['POST'])
def blackjack_draw():
    cards = blackjack_game.draw_cards(2)
    return render_template("blackjack.html", cards=cards)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/blackjack")
def blackjack():
    return render_template("blackjack.html")

if __name__ == '__main__':
    app.run(debug=True)
