# "Texas Hold'em" game analytics
![Image containing some cards on white background](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT13KjK7D9lIdrLn3kXN5X0GaVqVrBRZbf09g&usqp=CAU)
## Scope
The idea behind this project is to provide a tool for assisting the player during a Poker game,
particularly by analyzing in real time a hand given a user input and thus helping the player to improve his strategy and decision making by offering probability based predictions.

## Code Structure
The program is built using OOP paradigms. Each entity has its own class and methods and custom exceptions are added to improve error handling.

- ### TCard
  Each card has a value and a suit and is represented by a name obtained glueing together its     value and its suit (e.g. "JH", "qs", "Ad", "3c").
  Altough only certain values are accepted (see TDeck), technically speaking the only rule you have to follow when creating an instance TCard, is to provide a name of exactly two characters (with the sole exceptions of all cards with value 10, as it's possible to use both "T" and "10" as the value, with "10" promptly converted to "T").
  
  Class methods are:
  - **getName:**  _Returns a two-character string containing object attributes value + suit_
  - **getValue:**  _Returns the value as a char_
  - **getSuit:**  _Returns the suit as a char_
  
- ### TDeck
  A container for the allowed cards according to the current game rules.
  Since we're interested in analyzing a "Texas Hold'em" game, the cards are stored in a 4x13 matrix (4 suits, 13 values), but obviously we can change it to fit different card games.
  
  Class methods are:
  - **addCard:**  _Given a valid object TCard, adds it to the deck_
  - **removeCard:**  _Checks if a card is present and removes it from the deck_
  - **getCards:**  _Returns the numpy array containig all current cards_
  - **getValues:**  _Returns the list of allowed values_
  - **getSuits:**  _Returns the list of allowed suits_

  There are other methods, but are of much smaller impact and have way less use cases, so have been omitted.

  **Accepted values are:**
    - (2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A)

  **Accepted suits are:**
    - (S, H, D, C)
    
- ### TStdDeck
  Simply a child class of TDeck from whom inherites all methods and attributes, but it's been prefilled with all 52 possible cards by default. Very useful for all the probability calculations later occuring.
  
- ### THand
  Still in costruction, but as of now accepts user inputs and, by setting a deck and the current number of players, returns step-by-step the current value of your hand and the odds of improving it by the next reveal of new cards.
