import random
from collections import defaultdict
import numpy as np
from utils import calculate_hand_value

class RLAgent:
  def __init__(self):
    self.player_wins = 0
    self.total_matches = 0 
    # Learning rate - 
    self.alpha = 0.1
    # Discount factor - Balanço entre priorizar recompensas futuras e atuais
    self.gamma = 0.9
    # Exploration rate - epsilon greedy
    self.epsilon = 0.1
    # Lembrando a ultima acao
    self.last_opponent_action = None
    # Flag indicando se essa seria a ultima rodada
    self.last_round = False   
    # Q table
    self.Q = defaultdict(lambda: [0.0, 0.0])
    self.action_list = ["hit", "stop"]
    
    self.current_input = None
    self.current_output = None    
    
  # def extract_rl_state(self, your_hand):
  #   # versão bem básica onde apenas verificamos se o total
  #   # em nossa mão é maior que 11, assim podemos
  #   # ter uma característica para indicar se tem
  #   # uma chance de 'estourar' a mão mas isso 
  #   # não leva em conta várias pontos importantes z
  #   return (int(calculate_hand_value(your_hand) > 11),);

  def extract_rl_state(self, your_hand, dealer_first_card):
    player_value = calculate_hand_value(your_hand)
    dealer_value = calculate_hand_value([dealer_first_card])
    ace_count = sum(1 for card in your_hand if card.value == 'ace')
    
    state = (player_value, dealer_value, ace_count)
    return state
 
  # def choose_action(self, state):
  #   #
  #   # Pode ser melhorado!
  #   #
  #   if not state:
  #     if np.random.uniform(0, 1) < self.epsilon:
  #       # Explore: Choose a random action
  #       action = np.random.choice(self.action_list)
  #     else:
  #       # Exploit: Choose the action with the maximum Q-value
  #       action = self.action_list[np.argmax(self.Q[state])]
  #   else:
  #     return "hit"
  #   return action
  

  def choose_action(self, state):
    if np.random.uniform(0, 1) < self.epsilon:
        action = np.random.choice(self.action_list)  
    else:
        if state in self.Q:
            action = self.action_list[np.argmax(self.Q[state])]
        else:
            action = "hit"  
    return action
    
    
  # def update_qtable(self, state, action, reward, next_state):
  #   alp = self.alpha
  #   gam = self.gamma
  #   action_index = self.action_list.index(action)
  #   self.Q[state][action_index] = (1 - alp) * self.Q[state][action_index] + alp * (reward + gam * np.max(self.Q[next_state]))  

  def update_qtable(self, state, action, reward, next_state, player_hand, dealer_first_card):
    alp = self.alpha
    gam = self.gamma
    action_index = self.action_list.index(action)
    max_next_q = np.max(self.Q[next_state]) if next_state in self.Q else 0.0
    
    playerValue = calculate_hand_value(player_hand)
    dealerValue = calculate_hand_value([dealer_first_card])
    
    if ((action == "stop" and (playerValue > 17 and not any(card.value == 'ace' for card in player_hand))) 
        or 
        (action == "hit" and (playerValue < 17 and dealerValue >= 7))
        or
        (action == "stop" and (playerValue < 17 and playerValue > 12 and dealerValue < 7))
        or
        (action == "hit" and (playerValue < 11))
        or
        (action == "hit" and (any(card.value == 'ace' for card in player_hand) and playerValue >= 17 and playerValue < dealerValue + 10))
        or
        (action == "stop" and (any(card.value == 'ace' for card in player_hand) and playerValue >= 17 and playerValue > dealerValue + 10))
        or
        (action == "hit" and (any(card.value == 'ace' for card in player_hand) and playerValue < 17))
        ):
        reward += 1  
    else:
        reward -= 1  
        
    self.Q[state][action_index] += alp * (reward + gam * max_next_q - self.Q[state][action_index])

    
  # Essa função toma a decisão após observar
  # o estado observável do campo
  def decision(self, your_hand, dealer_first_card):
    player_hand = [d for d in your_hand]
    print("======== Start of turn =======")
    print(f"Player hand: {player_hand} vs dealer {dealer_first_card}, ...", ) 
    state = self.extract_rl_state(your_hand=your_hand, dealer_first_card=dealer_first_card)
    choice = self.choose_action(state)
    print(f"You made the decision '{choice}'")
    return choice

  # Essa função deveria atualiza QTable
  # def result(self, your_hand, dealer_first_card, decision, reward, is_not_done):
  #   player_hand = [d for d in your_hand]
  #   game_status = "still going" if is_not_done else "is done" 
  #   print(f"{your_hand=}")
  #   state = self.extract_rl_state(your_hand=your_hand[:-1])
  #   next_state = self.extract_rl_state(your_hand=your_hand)
  #   self.update_qtable(state, decision, reward, next_state)
  #   self.print_q_table(self.Q)
  #   print(f"Your hand ({calculate_hand_value(your_hand)}) after decision '{decision}' with {reward=} and game {game_status}")

  #   print("======== End of turn =======")    

  def result(self, your_hand, dealer_first_card, decision, reward, is_not_done):
    state = self.extract_rl_state(your_hand, dealer_first_card)
    next_state = self.extract_rl_state(your_hand + [dealer_first_card], dealer_first_card)

    game_status = "still going" if is_not_done else "is done" 
    print(f"{your_hand=}")

    self.update_qtable(state, decision, reward, next_state, your_hand, dealer_first_card)
    self.print_q_table(self.Q)
    print(f"Your hand ({calculate_hand_value(your_hand)}) after decision '{decision}' with {reward=} and game {game_status}")

    print("======== End of turn =======") 
  
  def print_q_table(self, Q):
    for k,v in Q.items():
      print(f"For state={k}")
      for idx, a in enumerate(self.action_list):
        print(f"  Q for {a}", Q[k][idx])
    
  # Nome de seu agente deve ser colocado aqui  
  def get_name(self):
    return "TigerBaldo"


