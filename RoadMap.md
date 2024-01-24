# Project RoadMap

## Urgent mods

- **Modify function "what_do_I_have" in class THand**

  At the moment it returns an f string containing info about your current hand, making it easy for the user to acknowledge his situation, but rather difficult for the machine . In particular, if it has to calculate the odds of improving your hand, it's crucial to obtain the result of what_do_I_have in a "workable" and flexible format. The solution is to separate the print and the calculations in different functions. This way we can also add a third function in between to order the cards by value.

- **Update or point-blank write the probability calculation functions**
- **Add the "against-odds" calculated considering the number of players**
- **Refactor code in different files for better usability and mantainability**

## Additional features to be implemented

- **Start considering the pot and calculate the pot odds; compare the pot odds with the actual odds and decide wheter a play has positive expectancy**

  This feature, altough quite useful, involves several risks, as it may severely slow the input of the necessary data, therefore making it difficult to use the program effectively in a real time game.
  
- **Create a TGame class with the purpose of storing data about the previous hands played**

  The data may be saved on a dedicated DB or simply in a pd.DataFrame. The point is to create a comprehensive record of the played hands from where to extrapolate important info about the player's behaviour and other analytics.

- **Create a GUI in python or possibly migrate to Java/Kotlin**

  The intention is to make the tools available to a wider userbase and increment the overall speed and effectiv ness by making easier the data input, which is  currently the more time-costly
part of the project.

- **Add implied odds**

  Multiply the pot odds by a factor based on your position. If you're the last one, the factor should be 1 as you're 100% sure the pot won't change after you call or bet, on the contrary, when you're 
among the firsts to make a decision about a certain call or bet, the pot odds are much more uncertain and volatile.
