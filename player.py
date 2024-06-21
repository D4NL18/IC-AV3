import random 
from utils import calculate_hand_value, calculate_card_value

 ######################################
 #
 # Seu agente deve ser colocado nessa região
 # Lembre-se que a regra do blackjack foi modificada
 # nesse versão o dealer joga primeiro que você
 # e você joga vendo a primeira carta dele
 #
 #
class Player:
  # Essa função toma a decisão após observar
  # o estado observável do campo
  def __init__(self):
    self.player_wins = 0
    self.total_matches = 0  
  
  def decision(self, your_hand, dealer_first_card):
    player_hand = [d for d in your_hand]
    print("======== Start of turn =======")
    print(f"Player hand: {player_hand} vs dealer {dealer_first_card}, ...", )
    if calculate_hand_value(your_hand) <= 11:
      choice = "hit"
    elif calculate_hand_value(your_hand) == 12 and (calculate_card_value(dealer_first_card) == 2 or calculate_card_value(dealer_first_card) == 3 or(calculate_card_value(dealer_first_card) >= 7)):
      choice = "hit"
    elif calculate_hand_value(your_hand) == 12 and (calculate_card_value(dealer_first_card) == 4 or calculate_card_value(dealer_first_card) == 5 or calculate_card_value(dealer_first_card) == 6):
      choice = "stop"
    elif (calculate_hand_value(your_hand) == 13 or calculate_hand_value(your_hand) == 14) and calculate_card_value(dealer_first_card) >=7:
      choice = "hit"
    elif (calculate_hand_value(your_hand) == 13 or calculate_hand_value(your_hand) == 14) and calculate_card_value(dealer_first_card) <7:
      choice = "stop"
    elif calculate_hand_value(your_hand) == (15) and calculate_card_value(dealer_first_card) >=7 and calculate_card_value(dealer_first_card) != 10:
      choice = "hit"
    elif calculate_hand_value(your_hand) == (15) and (calculate_card_value(dealer_first_card) <7 or calculate_card_value(dealer_first_card) == 10):
      choice = "stop"
    elif calculate_hand_value(your_hand) == (16) and (calculate_card_value(dealer_first_card) != 9 or calculate_card_value(dealer_first_card) != 10 or calculate_card_value(dealer_first_card) != 11):
      choice = "hit"
    elif calculate_hand_value(your_hand) == (16) and (calculate_card_value(dealer_first_card) == 9 or calculate_card_value(dealer_first_card) == 10 or calculate_card_value(dealer_first_card) == 11):
      choice = "stop"
    elif calculate_hand_value(your_hand) == (17):
      choice = "stop"
    else:
      choice = "stand"
    print(f"You made the decision '{choice}'")
    return choice

  # Essa função deveria utilizar o resultado para 
  # atualizar a QTable
  def result(self, your_hand, dealer_first_card, decision, reward, is_not_done):
    player_hand = [d for d in your_hand]
    game_status = "still going" if is_not_done else "is done" 
    print(f"Your hand ({calculate_hand_value(your_hand)}) after decision '{decision}' with {reward=} and game {game_status}")
    if not is_not_done:
      print("======== End of turn =======")
