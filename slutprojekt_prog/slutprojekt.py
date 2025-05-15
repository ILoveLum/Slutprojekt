from flask import Flask, redirect, url_for, render_template, request, session
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

class Blackjack: # Class för blackjack och spelets funktioner
    def __init__(self, nr_decks=6):
        self._deck_id = None
        self._create_new_deck(nr_decks)
        
    def _create_new_deck (self,nr_decks): # Nytt däck skapas
        try:
            response = requests.get(f"https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count={nr_decks}")
            response.raise_for_status()
            data = response.json()
            self._deck_id = data["deck_id"]
        except requests.RequestException as e:
            print(f"[ERROR] Kunde inte skapa kortlek: {e}")
            
    def draw_cards(self,count=2): # Drar 2 kort för spelaren
        
        if not self._deck_id:
            return None
        try:
            response = requests.get(f"https://www.deckofcardsapi.com/api/deck/{self._deck_id}/draw/?count={count}")
            response.raise_for_status()
            return response.json().get("cards", [])
        except requests.RequestException as e:
            print(f"[ERROR] Kunde inte dra kort: {e}")
            return None
        
    def calculate_points(self,cards): # Pöang system
        points = 0
        aces = 0
        
        for card in cards:
            value = card ["value"]
            if value.isdigit():
                points += int(value)
            elif value in ["JACK", "QUEEN", "KING"]: # Dessa hanteras som 10 i blackjack
                points += 10
            elif value == "ACE": # Ace hanteras som 1 eller 10 beroande på spelarens värde
                aces += 1
                
        for _ in range(aces):
            # Om 11 inte bustar, använd 11 annars 1
            if points + 11 <= 21:
                points += 11
            else:
                points += 1

        return points
    
class HiLo: # Class och funktioner för spelet Higher or lower (HiLo)
    def __init__(self):
        self._deck_id = None
        self._create_new_deck()

    def _create_new_deck(self): # Nytt däck skapas som i Blackjack
        try:
            response = requests.get("https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
            response.raise_for_status()
            data = response.json()
            self._deck_id = data["deck_id"]
        except requests.RequestException as e:
            print(f"[ERROR] Kunde inte skapa Hi-Lo-lek: {e}")

    def draw_card(self): # 1 kort dras
        if not self._deck_id:
            return None
        try:
            response = requests.get(f"https://www.deckofcardsapi.com/api/deck/{self._deck_id}/draw/?count=1")
            response.raise_for_status()
            return response.json()["cards"][0]
        except requests.RequestException as e:
            print(f"[ERROR] Kunde inte dra kort i Hi-Lo: {e}")
            return None
        
    def compare_guess(self, guess):
        # Dra ett nytt kort och jämför med det tidigare
        new_card = self.draw_card()
        if not self.current_card or not new_card:
            return None, None, "Fel vid kortdragning"

        old_value = self._card_value(self.current_card["value"]) # Gamla värdet på kortet
        new_value = self._card_value(new_card["value"]) # Nya värdet

        correct = (guess == "higher" and new_value > old_value or old_value == new_value) or \
                  (guess == "lower" and new_value < old_value or old_value == new_value) # Kollar om det är rätt. Samma värde räknas som rätt
                  
        return new_card, correct, None
    
    def _card_value(self, value):
        if value == "ACE": # ACE räknas som 1
            return 1
        elif value in ["JACK", "QUEEN", "KING"]:
            return 11 + ["JACK", "QUEEN", "KING"].index(value) # Jack är 11 med index 0 så det blir 11 osv med andra kort som har högre index
        else:
            return int(value)

            
blackjack_game = Blackjack(nr_decks=6) # Blackjack körs oftast med 6 däck (kan variera)    

hilo_game = HiLo()

@app.route('/blackjack/draw', methods=['POST'])
def blackjack_draw():
    cards = blackjack_game.draw_cards(2)
    points = blackjack_game.calculate_points(cards) if cards else 0
    return render_template("blackjack.html", cards=cards, points=points)

@app.route('/hilo')
def hilo():
    session ['score'] = 0
    card = hilo_game.draw_card()
    session ['previous_card'] = card
    return render_template("hilo.html", card=card, score = 0)

@app.route('/hilo/guess', methods=['POST'])
def hilo_guess():
    guess = request.form.get("guess")

    # Stoppar spelet manuellt
    if guess == "stop":
        score = session.get("score", 0)
        session.clear()
        return render_template("hilo.html", card=None, score=score, game_over=True)

    previous_card = session.get("previous_card")
    if not previous_card:
        return redirect(url_for("hilo"))  # Om något går fel, börja om

    hilo_game.current_card = previous_card
    new_card, correct, error = hilo_game.compare_guess(guess)

    if error:
        return render_template("hilo.html", error=error)

    if correct:
        session["score"] += 1
        session["previous_card"] = new_card
        return render_template("hilo.html", card=new_card, score=session["score"], correct=True)
    else:
        score = session["score"]
        session.clear()
        return render_template("hilo.html", card=new_card, score=score, correct=False, game_over=True)

def render_blackjack_page(error=None):
    player_cards = session.get("player_cards", [])
    dealer_cards = session.get("dealer_cards", [])
    player_points = blackjack_game.calculate_points(player_cards)
    dealer_points = blackjack_game.calculate_points(dealer_cards) if session.get("game_over") else None
    game_over = session.get("game_over", False)
    result = session.get("result", None)

    # Om spelet inte är över, visa endast första dealer-kortet + baksida
    if not game_over and dealer_cards:
        displayed_dealer_cards = [dealer_cards[0], {"image": "/static/back.png"}]
    else:
        displayed_dealer_cards = dealer_cards

    return render_template("blackjack.html",
                           player_cards=player_cards,
                           dealer_cards=displayed_dealer_cards,
                           player_points=player_points,
                           dealer_points=dealer_points,
                           game_over=game_over,
                           result=result,
                           error=error)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/blackjack")
def blackjack():
    return redirect(url_for("blackjack_start"))


@app.route('/blackjack/start')
def blackjack_start():
    player_cards = blackjack_game.draw_cards(2)
    dealer_cards = blackjack_game.draw_cards(2)

    if not player_cards or not dealer_cards:
        return "Kunde inte dra kort – kontrollera internetanslutning eller API:n."

    session["player_cards"] = player_cards
    session["dealer_cards"] = dealer_cards
    session["game_over"] = False
    session["result"] = None

    player_points = blackjack_game.calculate_points(player_cards)
    if player_points == 21:
        session["game_over"] = True
        session["result"] = "Blackjack! Du vinner direkt!"

    return render_blackjack_page()


@app.route('/blackjack/hit', methods=['POST'])
def blackjack_hit():
    
    player_cards = session.get("player_cards", [])
    dealer_cards = session.get("dealer_cards", [])

    new_card = blackjack_game.draw_cards(1)[0]
    player_cards.append(new_card)
    session["player_cards"] = player_cards

    player_points = blackjack_game.calculate_points(player_cards)
    if player_points > 21:
        session["game_over"] = True
        session["result"] = "Du fick över 21. Du förlorar!"

    return render_blackjack_page()

@app.route('/blackjack/stay', methods=['POST'])
def blackjack_stay():

    player_cards = session.get("player_cards", [])
    dealer_cards = session.get("dealer_cards", [])

    player_points = blackjack_game.calculate_points(player_cards)
    dealer_points = blackjack_game.calculate_points(dealer_cards)

    while dealer_points < 17:
        new_card = blackjack_game.draw_cards(1)[0]
        dealer_cards.append(new_card)
        dealer_points = blackjack_game.calculate_points(dealer_cards)

    session["game_over"] = True

    if dealer_points > 21 or player_points > dealer_points:
        result = "Du vinner!"
    elif dealer_points > player_points:
        result = "Dealern vinner."
    else:
        result = "Oavgjort!"

    session["result"] = result

    return render_blackjack_page()


if __name__ == '__main__':
    app.run(debug=True)
    