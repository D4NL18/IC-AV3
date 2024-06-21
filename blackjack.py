import pygame
import random
import itertools
from utils import calculate_hand_value
from dealer import DealerPlayer
from PlayerRL import RLAgent as Player

# Initialize Pygame
pygame.init()

# Game window settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Simple Blackjack')

# Load character portraits
portraits = [
  pygame.image.load(f'portrait/1.png'),
  pygame.image.load(f'portrait/2.png'),  
]

dealer_portrait_img = pygame.image.load(f'portrait/dealer.png'),  

winner_image = pygame.transform.scale(pygame.image.load(f'symbols/winner.png'), (200, 200))

# Load card images (assuming we have basic card images named as '2_of_clubs.png', '3_of_hearts.png', etc.)
card_images = {}
suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
player_portrait = pygame.transform.scale(random.choice(portraits), (80, 160))
dealer_portrait = pygame.transform.scale(random.choice(dealer_portrait_img), (80, 160))

for suit in suits:
    for value in values:
        image_scale = 0.5
        card_img =  pygame.image.load(f'cards/{value}_of_{suit}.png')
        scaled_card = pygame.transform.scale(card_img, (int(200 * image_scale), int(300 * image_scale)))        
        card_images[(suit, value)] = scaled_card


# Card values
card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
               'jack': 10, 'queen': 10, 'king': 10, 'ace': [1, 11]}


# Draw card function
def draw_card(deck, hand):
    card = random.choice(deck)
    hand.append(card)
    deck.remove(card)
    return card

def render_card(card, pos):
    screen.blit(card_images[(card.suit, card.value)], pos) 
    
def render_hand(hand, pos):
    for idx, c in enumerate(hand):
      screen.blit(card_images[(c.suit, c.value)], pos)
      pos = (pos[0] + 120, pos[1])

def render_portrait(portrait, pos):
    screen.blit(portrait, pos) 

def render_winner(pos):
    screen.blit(winner_image, pos) 

class Card:
  def __init__(self, suit, value):
    self.value = value
    self.suit = suit
    
  def __repr__(self):
    return f'[{self.value}-{self.suit}]'
    


# Main game loop
def play_blackjack(player):
    running = True
    player_turn = False  # True if it's player's turn, False for dealer's turn
    dealer_turn = True


    

    # Create a deck of cards and deal initial hands
    # [rest of the initial setup is the same]
    deck = [Card(s,v) for s,v in itertools.product(suits, values)]
    player_hand = []
    dealer_hand = []
    hand_result = 0
    random.shuffle(deck)
    #print([d for d in deck])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle player input here (e.g., hit or stand)
            # You can use keys or mouse clicks for player decisions

        screen.fill((0, 0, 0))  # Clear screen (black background)
        #render_card(deck[0], (100, 100))
        
        # Display the cards and scores

        if dealer_turn:
            # Dealer's turn logic
            dealer_value = calculate_hand_value(dealer_hand)
            if dealer_value < 17:
                draw_card(deck, dealer_hand) 
            else:
              dealer_turn = False
              player_turn = True       
        elif player_turn:
            # Player's turn logic
            # Implement hit or stand decision
            decision = player.decision(player_hand, dealer_hand[0])
            if decision == "hit":
               draw_card(deck, player_hand)
            else:
               player_turn = False

            if calculate_hand_value(player_hand) >= 21:
              player_turn = False                
               
            score = 0   
            #decision = player.result(player_hand, dealer_hand[0], decision)   
            
            if not player_turn:
                # Compare hands and decide winner
                player_value = calculate_hand_value(player_hand)
                if (player_value > 21):
                  hand_result = -1
                  player.total_matches+=1
                elif (dealer_value > 21):
                  hand_result = +1
                  player.player_wins+=1
                  player.total_matches+=1
                elif (player_value > dealer_value):
                  hand_result = +1
                  player.player_wins+=1
                  player.total_matches+=1
                elif (player_value == dealer_value):
                  hand_result = 0
                  player.total_matches+=1
                else:
                  hand_result = -1
                  player.total_matches+=1
                #print(f"Round result {hand_result}")                     
                running = False
            # Decision
            print(f"Dealer hidden hand ({dealer_value}): {dealer_hand}")
            decision = player.result(player_hand, dealer_hand[0], decision, hand_result, player_turn)
        
        render_hand(player_hand, (150, 100))
        render_hand(dealer_hand, (150, 300))     
        render_portrait(player_portrait, (50, 100))
        render_portrait(dealer_portrait, (50, 300))                
        pygame.display.flip()  # Update the display
        pygame.time.wait(10)  
        
    # Durante treinamento você deve 
    # remover esse delay para acelerar o treinamento 
    print(f'winrate: {player.player_wins*100/player.total_matches}%')   
    pygame.time.wait(10000)  

    return hand_result


def play_n_rounds(player, n):
    results = []
    for _ in range(n):
      results.append(play_blackjack(player))  
    return results

def get_odds(results):
  t = len(results)
  return (results.count(1) / t, results.count(-1) / t, results.count(0) / t)

# Insire seu jogador abaixo:
player = Player()

# Jogamos 100 rodadas de treino 
# depois disso jogamos 100 rodadas
# onde deveríamos jogar de forma
# mais gulosa para obter o score
# final. Não existe rodada de 
# treino, o RL aprende enquanto
# explora as possibilidades mas
# para normalizar os resultados
# faremos desse jeito. Você
# pode alterar esses valores sem
# nenhum problema. Os valores de treino
# e teste em particular podem (e devem)
# ser bem maiores.
training_score = play_n_rounds(player, 100)
real_score = play_n_rounds(player, 100)
 

import statistics
print(f"Player Expected Value was {get_odds(real_score)} [Training: {get_odds(training_score)}]")
pygame.time.wait(3000)
pygame.quit()
