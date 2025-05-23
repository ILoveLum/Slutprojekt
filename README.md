## Kortspelsapplikation
En webbapplikation utvecklad med Flask som erbjuder två klassiska kortspel: Blackjack och Higher-or-Lower (HiLo).
Beskrivning
Denna applikation låter användare spela två populära kortspel genom ett enkelt webbgränssnitt:

Blackjack: Spela mot dealern och försök få en hand värd 21 poäng eller så nära som möjligt utan att gå över.
Higher-or-Lower (HiLo): Gissa om nästa kort kommer vara högre eller lägre än det nuvarande kortet.

Båda spelen använder Deck of Cards API för att simulera kortlekar och korthantering.
Funktioner
Blackjack

Spelas med sex kortlekar för autenticitet
Dealern drar kort tills han har minst 17
Stöd för "Hit" och "Stay" actions
Automatisk poängberäkning och hantering av ess (som kan vara värda 1 eller 11)
Direkt vinst vid Blackjack (21 på första två korten)

Higher-or-Lower (HiLo)

Fortlöpande poängräkning för att spåra spelsekvenser
Spelaren kan välja att avsluta när som helst för att behålla sin poäng
Automatisk kontroll av gissningar
Samma värde räknas som rätt gissning

## Installation

1. Klona detta repository

2. git clone https://github.com/ILoveLum/Slutprojekt.git 
   cd kortspel-app

3. Skapa en virtuell miljö och aktivera den

4. python -m venv venv
   source venv/bin/activate  # På Windows: venv\Scripts\activate

## Installera beroenden

1. pip install -r requirements.txt

2. Starta applikationen

3. python app.py

4. Besök http://localhost:5000 i din webbläsare

## Tekniska detaljer

Backend: Python med Flask
Korthantering: Deck of Cards API
Sessionhantering: Flask sessioner för att spåra spelstatus
Responsiv design: Anpassat för både desktop och mobila enheter (Gjort med AI!)

## Projektstruktur
kortspel-app/
├── app.py                # Huvudapplikationsfil med Flask-routes och spellogik
├── static/
│   ├── back.png          # Kortets baksida för Blackjack
│   ├── styles.css        # CSS-stilar
│   └── script.js         # JavaScript-funktionalitet
├── templates/
│   ├── index.html        # Startsida
│   ├── blackjack.html    # Blackjack-spelsida
│   └── hilo.html         # HiLo-spelsida
└── requirements.txt      # Projektberoenden

## Krav
Python 3.11.4+
Flask
Requests
Internetanslutning (för att ansluta till Deck of Cards API)

## Framtida förbättringar

Lägga till insatssystem (pengar)
Implementera delning och dubbel insats i Blackjack
Spara highscores för HiLo
Lägga till fler kortspel (Poker, backarat etc.)

Licens
MIT