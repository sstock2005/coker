import dataclasses
import pygame.freetype 
import pygame
import yaml
import random
import os
from dataclasses import dataclass
from enum import Enum
import time

# Load config
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

class WinResult(Enum): # DONE
    TIE = (True, True)
    PLAYER_WIN = (True, False)
    NPC_WIN = (False, True)
    NO_WIN = (False, False)
    
class WinningHand(Enum): # DONE
    STRAIGHT_FLUSH = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    FLUSH = 3
    STRAIGHT = 4
    THREE_OF_A_KIND = 5
    TWO_PAIR = 6
    ONE_PAIR = 7
    HIGH_CARD = 8
    NONE = 9
    
class Suit(Enum): # DONE
    CLUB = 1
    DIAMOND = 2
    HEART = 3
    SPADE = 4
    
class CardNumber(Enum): # DONE
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    
class GameState(Enum): # DONE
    DRAW = 0
    BETTING = 1
    HOUSECARDS = 2
    NOTHING = 3
    END = 4
    
class ButtonType(Enum): # DONE
    BET1 = 0
    BET5 = 1
    BET10 = 2
    BETALLIN = 3
    CALL = 4
    RAISE = 5
    FOLD = 6
    NEW = 7
    START = 8
    
def width(): # DONE
    return 1280

def height(): # DONE
    return 720

def get_horizontal_middle(image_width: int) -> int: # DONE
    return (width() // 2) - (image_width // 2)

def get_vertical_middle(image_height: int) -> int: # DONE
    return (height() // 2) - (image_height // 2)

def get_hand_1_pos(): # DONE
    x = (get_horizontal_middle(config['game']['card_width'])) - (config['game']['card_width'] * 0.55)
    y = (height() // 4) * 3
    return x, y

def get_hand_2_pos(): # DONE
    x = (get_horizontal_middle(config['game']['card_width'])) + (config['game']['card_width'] * 0.55)
    y = (height() // 4) * 3
    return x, y

def get_hand_1_pos_npc(): # DONE
    x, y = get_hand_1_pos()
    y -= (height() * 0.7)
    return x, y

def get_hand_2_pos_npc(): # DONE
    x, y = get_hand_2_pos()
    y -= (height() * 0.7)
    return x, y

def get_card(suit: Suit, position: int, back: bool = False):
    if back:
        location = os.path.join('resources/Top-Down/Cards', 'Card_Back-88x124.png')
        image = pygame.image.load(location)
        rect = pygame.Rect(0, 0, config['game']['card_width'], config['game']['card_height'])
        return image, rect
    
    match suit:
        case Suit.CLUB:
            location = os.path.join('resources/Top-Down/Cards', 'Clubs-88x124.png')
        case Suit.DIAMOND:
            location = os.path.join('resources/Top-Down/Cards', 'Diamonds-88x124.png')
        case Suit.HEART:
            location = os.path.join('resources/Top-Down/Cards', 'Hearts-88x124.png')
        case Suit.SPADE:
            location = os.path.join('resources/Top-Down/Cards', 'Spades-88x124.png')
            
    match position:
        case 1:
            rect = pygame.Rect(0, 0, config['game']['card_width'], config['game']['card_height'])
        case 2:
            rect = pygame.Rect(config['game']['card_width'], 0, config['game']['card_width'], config['game']['card_height'])
        case 3:
            rect = pygame.Rect(config['game']['card_width'] * 2, 0, config['game']['card_width'], config['game']['card_height'])
        case 4:
            rect = pygame.Rect(config['game']['card_width'] * 3, 0, config['game']['card_width'], config['game']['card_height'])
        case 5:
            rect = pygame.Rect(config['game']['card_width'] * 4, 0, config['game']['card_width'], config['game']['card_height'])
        case 6:
            rect = pygame.Rect(0, config['game']['card_height'], config['game']['card_width'], config['game']['card_height'])
        case 7:
            rect = pygame.Rect(config['game']['card_width'], config['game']['card_height'], config['game']['card_width'], config['game']['card_height'])
        case 8:
            rect = pygame.Rect(config['game']['card_width'] * 2, config['game']['card_height'], config['game']['card_width'], config['game']['card_height'])
        case 9:
            rect = pygame.Rect(config['game']['card_width'] * 3, config['game']['card_height'], config['game']['card_width'], config['game']['card_height'])
        case 10:
            rect = pygame.Rect(config['game']['card_width'] * 4, config['game']['card_height'], config['game']['card_width'], config['game']['card_height'])
        case 11:
            rect = pygame.Rect(0, config['game']['card_height'] * 2, config['game']['card_width'], config['game']['card_height'])
        case 12:
            rect = pygame.Rect(config['game']['card_width'], config['game']['card_height'] * 2, config['game']['card_width'], config['game']['card_height'])
        case 13:
            rect = pygame.Rect(config['game']['card_width'] * 2, config['game']['card_height'] * 2, config['game']['card_width'], config['game']['card_height'])
            
    image = pygame.image.load(location)
    return image, rect

def get_card_pile():
    location = os.path.join('resources/Top-Down/Cards', 'Card_DeckA-88x140.png')
    image = pygame.image.load(location)
    rect = pygame.Rect(88, 0, 88, 150)
    return image, rect

def get_button(type: ButtonType, pressed: bool = False):
    
    if pressed == False:
        frame = 0
    else:
        frame = 1
        
    match type:
        case ButtonType.BET1:
            location = os.path.join('resources', 'bet_1_button.png')
        case ButtonType.BET5:
            location = os.path.join('resources', 'bet_5_button.png')
        case ButtonType.BET10:
            location = os.path.join('resources', 'bet_10_button.png')
        case ButtonType.BETALLIN:
            location = os.path.join('resources', 'bet_all_in_button.png')
        case ButtonType.CALL:
            location = os.path.join('resources', 'call_button.png')
        case ButtonType.RAISE:
            location = os.path.join('resources', 'raise_button.png')
        case ButtonType.FOLD:
            location = os.path.join('resources', 'fold_button.png')
        case ButtonType.NEW:
            location = os.path.join('resources', 'new_button.png')
        case ButtonType.START:
            location = os.path.join('resources', 'start_button.png')
            
    image = pygame.image.load(location)
    
    if frame == 0:
        rect = pygame.Rect(0, 0, config['game']['button_width'], config['game']['button_height'])
    if frame == 1:
        rect = pygame.Rect(config['game']['button_width'], 0, config['game']['button_width'], config['game']['button_height'])
        
    return image, rect
        
@dataclass
class PlayingCard:
    """Class for cards"""
    
    def __init__(self, suit: Suit | None, number: CardNumber | None, npc: bool = False):
        self.npc = npc
        self.hidden = False
        
        if suit is not None:
            self.suit = suit
            
        if number is not None:
            self.number = number
            
        self.sprite = Card(self.suit, self.number.value, npc=self.npc)
            
    def set_npc(self, value: bool):
        self.npc = value
        self.sprite = Card(self.suit, self.number.value, npc=self.npc)
        
    def set_hidden(self, value: bool):
        self.hidden = value
        self.sprite.set_hidden(value)
        
    def tostring(self) -> str:
        match self.suit:
            case Suit.CLUB:
                symbol = "\u2660"
            case Suit.HEART:
                symbol = "\u2665"
            case Suit.DIAMOND:
                symbol = "\u2666"
            case Suit.SPADE:
                symbol = "\u2663"
                
        return f"{symbol} {self.number.name}"

@dataclass
class CardDeck:
    """Class for deck - 52 cards, 1 suit of each cardnumber"""
    
    def __init__(self):
        cards: list[PlayingCard] = []

        for suit in list(Suit):
            for number in list(CardNumber):
                card = PlayingCard(suit, number)
                cards.append(card)
                
        if len(cards) > 52:
            ValueError(f"Wrong amount of cards in generated deck: {len(cards)} should be 52!")
            
        self.cards = cards
        self.sprite = Deck()
        
    def shuffle(self):
        for _ in range(config['game']['random_counter']):
            random.shuffle(self.cards)
    
    def draw(self, npc: bool = False) -> PlayingCard:
        if len(self.cards) > 0:
            card = self.cards.pop()
            card.set_npc(npc)
        else:
            card = None
        return card

@dataclass
class Pair:
    """Class for Pairs"""
    
    def __init__(self, card_one: PlayingCard, card_two: PlayingCard):
        self.card_one = card_one
        self.card_two = card_two
        
    def __iter__(self):
        return iter(dataclasses.asdict(self).values())

class Card(pygame.sprite.Sprite): # DONE
    def __init__(self, suit: Suit, position: int, x: int | None = None, y: int | None = None, 
                 card1: bool = False, card2: bool = False, hidden: bool = False, npc: bool = False):
        super().__init__()
        
        self.npc = npc
        self.hidden = hidden
        self.suit = suit
        self.position = position
        self.clicked = False
        self.card1 = card1
        self.card2 = card2
        
        image, source_rect = get_card(suit, position, self.hidden)
        self.image = image
        self.source_rect = source_rect
        
        if card1:
            if self.npc:
                px, py = get_hand_1_pos_npc()
            else:
                px, py = get_hand_1_pos()
            self.x, self.y = px, py
        elif card2:
            if self.npc:
                px, py = get_hand_2_pos_npc()
            else:
                px, py = get_hand_2_pos()
            self.x, self.y = px, py
        else:
            self.x = x if x is not None else get_horizontal_middle(source_rect.width)
            self.y = y if y is not None else get_vertical_middle(source_rect.height)
            
        self.rect = pygame.Rect(self.x, self.y, source_rect.width, source_rect.height)
        self.set_hidden(self.npc)
        
    def set_npc(self, value: bool):
        self.npc = value
        self.hidden = value
        self.set_hidden(value)
        
        if value:
            if self.card1:
                px, py = get_hand_1_pos_npc()
                self.x, self.y = px, py
            if self.card2:
                px, py = get_hand_2_pos_npc()
                self.x, self.y = px, py
         
    def set_hidden(self, value: bool):
        image, source_rect = get_card(self.suit, self.position, value)
        self.image = image
        self.source_rect = source_rect
        self.rect = pygame.Rect(self.x, self.y, source_rect.width, source_rect.height)
        
    def set_x(self, x: int):
        self.x = x
        self.rect.x = x
        
    def set_y(self, y: int):
        self.y = y
        self.rect.y = y
        
    def set_card1(self, value: bool):
        self.card1 = value
        if value:
            if self.npc:
                px, py = get_hand_1_pos_npc()
            else:
                px, py = get_hand_1_pos()
            self.x, self.y = px, py
            self.rect.x, self.rect.y = px, py
        
    def set_card2(self, value: bool):
        self.card2 = value
        if value:
            if self.npc:
                px, py = get_hand_2_pos_npc()
            else:
                px, py = get_hand_2_pos()
            self.x, self.y = px, py
            self.rect.x, self.rect.y = px, py
            
    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = not self.clicked
                    
        if self.clicked:
            self.clicked = False

class Deck(pygame.sprite.Sprite): # DONE
    def __init__(self, x: int | None = None, y: int | None = None, centered: bool = True):
        super().__init__()
        
        image, source_rect = get_card_pile()
        self.image = image
        self.source_rect = source_rect
        self.clicked = False
        
        if centered:
            self.x = get_horizontal_middle(source_rect.width)
            self.y = get_vertical_middle(source_rect.height)
        else:
            self.x = x
            self.y = y
        
        self.rect = pygame.Rect(self.x, self.y, source_rect.width, source_rect.height)
        
    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = not self.clicked
                    
        if self.clicked:
            self.clicked = False
            
    def set_x(self, x: int):
        self.x = x
        self.rect.x = x

class Button(pygame.sprite.Sprite):
    def __init__(self, type: ButtonType, x: int | None = None, y: int | None = None):
        super().__init__()

        self.clicked = False
        self.image = None
        self.source_rect = None
        self.pressed = False
        self.type = type
        
        self.image, self.source_rect = get_button(type, self.pressed)
        
        match type:
            case ButtonType.BET1:
                if x is None:
                    horizontal_middle = get_horizontal_middle(self.source_rect.width)
                    self.x = horizontal_middle + (horizontal_middle // 2)
                else:
                    self.x = x
                if y is None:
                    self.y = (height() // 4) * 3.5
                else:
                    self.y = y
                    
            case ButtonType.BET5:
                if x is None:
                    horizontal_middle = get_horizontal_middle(self.source_rect.width)
                    self.x = horizontal_middle + (horizontal_middle // 2) + config['game']['button_width']
                else:
                    self.x = x
                if y is None:
                    self.y = (height() // 4) * 3.5
                else:
                    self.y = y
                    
            case ButtonType.BET10:
                if x is None:
                    horizontal_middle = get_horizontal_middle(self.source_rect.width)
                    self.x = horizontal_middle + (horizontal_middle // 2) + (config['game']['button_width'] * 2)
                else:
                    self.x = x
                if y is None:
                    self.y = (height() // 4) * 3.5
                else:
                    self.y = y
                    
            case ButtonType.BETALLIN:
                if x is None:
                    horizontal_middle = get_horizontal_middle(self.source_rect.width)
                    self.x = horizontal_middle + (horizontal_middle // 2) + config['game']['button_width']
                else:
                    self.x = x
                if y is None:
                    self.y = (height() // 4) * 2.5
                else:
                    self.y = y
                    
            case ButtonType.CALL:
                if x is None:
                    horizontal_middle = get_horizontal_middle(self.source_rect.width)
                    self.x = horizontal_middle + (horizontal_middle // 1.5) - config['game']['button_width'] - 10
                else:
                    self.x = x
                if y is None:
                    self.y = (height() // 4) * 3
                else:
                    self.y = y
                    
            case ButtonType.RAISE:
                if x is None:
                    horizontal_middle = get_horizontal_middle(self.source_rect.width)
                    self.x = horizontal_middle + (horizontal_middle // 1.5)
                else:
                    self.x = x
                if y is None:
                    self.y = (height() // 4) * 3
                else:
                    self.y = y
                    
            case ButtonType.FOLD:
                if x is None:
                    horizontal_middle = get_horizontal_middle(self.source_rect.width)
                    self.x = horizontal_middle + (horizontal_middle // 1.5) + config['game']['button_width'] + 10
                else:
                    self.x = x
                if y is None:
                    self.y = (height() // 4) * 3
                else:
                    self.y = y
            
            case ButtonType.NEW:
                if x is None:
                    horizontal_middle = get_horizontal_middle(self.source_rect.width)
                    self.x = horizontal_middle + (horizontal_middle // 1.5)
                else:
                    self.x = x
                if y is None:
                    self.y = (height() // 4) * 3
                else:
                    self.y = y
                    
            case ButtonType.START:
                if x is None:
                    horizontal_middle = get_horizontal_middle(self.source_rect.width)
                    self.x = horizontal_middle
                else:
                    self.x = x
                if y is None:
                    self.y = (height() // 4) * 3
                else:
                    self.y = y
                    
        self.rect = pygame.Rect(self.x, self.y, self.source_rect.width, self.source_rect.height)
        
    def update(self, event_list):
        global START_NEW, TITLESCREEN
        disabled = PLAYER.hasbet
            
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = not self.clicked
        
        if self.clicked == False and not disabled and self.pressed == True:
            self.pressed = not self.pressed
            self.image, self.source_rect = get_button(self.type, self.pressed)
            self.rect = pygame.Rect(self.x, self.y, self.source_rect.width, self.source_rect.height)
            
        if self.clicked and not disabled:
            self.pressed = not self.pressed
            self.image, self.source_rect = get_button(self.type, self.pressed)
            self.rect = pygame.Rect(self.x, self.y, self.source_rect.width, self.source_rect.height)
            
            if self.type == ButtonType.BET1:
                PLAYER.bet(chips=1)
            elif self.type == ButtonType.BET5:
                PLAYER.bet(chips=5)
            elif self.type == ButtonType.BET10:
                PLAYER.bet(chips=10)
            elif self.type == ButtonType.BETALLIN:
                PLAYER.bet(chips=-1)
            elif self.type == ButtonType.CALL:
                PLAYER.call()
            elif self.type == ButtonType.RAISE:
                PLAYER.raiseFunction()
            elif self.type == ButtonType.FOLD:
                PLAYER.fold()
            elif self.type == ButtonType.NEW:
                start(START_CHIPS_PLAYER, START_CHIPS_NPC)
                START_NEW = True
            elif self.type == ButtonType.START:
                start(START_CHIPS_PLAYER, START_CHIPS_NPC)
                TITLESCREEN = False
                START_NEW = True
                
            self.clicked = False

class Player:
    def __init__(self, npc: bool = False, chips: int = 100):
        self.chips = chips
        self.hasbet = False
        self.hascards = False
        self.card1: PlayingCard = None
        self.card2: PlayingCard = None
        self.npc = npc
        self.lastbet = 0
        self.totalbet = 0
        self.hasante = False
        
    def fold(self):
        global ROUND_WINNER, ROUND_OVER
        if self.get_opponent().npc:
            ROUND_WINNER = "player_fold"
        else:
            ROUND_WINNER = "npc_fold"

        ROUND_OVER = True
        
    def call(self):
        last_bet = self.get_opponent().get_last_bet()
        if self.chips - last_bet >= 0:
            self.bet(last_bet)
            
    def raiseFunction(self):
        last_bet = self.get_opponent().get_last_bet()
        if self.chips - (last_bet + 10) >= 0:
            self.bet(last_bet + 10)
        
    def get_opponent(self):
        if self.npc:
            return PLAYER
        else:
            return NPC
            
    def bet(self, chips: int):
        
        if self.hasbet == False:
            if chips == -1:  # All in
                chips = self.chips
            self.chips -= chips
            self.lastbet = chips
            self.totalbet += chips
            self.hasbet = True
            global POT
            POT += chips
        
    def get_chips(self):
        return self.chips
        
    def get_last_bet(self):
        return self.lastbet
        
    def get_has_bet(self):
        return self.hasbet
        
    def set_has_bet(self, value: bool):
        self.hasbet = value
        
    def set_hascards(self, value: bool):
        self.hascards = value
        
    def think(self):
        return 1

# Global game state
GAMESTATE = GameState.DRAW
PLAYER = Player(chips=100)
NPC = Player(npc=True, chips=100)
DECK = None
HOUSE_CARDS = []
POT = 0
ROUND_OVER = False
ROUND_WINNER = None
ROUND_WINNER_REASON = None
DEALER = config['game']['player_id']
START_CHIPS_PLAYER = 100
START_CHIPS_NPC = 100
START_NEW = False

def get_gamestate():
    return GAMESTATE

def set_gamestate(state: GameState):
    global GAMESTATE
    GAMESTATE = state

def get_player():
    return PLAYER

def get_npc():
    return NPC

def get_deck():
    return DECK

def create_deck():
    global DECK
    DECK = CardDeck()

def get_house_cards():
    return HOUSE_CARDS

def append_house_card(card):
    HOUSE_CARDS.append(card)

def get_pot():
    return POT

def get_round_over():
    return ROUND_OVER

def set_round_over(value: bool):
    global ROUND_OVER
    ROUND_OVER = value

def get_round_winner():
    return ROUND_WINNER

def get_dealer():
    return DEALER

def start(player_chips: int = 100, npc_chips: int = 100, delay: bool = False): 
    global PLAYER, NPC, HOUSE_CARDS, POT, ROUND_OVER, GAMESTATE
    
    if not delay:
        ROUND_OVER = False
        
    PLAYER = Player(chips=START_CHIPS_PLAYER)
    NPC = Player(npc=True, chips=START_CHIPS_NPC)
    HOUSE_CARDS = []
    POT = 0
    
    GAMESTATE = GameState.DRAW
    create_deck()

def calcualte_winner():
    global ROUND_WINNER, ROUND_OVER, ROUND_WINNER_REASON
    
    house_cards = get_house_cards()
    player_cards = [get_player().card1, get_player().card2]
    npc_cards = [get_npc().card1, get_npc().card2]
    
    ROUND_WINNER, ROUND_WINNER_REASON = get_winner(player_cards, npc_cards, house_cards)
    ROUND_OVER = True

######## WINNER LOGIC ########

# TODO:
# - Incorporate suit value into value calculations (happens sometimes but not everywhere)
# - Fix get_three_of_a_kind_value
# - Fix get_straight

#### HELPER FUNCTIONS ####

def is_card_in_house(card: PlayingCard, house: list[PlayingCard]) -> bool:
    return (card in house)

def get_card_value(card: PlayingCard) -> int:
    """Returns a PlayingCard's value as an int

    Args:
        card (PlayingCard): A PlayingCard

    Returns:
        int: A PlayingCard's value
    """
    
    return 14 if card.number == CardNumber.ACE else card.number.value

def get_card_value_via_suit(card: PlayingCard) -> int:
    return card.suit.value

def get_best_hand(hand: list[PlayingCard], house: list[PlayingCard]) -> list[PlayingCard]:
    """Returns best hand from given hand and house cards

    Args:
        hand (list[PlayingCard]): Player's hand
        house (list[PlayingCard]): House cards

    Returns:
        list[PlayingCard]: The player's best hand
    """
    
    pool = hand.copy() + house.copy()
    
    pool.sort(key=get_card_value, reverse=True)
    
    return pool[:5]

def get_card_number_count(number: CardNumber, pool: list[PlayingCard]) -> int:
    count = 0
    
    for c in pool:
        if c.number == number:
            count += 1
            
    return count

def get_card_suit_count(suit: Suit, pool: list[PlayingCard]) -> int:
    count = 0
    
    for c in pool:
        if c.suit == suit:
            count += 1
            
    return count

#### VALUE CALCUALATION FUNCTIONS ####

def get_cards_value_generic(generic_list: list[PlayingCard]) -> int:
    value = 0
    
    for card in generic_list:
        value += get_card_value(card)
        
    return value

def get_three_of_a_kind_value(three_of_a_kind: list[PlayingCard]) -> int:
    three_of_a_kind_value = 0

    # TODO: Warning: I can't figure out why I have to unpack three_of_a_kind once to access the card list?
    for lst in three_of_a_kind:
        for card in lst:
            card_value = get_card_value(card)
            three_of_a_kind_value += card_value

    return three_of_a_kind_value

def get_two_pair_value(two_pair: list[Pair]) -> int:
    
    two_pair_value = 0
    for pair in two_pair:
        pair_value = 0
            
        for card in pair:
            card_value = get_card_value(card)
            pair_value += card_value
            
        two_pair_value += pair_value
        
    return two_pair_value

def get_pair_value(pair: Pair) -> int:
    
    pair_value = 0
    
    card_one_value = get_card_value(pair.card_one)
    card_two_value = get_card_value(pair.card_two)
    
    pair_value += card_one_value
    pair_value += card_two_value
    
    return pair_value

#### POKER HAND CALCULATION FUNCTIONS ####

def get_four_of_a_kind(hand: list[PlayingCard], house: list[PlayingCard]) -> list[PlayingCard]:
    pool = hand.copy() + house.copy()
    
    found: list[list[PlayingCard]] = []
    
    for number in CardNumber:
        count = get_card_number_count(number, pool)
        
        if count > 3 and count < 5:
            
            group = []
            
            for card in pool:
                if card.number == number:
                    group.append(card)
                    
            found.append(group)
    
    if found == []:
        return None
    
    return found

def get_fullhouse(hand: list[PlayingCard], house: list[PlayingCard]) -> list[PlayingCard]:
    
    three_of_a_kind = get_three_of_a_kind(hand, house)
    
    if three_of_a_kind == None:
        return None
    
    if three_of_a_kind[0] == None:
        return None
    
    pairs = get_pairs(hand, house)
    
    if pairs == None:
        return None
    
    highest_pair = pairs[0]
    
    if highest_pair.card_one in three_of_a_kind[0]:
        highest_pair = pairs[1]
        
    if highest_pair == None:
        return None
    
    fullhouse = [highest_pair.card_one, highest_pair.card_two, three_of_a_kind[0][0], three_of_a_kind[0][1], three_of_a_kind[0][2]]
    
    return fullhouse

def get_flush(hand: list[PlayingCard], house: list[PlayingCard]) -> list[PlayingCard]:
    pool = hand.copy() + house.copy()
    
    pool.sort(key=get_card_value_via_suit)
    
    found: dict[int, list[PlayingCard]] = {} # flush value, flush
    
    for suit in Suit:
        count = get_card_suit_count(suit, pool)
        
        if count > 4:
            group: list[PlayingCard] = []
            
            for card in pool:
                if card.suit == suit:
                    group.append(card)
                    
            found[get_cards_value_generic(group)] = group
            
    highscore = -1
    for value in found.keys():
        if value > highscore:
            highscore = value
    
    if highscore != -1:
        return found[highscore]
    else:
        return None
    
def get_straight(hand: list[PlayingCard], house: list[PlayingCard]) -> list[PlayingCard]:
    
    # TODO: Implement high ace calculations, this only works with low aces
    
    pool = hand.copy() + house.copy()

    pool.sort(key=get_card_value)
    
    straights: dict[int, list[PlayingCard]] = {} # straight value, straight playingcard list
    
    # remove duplicate suits
    cards: dict[CardNumber, PlayingCard] = {}
    
    for card in pool:
        result = cards.get(card.number)
        
        if not result or get_card_value_via_suit(result) < get_card_value_via_suit(card):
            cards[card.number] = card
            
    for c in cards.values():
        try:
            if cards.get(CardNumber(c.number.value + 1)).number.value - c.number.value > 1:
                continue
            elif cards.get(CardNumber(c.number.value + 2)).number.value - cards.get(CardNumber(c.number.value + 1)).number.value > 1:
                continue
            elif cards.get(CardNumber(c.number.value + 3)).number.value - cards.get(CardNumber(c.number.value + 2)).number.value > 1:
                continue
            elif cards.get(CardNumber(c.number.value + 4)).number.value - cards.get(CardNumber(c.number.value + 3)).number.value > 1:
                continue
        except AttributeError:
            continue # next card does not exist
        except ValueError as ve:
            if "is not a valid CardNumber" in str(ve):
                continue # next card does not exist
            
        result = []
        
        for i in range(5):
            result.append(cards.get(CardNumber(c.number.value + i)))
            
        straights[get_cards_value_generic(result)] = result
        
    highscore = -1
    for value in straights.keys():
        if value > highscore:
            highscore = value
    
    if highscore != -1:
        return straights[highscore]
    else:
        return None

def get_three_of_a_kind(hand: list[PlayingCard], house: list[PlayingCard]) -> list[list[PlayingCard]]:
    pool = hand.copy() + house.copy()
    
    found = []
    
    for number in CardNumber:
        count = get_card_number_count(number, pool)
        
        if count > 2 and count < 4:
            
            group = []
            
            for card in pool:
                if card.number == number:
                    group.append(card)
                    
            found.append(group)
    
    if found == []:
        return None
    else:
        return found

def get_two_pair(hand: list[PlayingCard], house: list[PlayingCard]) -> list[Pair] | None:
    """Returns any two pairs from given hand and house cards

    Args:
        hand (list[PlayingCard]): _description_
        house (list[PlayingCard]): _description_

    Returns:
        list[Pair]: _description_
    """
    
    pool = hand.copy() + house.copy()
    
    # Group cards by their number
    card_groups = {}
    
    for card in pool:
        if card.number not in card_groups:
            card_groups[card.number] = []
        card_groups[card.number].append(card)
    
    # Find all ranks that have at least 2 cards (pairs)
    pair_ranks = []
    for rank, cards in card_groups.items():
        if len(cards) >= 2:
            pair_ranks.append((rank, cards))
    
    # If we don't have at least 2 different ranks with pairs, return None
    if len(pair_ranks) < 2:
        return None
    
    # Sort by card value (highest first)
    pair_ranks.sort(key=lambda x: get_card_value(x[1][0]), reverse=True)
    
    # Create pairs from the two highest ranks
    result = []
    for i in range(2):
        rank, cards = pair_ranks[i]
        # Take the first two cards of this rank to form a pair
        result.append(Pair(cards[0], cards[1]))
    
    if result == []:
        return None
    else:
        return result

def get_pairs(hand: list[PlayingCard], house: list[PlayingCard]) -> list[Pair]:
    
    pool = hand.copy() + house.copy()
    
    pairs: list[Pair] = []
    
    # get pairs
    for c1 in pool:
        for c2 in pool:
            c1num = c1.number
            c2num = c2.number
            
            if c1num == c2num and c1.suit != c2.suit:
                pairs.append(Pair(c1, c2))
                
    # get highest pair
    
    if len(pairs) < 1:
        return None
    
    pairs.sort(key=get_pair_value)
    
    return pairs
    
def get_pair(hand: list[PlayingCard], house: list[PlayingCard]) -> Pair:
    """Return's highest pair available (including house card pairs)

    Args:
        hand (list[PlayingCard]): A Player's hand
        house (list[PlayingCard]): An NPC's hand

    Returns:
        tuple[PlayingCard, PlayingCard]: The highest pair available
    """
    
    pool = hand.copy() + house.copy()
    
    pairs: list[Pair] = []
    
    # get pairs
    for c1 in pool:
        for c2 in pool:
            c1num = c1.number
            c2num = c2.number
            
            if c1num == c2num and c1.suit != c2.suit:
                pairs.append(Pair(c1, c2))
                
    # get highest pair
    
    if len(pairs) < 1:
        return None
    
    highest = 0
    winning_pair: Pair = None
    
    for pair in pairs:
        pair_value = get_card_value(pair.card_one) + get_card_value(pair.card_two)
        
        if pair_value > highest:
            winning_pair = pair
            
    if winning_pair != None:
        return winning_pair
    else:
        return None
    
#### WINNER CALCULATION FUNCITONS ####

def get_four_of_a_kind_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]):
    player_four_of_a_kind = get_four_of_a_kind(player_hand, house)
    npc_four_of_a_kind = get_four_of_a_kind(npc_hand, house)
    
    if player_four_of_a_kind == None and npc_four_of_a_kind != None:
        return WinResult.NPC_WIN, "FOUR OF A KIND"
    elif npc_four_of_a_kind == None and player_four_of_a_kind != None:
        return WinResult.PLAYER_WIN, "FOUR OF A KIND"
    elif player_four_of_a_kind == None and npc_four_of_a_kind == None:
        return None, None
    else:
        player_four_of_a_kind_value = get_cards_value_generic(player_four_of_a_kind)
        npc_four_of_a_kind_value = get_cards_value_generic(npc_four_of_a_kind)
            
        if player_four_of_a_kind_value == npc_four_of_a_kind_value:
            return WinResult.TIE, "FOUR OF A KIND"
        elif player_four_of_a_kind_value > npc_four_of_a_kind_value:
            return WinResult.PLAYER_WIN, "FOUR OF A KIND"
        else:
            return WinResult.NPC_WIN, "FOUR OF A KIND"
        
def get_fullhouse_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]):
    player_fullhouse = get_fullhouse(player_hand, house)
    npc_fullhouse = get_fullhouse(npc_hand, house)
        
    if player_fullhouse == None and npc_fullhouse != None:
        return WinResult.NPC_WIN, "FULLHOUSE"
    elif npc_fullhouse == None and player_fullhouse != None:
        print("player fullhouse:")
        for c in player_fullhouse:
            print(c.tostring(), end=", ")
        return WinResult.PLAYER_WIN, "FULLHOUSE"
    elif player_fullhouse == None and npc_fullhouse == None:
        return None, None
    else:
        print("player fullhouse:")
        for c in player_fullhouse:
            print(c.tostring(), end=", ")
            
        player_fullhouse_value = get_cards_value_generic(player_fullhouse)
        npc_fullhouse_value = get_cards_value_generic(npc_fullhouse)
        
        if player_fullhouse_value == npc_fullhouse_value:
            return WinResult.TIE, "FULLHOUSE"
        elif player_fullhouse_value > npc_fullhouse_value:
            return WinResult.PLAYER_WIN, "FULLHOUSE"
        else:
            return WinResult.NPC_WIN, "FULLHOUSE"
        
def get_flush_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]):
    player_flush = get_flush(player_hand, house)
    npc_flush = get_flush(npc_hand, house)
    
    if player_flush == None and npc_flush != None:
        return WinResult.NPC_WIN, "FLUSH"
    elif npc_flush == None and player_flush != None:
        return WinResult.PLAYER_WIN, "FLUSH"
    elif player_flush == None and npc_flush == None:
        return None, None
    else:
        player_flush_value = get_cards_value_generic(player_flush)
        npc_flush_value = get_cards_value_generic(npc_flush)
        
        if player_flush_value == npc_flush_value:
            return WinResult.TIE, "FLUSH"
        elif player_flush_value > npc_flush_value:
            return WinResult.PLAYER_WIN, "FLUSH"
        else:
            return WinResult.NPC_WIN, "FLUSH"
        
def get_straight_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]):
    player_straight = get_straight(player_hand, house)
    npc_straight = get_straight(npc_hand, house)
    
    if player_straight == None and npc_straight != None:
        return WinResult.NPC_WIN, "STRAIGHT"
    elif npc_straight == None and player_straight != None:
        return WinResult.PLAYER_WIN, "STRAIGHT"
    elif player_straight == None and npc_straight == None:
        return None, None
    else:
        player_straight_value = get_cards_value_generic(player_straight)
        npc_straight_value = get_cards_value_generic(npc_straight)
        
        if player_straight_value == npc_straight_value:
            return WinResult.TIE, "STRAIGHT"
        elif player_straight_value > npc_straight_value:
            return WinResult.PLAYER_WIN, "STRAIGHT"
        else:
            return WinResult.NPC_WIN, "STRAIGHT"
        
def get_three_of_a_kind_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]):
    player_three_of_a_kind = get_three_of_a_kind(player_hand, house)
    npc_three_of_a_kind = get_three_of_a_kind(npc_hand, house)
    
    if player_three_of_a_kind == None and npc_three_of_a_kind != None:
        return WinResult.NPC_WIN, "THREE OF A KIND"
    elif npc_three_of_a_kind == None and player_three_of_a_kind != None:
        return WinResult.PLAYER_WIN, "THREE OF A KIND"
    elif player_three_of_a_kind == None and npc_three_of_a_kind == None:
        return None, None
    else:
        player_three_of_a_kind_value = get_three_of_a_kind_value(player_three_of_a_kind)
        npc_three_of_a_kind_value = get_three_of_a_kind_value(npc_three_of_a_kind)
            
        if player_three_of_a_kind_value == npc_three_of_a_kind_value:
            return WinResult.TIE, "THREE OF A KIND"
        elif player_three_of_a_kind_value > npc_three_of_a_kind_value:
            return WinResult.PLAYER_WIN, "THREE OF A KIND"
        else:
            return WinResult.NPC_WIN, "THREE OF A KIND"

def get_two_pair_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]) -> WinResult | None:

    player_two_pair = get_two_pair(player_hand, house)
    npc_two_pair = get_two_pair(npc_hand, house)
    
    if player_two_pair == None and npc_two_pair != None:
        return WinResult.NPC_WIN, "TWO PAIR"
    elif npc_two_pair == None and player_two_pair != None:
        return WinResult.PLAYER_WIN, "TWO PAIR"
    elif player_two_pair == None and npc_two_pair == None:
        return None, None
    else:
        player_two_pair_value = get_two_pair_value(player_two_pair)
        npc_two_pair_value = get_two_pair_value(npc_two_pair)
            
        if player_two_pair_value == npc_two_pair_value:
            return WinResult.TIE, "TWO PAIR"
        elif player_two_pair_value > npc_two_pair_value:
            return WinResult.PLAYER_WIN, "TWO PAIR"
        else:
            return WinResult.NPC_WIN, "TWO PAIR"

def get_pair_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]) -> WinResult | None:
    
    player_pair = get_pair(player_hand, house)
    npc_pair = get_pair(npc_hand, house)
    
    if player_pair == None and npc_pair != None:
        return WinResult.NPC_WIN, "PAIR"
    elif npc_pair == None and player_pair != None:
        return WinResult.PLAYER_WIN, "PAIR"
    elif player_pair == None and npc_pair == None:
        return None, None
    else:
        player_value = get_card_value(player_pair.card_one) + get_card_value(player_pair.card_two)
        npc_value = get_card_value(npc_pair.card_one) + get_card_value(npc_pair.card_two)
        
        if player_pair in house and npc_pair in house:
            return None
        elif player_value == npc_value:
            return WinResult.TIE, "PAIR"
        elif player_value > npc_value:
            return WinResult.PLAYER_WIN, "PAIR"
        else:
            return WinResult.NPC_WIN, "PAIR"
    
def get_highcard_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]) -> WinResult:
    
    players_best = get_best_hand(player_hand, house)
    npc_best = get_best_hand(npc_hand, house)

    for i in range(5):
        pcard = players_best[i]
        ncard = npc_best[i]
        
        if get_card_value(pcard) > get_card_value(ncard):
            return WinResult.PLAYER_WIN, "HIGHCARD"
        elif get_card_value(pcard) < get_card_value(ncard):
            return WinResult.NPC_WIN, "HIGHCARD"
        elif get_card_value(pcard) == get_card_value(ncard):
            continue
        
    # if the entire hand is equal
    return WinResult.TIE, "HIGHCARD"

def get_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]) -> tuple[WinResult, str]:
    
    # winner, reason = get_royale_flush_winner(player_hand, npc_hand, house)
    
    # if winner != None:
    #     return winner, reason
    
    # winner, reason = get_straight_flush_winner(player_hand, npc_hand, house)
    
    # if winner != None:
    #     return winner, reason
    
    winner, reason = get_four_of_a_kind_winner(player_hand, npc_hand, house)
    
    if winner != None:
       print(winner, reason)
       return winner, reason
    
    winner, reason = get_fullhouse_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = get_flush_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = get_straight_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = get_three_of_a_kind_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = get_two_pair_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = get_pair_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = get_highcard_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    return None, None

##############################


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("coker - crappy poker")

clock = pygame.time.Clock()
GAME_FONT = pygame.freetype.Font("resources/Pixelon.ttf", 32)
TITLE_FONT_LARGE = pygame.freetype.Font("resources/Pixelon.ttf", 64)

START_NEW = True
TITLESCREEN = True

if __name__ != '__main__':
    running = False
else:
    running = True

# Main game loop
while running:
    clock.tick(60)
    
    event_list = pygame.event.get()
    
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    if TITLESCREEN:
        sprites_list = pygame.sprite.Group()
        
        button_sprites = []
        for button in list(ButtonType):
            button_sprites.append(Button(type=button))
        
        sprites_list.add(button_sprites[ButtonType.START.value])
        
        sprites_list.update(event_list)
        
        screen.fill(config['game']['background_color'])
        
        for sprite in sprites_list:
            screen.blit(sprite.image, (sprite.x, sprite.y), sprite.source_rect)
            
        TITLE_FONT_LARGE.render_to(screen, (width() // 2 - 80, height() // 4), "coker", (255, 255, 255))
        GAME_FONT.render_to(screen, (width() // 2 - 105, height() // 4 + 60), "crappy poker", (255, 255, 255))
        
    else:
        if START_NEW:
            START_NEW = False
            sprites_list = pygame.sprite.Group()

            button_sprites = []
            for button in list(ButtonType):
                button_sprites.append(Button(type=button))

            start()
            current_deck = get_deck()
            sprites_list.add(current_deck.sprite)

            if get_dealer() == config['game']['player_id']:
                sprites_list.add(button_sprites[ButtonType.RAISE.value])
                sprites_list.add(button_sprites[ButtonType.CALL.value])
                sprites_list.add(button_sprites[ButtonType.FOLD.value])
            else:
                sprites_list.add(button_sprites[ButtonType.BET1.value])
                sprites_list.add(button_sprites[ButtonType.BET5.value])
                sprites_list.add(button_sprites[ButtonType.BET10.value])
                sprites_list.add(button_sprites[ButtonType.BETALLIN.value])
                sprites_list.add(button_sprites[ButtonType.FOLD.value])
        
        sprites_list.update(event_list)
        
        screen.fill(config['game']['background_color'])
        
        for sprite in sprites_list:
            screen.blit(sprite.image, (sprite.x, sprite.y), sprite.source_rect)
                
        if not get_round_over():
            
            if get_dealer() == config['game']['player_id']:
                GAME_FONT.render_to(screen, (width() * 0.125, height() * 0.05 + 50), "you're dealing", (255, 255, 255))
            else:
                GAME_FONT.render_to(screen, (width() * 0.125, height() * 0.05 + 50), "the npc is dealing", (255, 255, 255))
            
            player = get_player()
            npc = get_npc()
            
            GAME_FONT.render_to(screen, (width() * 0.7, height() * 0.05), f"{npc.get_chips()} chips", (255, 255, 255))
            
            if npc.get_last_bet() > 0:
                if npc.get_last_bet() == 1:
                    message = f"npc bet {npc.get_last_bet()} chip"
                else:
                    message = f"npc bet {npc.get_last_bet()} chips"
                GAME_FONT.render_to(screen, (width() * 0.7, height() * 0.05 + 50), message, (255, 255, 255))
            
            GAME_FONT.render_to(screen, (width() * 0.15, height() * 0.825), f"{player.get_chips()} chips", (255, 255, 255))
            
            if player.get_last_bet() > 0:
                if player.get_last_bet() == 1:
                    message = f"you bet {player.get_last_bet()} chip"
                else:
                    message = f"you bet {player.get_last_bet()} chips"
                GAME_FONT.render_to(screen, (width() * 0.15, height() * 0.825 + 50), message, (255, 255, 255))
                
            if get_pot() == 1:
                potm = f"{get_pot()} chip"
            else:
                potm = f"{get_pot()} chips"
            GAME_FONT.render_to(screen, (get_deck().sprite.x + 200, height() * 0.45), potm, (255, 255, 255))
            
            if get_gamestate() == GameState.DRAW:
                if not get_player().hascards:
                    
                    if get_deck() is None:
                        create_deck()
                    
                    current_deck = get_deck()
                    sprites_list.add(current_deck.sprite)

                    current_deck.shuffle()
                    
                    # Draw cards in turn
                    player.card1 = current_deck.draw()
                    npc.card1 = current_deck.draw(npc=True)
                    player.card2 = current_deck.draw()
                    npc.card2 = current_deck.draw(npc=True)
                    
                    player.card1.sprite.set_card1(True)
                    player.card2.sprite.set_card2(True)
                    
                    npc.card1.sprite.set_card1(True)
                    npc.card2.sprite.set_card2(True)
                    
                    sprites_list.add(player.card1.sprite)
                    sprites_list.add(player.card2.sprite)
                    sprites_list.add(npc.card1.sprite)
                    sprites_list.add(npc.card2.sprite)
                    
                    player.set_hascards(True)
                    npc.set_hascards(True)
                    
                    set_gamestate(GameState.BETTING)
                    
            if get_gamestate() == GameState.BETTING:
                    
                if len(get_house_cards()) > 5 and npc.get_has_bet() == False:
                    raise Exception("Should not go past 4 betting rounds!")
                
                npc_bet = npc.think()
                npc.bet(chips=npc_bet)
                
                if player.get_has_bet() == True and npc.get_has_bet() == True:
                    npc.set_has_bet(False)
                    player.set_has_bet(False)
                    
                    if len(get_house_cards()) == 5:
                        calcualte_winner()
                    else:
                        set_gamestate(GameState.HOUSECARDS)
                    
            if get_gamestate() == GameState.HOUSECARDS:
                
                if len(get_house_cards()) == 0:
                    while len(get_house_cards()) < 3:
                        card = get_deck().draw()
                        append_house_card(card)
                        
                elif len(get_house_cards()) == 3:
                    burn_card = get_deck().draw()  # burn and turn
                    card = get_deck().draw()
                    append_house_card(card)
                        
                elif len(get_house_cards()) == 4:
                    burn_card = get_deck().draw()  # burn and turn
                    card = get_deck().draw()
                    append_house_card(card)
                
                # Position house cards
                if len(get_house_cards()) == 3:
                    card2x = get_horizontal_middle(config['game']['card_width'])
                    card2y = get_vertical_middle(config['game']['card_height'])
                        
                    card1x = card2x - config['game']['card_width'] - 10
                    card1y = card2y
                    
                    card3x = card2x + config['game']['card_width'] + 10
                    card3y = card2y
                
                    current_decknewx = card3x + config['game']['card_width'] + 20
                    
                elif len(get_house_cards()) == 4:
                    middle_x = get_horizontal_middle(config['game']['card_width'])
                    middle_y = get_vertical_middle(config['game']['card_height'])
                    
                    gap = 10
                    total_width = (config['game']['card_width'] * 4) + (gap * 3)
                    start_x = (width() - total_width) // 2
                    
                    card1x = start_x
                    card1y = middle_y
                    
                    card2x = start_x + config['game']['card_width'] + gap
                    card2y = middle_y
                    
                    card3x = start_x + (config['game']['card_width'] + gap) * 2
                    card3y = middle_y
                    
                    card4x = start_x + (config['game']['card_width'] + gap) * 3
                    card4y = middle_y
                    
                    current_decknewx = card4x + config['game']['card_width'] + 20
                    
                elif len(get_house_cards()) == 5:
                    middle_x = get_horizontal_middle(config['game']['card_width'])
                    middle_y = get_vertical_middle(config['game']['card_height'])
                    
                    card3x = middle_x
                    card3y = middle_y
                    
                    card2x = card3x - config['game']['card_width'] - 5
                    card2y = middle_y
                    
                    card4x = card3x + config['game']['card_width'] + 5
                    card4y = middle_y
                    
                    card1x = card2x - config['game']['card_width'] - 5
                    card1y = middle_y
                    
                    card5x = card4x + config['game']['card_width'] + 5
                    card5y = middle_y
                    
                    current_decknewx = card5x + config['game']['card_width'] + 20
                    
                i = 0
                for c in get_house_cards():
                    
                    if i == 0:
                        c.sprite.set_x(card1x)
                        c.sprite.set_y(card1y)
                        
                    if i == 1:
                        c.sprite.set_x(card2x)
                        c.sprite.set_y(card2y)
                    if i == 2:
                        c.sprite.set_x(card3x)
                        c.sprite.set_y(card3y)
                        
                    if i == 3:
                        c.sprite.set_x(card4x)
                        c.sprite.set_y(card4y)
                        
                    if i == 4:
                        c.sprite.set_x(card5x)
                        c.sprite.set_y(card5y)
                        
                    if i > 4:
                        raise ValueError("how do we have more than 5 house cards...")
                        
                    sprites_list.add(c.sprite)
                    
                    i += 1
                    
                current_deck.sprite.set_x(current_decknewx)
                
                set_gamestate(GameState.BETTING)
                
            if get_gamestate() == GameState.END:
                screen.fill(config['game']['background_color'])
                
                winner = get_round_winner()
                
                if ROUND_WINNER_REASON != None:
                    reason = ROUND_WINNER_REASON
                else:
                    reason = "N/A"
                
                match reason:
                    case "HIGHCARD":
                        match winner:
                            case WinResult.TIE:
                                message = "You and the NPC had equal value hands!"
                            case WinResult.PLAYER_WIN:
                                message = "You had a high card that beat the NPC's hand!"
                            case WinResult.NPC_WIN:
                                message = "The NPC had a high card that beat your hand!"
                            case WinResult.NO_WIN:
                                message = ":("
                    case "PAIR":
                        match winner:
                            case WinResult.TIE:
                                message = "You and the NPC had equal value hands!"
                            case WinResult.PLAYER_WIN:
                                message = "You had a pair that beat the NPC's hand!"
                            case WinResult.NPC_WIN:
                                message = "The NPC had a pair that beat your hand!"
                            case WinResult.NO_WIN:
                                message = ":("
                    case "TWO PAIR":
                        match winner:
                            case WinResult.TIE:
                                message = "You and the NPC had equal value hands!"
                            case WinResult.PLAYER_WIN:
                                message = "You had a set of pairs that beat the NPC's hand!"
                            case WinResult.NPC_WIN:
                                message = "The NPC had a set of pairs that beat your hand!"
                            case WinResult.NO_WIN:
                                message = ":("
                    case "THREE OF A KIND":
                        match winner:
                            case WinResult.TIE:
                                message = "You and the NPC had equal value hands!"
                            case WinResult.PLAYER_WIN:
                                message = "You had a three of a kind that beat the NPC's hand!"
                            case WinResult.NPC_WIN:
                                message = "The NPC had a three of a kind that beat your hand!"
                            case WinResult.NO_WIN:
                                message = ":("
                    case "STRAIGHT":
                        match winner:
                            case WinResult.TIE:
                                message = "You and the NPC had equal value hands!"
                            case WinResult.PLAYER_WIN:
                                message = "You had a straight that beat the NPC's hand!"
                            case WinResult.NPC_WIN:
                                message = "The NPC had a straight that beat your hand!"
                            case WinResult.NO_WIN:
                                message = ":("
                    case "FLUSH":
                        match winner:
                            case WinResult.TIE:
                                message = "You and the NPC had equal value hands!"
                            case WinResult.PLAYER_WIN:
                                message = "You had a flush that beat the NPC's hand!"
                            case WinResult.NPC_WIN:
                                message = "The NPC had a flush that beat your hand!"
                            case WinResult.NO_WIN:
                                message = ":("
                    case "FULLHOUSE":
                        match winner:
                            case WinResult.TIE:
                                message = "You and the NPC had equal value hands!"
                            case WinResult.PLAYER_WIN:
                                message = "You had a full house that beat the NPC's hand!"
                            case WinResult.NPC_WIN:
                                message = "The NPC had a full house that beat your hand!"
                            case WinResult.NO_WIN:
                                message = ":("
                    case "FOUR OF A KIND":
                        match winner:
                            case WinResult.TIE:
                                message = "You and the NPC had equal value hands!"
                            case WinResult.PLAYER_WIN:
                                message = "You had a four of a kind that beat the NPC's hand!"
                            case WinResult.NPC_WIN:
                                message = "The NPC had a four of a kind that beat your hand!"
                            case WinResult.NO_WIN:
                                message = ":("
                    case _:
                        message = f"{winner} | {reason}"
                        
                match winner:
                    case WinResult.TIE:
                        START_CHIPS_PLAYER = player.get_chips() + (get_pot() // 2)
                        START_CHIPS_NPC = npc.get_chips() + (get_pot() // 2)
                        GAME_FONT.render_to(screen, (width() * 0.5 - 280, height() * 0.27), f"round over! split pot! you get {get_pot() // 2} chips!", (255, 255, 255))
                    case WinResult.PLAYER_WIN:
                        START_CHIPS_PLAYER = player.get_chips() + get_pot()
                        START_CHIPS_NPC = npc.get_chips()
                        GAME_FONT.render_to(screen, (width() * 0.5 - 250, height() * 0.27), f"round over! you won {get_pot()} chips!", (255, 255, 255))
                    case WinResult.NPC_WIN:
                        START_CHIPS_PLAYER = player.get_chips()
                        START_CHIPS_NPC = npc.get_chips() + get_pot()
                        GAME_FONT.render_to(screen, (width() * 0.5 - 250, height() * 0.27), f"round over! npc won {get_pot()} chips!", (255, 255, 255))
                    case WinResult.NO_WIN:
                        START_CHIPS_PLAYER = player.get_chips()
                        START_CHIPS_NPC = npc.get_chips() + get_pot()
                        GAME_FONT.render_to(screen, (width() * 0.5 - 250, height() * 0.27), "round over! no one won :(", (255, 255, 255))
                    case _:
                        if ROUND_WINNER == "npc_fold":
                            GAME_FONT.render_to(screen, (width() * 0.5 - 230, height() * 0.27), "round over! npc chose to fold!", (255, 255, 255))
                            START_CHIPS_PLAYER = player.get_chips() + get_pot()
                            START_CHIPS_NPC = npc.get_chips()
                            message = f"you get {get_pot()} chips!"
                            
                        if ROUND_WINNER == "player_fold":
                            GAME_FONT.render_to(screen, (width() * 0.5 - 230, height() * 0.27), "round over! you chose to fold!", (255, 255, 255))
                            START_CHIPS_PLAYER = player.get_chips()
                            START_CHIPS_NPC = npc.get_chips() + get_pot()
                            message = f"NPC gets {get_pot()} chips!"
                            
                if "You and the NPC had equal value hands!" in message:
                    GAME_FONT.render_to(screen, (width() * 0.5 - 300, height() * 0.33), message, (255, 255, 255))
                else:
                    GAME_FONT.render_to(screen, (width() * 0.5 - (len(message) * 8), height() * 0.33), message, (255, 255, 255))
                
                sprites_list = pygame.sprite.Group()
                
                sprites_list.add(button_sprites[ButtonType.NEW.value])
                
                npc.card1.set_hidden(False)
                npc.card2.set_hidden(False)
                sprites_list.add(player.card1.sprite)
                sprites_list.add(player.card2.sprite)
                sprites_list.add(npc.card1.sprite)
                sprites_list.add(npc.card2.sprite)
                
                middle_x = get_horizontal_middle(config['game']['card_width'])
                middle_y = get_vertical_middle(config['game']['card_height'])
                    
                card3x = middle_x
                card3y = middle_y
                    
                card2x = card3x - config['game']['card_width'] - 5
                card2y = middle_y
                    
                card4x = card3x + config['game']['card_width'] + 5
                card4y = middle_y
                    
                card1x = card2x - config['game']['card_width'] - 5
                card1y = middle_y
                    
                card5x = card4x + config['game']['card_width'] + 5
                card5y = middle_y
                    
                current_decknewx = card5x + config['game']['card_width'] + 20
                    
                i = 0
                for c in get_house_cards():
                    
                    if i == 0:
                        c.sprite.set_x(card1x)
                        c.sprite.set_y(card1y)
                        
                    if i == 1:
                        c.sprite.set_x(card2x)
                        c.sprite.set_y(card2y)
                    if i == 2:
                        c.sprite.set_x(card3x)
                        c.sprite.set_y(card3y)
                        
                    if i == 3:
                        c.sprite.set_x(card4x)
                        c.sprite.set_y(card4y)
                        
                    if i == 4:
                        c.sprite.set_x(card5x)
                        c.sprite.set_y(card5y)
                        
                    if i > 4:
                        raise ValueError("how do we have more than 5 house cards...")
                        
                    sprites_list.add(c.sprite)
                    
                    i += 1
                    
                current_deck = get_deck()
                sprites_list.add(current_deck.sprite)
                    
                current_deck.sprite.set_x(current_decknewx)
                
                for sprite in sprites_list:
                    screen.blit(sprite.image, (sprite.x, sprite.y), sprite.source_rect)
                    
                sprites_list.update(event_list)

        else:
            set_round_over(False)
            set_gamestate(GameState.END)
        
    pygame.display.flip()
    
pygame.quit()