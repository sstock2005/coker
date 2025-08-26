import random
import pygame

import modules.poker_types as pt

import modules.sprite_helper as sh
import modules.window_helper as wh
import modules.resource_manager as rm
import modules.constants
import modules.globals

class PokerCardSprite(pygame.sprite.Sprite):
    """Class for poker card sprite.

    Args:
        poker_suit (poker_types.PokerSuit): The card's suit
        poker_number (poker_types.PokerNumber): The card's number
        x (int | None, optional): custom x position. Defaults to None.
        y (int | None, optional): custom y position. Defaults to None.
        hand_position (int, optional): Position in hand. can be -1 | 0 | 1. Defaults to -1.
        is_hidden (bool, optional): Render the card's back instead of the front? Defaults to False.
        is_npc (bool, optional): Render as NPC's card? Defaults to False.
    """
    
    def __init__(self, poker_suit: pt.PokerSuit, poker_number: pt.PokerNumber, x: int | None = None, y: int | None = None, hand_position: int = -1, is_hidden: bool = False, is_npc: bool = False):
        super().__init__()
        
        self.poker_suit = poker_suit
        self.poker_number = poker_number
        self.hand_position = hand_position
        self.is_hidden = is_hidden
        self.is_npc = is_npc
        
        self.image, image_rect = rm.get_poker_card_image(poker_suit=self.poker_suit, poker_number=self.poker_number, is_hidden=self.is_hidden)
        
        if self.hand_position == -1:
            self.x = x if x is not None else wh.get_middle_h(image_rect.width)
            self.y = y if y is not None else wh.get_middle_v(image_rect.height)
        else:
            self.x, self.y = sh.get_hand_pos(hand_position=self.hand_position, is_npc=self.is_npc)
         
        self.rect = pygame.Rect(self.x, self.y, image_rect.width, image_rect.height)
        
        self.set_hidden(self.is_npc)
            
    def set_hidden(self, is_hidden: bool):
        """Function to set card's hidden status.

        Args:
            is_hidden (bool): Hidden value
        """
        
        image, _ = rm.get_poker_card_image(poker_suit=self.poker_suit, poker_number=self.poker_number, is_hidden=is_hidden)
        
        self.image = image
        
    def set_is_npc(self, is_npc: bool):
        self.is_npc = is_npc
        
        self.set_hidden(self.is_npc)
        
class PokerDeckSprite(pygame.sprite.Sprite):
    """Class for poker deck sprite.

    Args:
        x (int | None, optional): custom x position. Defaults to None.
        y (int | None, optional): custom y position. Defaults to None.
        center (bool, optional): default position center? Defaults to True.
    """
    
    def __init__(self, x: int | None = None, y: int | None = None, center: bool = True):
        super().__init__()
        
        self.image, image_rect = rm.get_poker_deck_image()
        
        self.cards: list[PokerCardSprite] = []
        
        for poker_suit in list(pt.PokerSuit):
            for poker_number in list(pt.PokerNumber):
                poker_card = PokerCardSprite(poker_suit, poker_number)
                self.cards.append(poker_card)
                
        if len(self.cards) > 52:
            ValueError(f"Wrong amount of cards in generated deck: {len(self.cards)} should be 52!")
            
        if center:
            self.x = wh.get_middle_h(image_rect.width)
            self.y = wh.get_middle_v(image_rect.height)
        else:
            self.x = x
            self.y = y
            
        self.rect = pygame.Rect(self.x, self.y, image_rect.width, image_rect.height)
        
    def shuffle(self):
        for _ in range(30):
            random.shuffle(self.cards)
    
    def draw(self, is_npc: bool = False) -> PokerCardSprite:
        if len(self.cards) > 0:
            card = self.cards.pop()
            card.set_is_npc(is_npc)
        else:
            card = None
        
        return card
            
class PokerButtonSprite(pygame.sprite.Sprite):
    """Class for poker button sprites.

    Args:
        button (poker_types.PokerButton): Poker Button
        x (int | None, optional): custom position x. Defaults to None.
        y (int | None, optional): custom position y. Defaults to None.
    """
    
    def __init__(self, button: pt.PokerButton, x: int | None = None, y: int | None = None):
        super().__init__()
        
        self.button = button
        self.clicked = False
        self.pressed = self.clicked
        
        self.image, image_rect = rm.get_poker_button_image(button=self.button, pressed=self.pressed)
        
        if x and y:
            self.x = x
            self.y = y
        else:
            mh = wh.get_middle_h(image_rect.width)
            area_one_y = (modules.constants.WINDOW_HEIGHT // 4) * 3
            area_two_y = (modules.constants.WINDOW_HEIGHT // 4) * 3.5
            area_three_y = (modules.constants.WINDOW_HEIGHT // 4) * 2.5
            
            match button:
                case pt.PokerButton.START:
                    self.x = mh
                    self.y = area_one_y
                case pt.PokerButton.CALL:
                    self.x = mh + (mh // 1.5) - modules.constants.BUTTON_WIDTH - 10
                    self.y = (modules.constants.WINDOW_HEIGHT // 4) * 3
                case pt.PokerButton.RAISE:
                    self.x = mh + (mh // 1.5)
                    self.y = area_one_y
                case pt.PokerButton.BET1:
                    self.x = mh + (mh // 2)
                    self.y = area_two_y
                case pt.PokerButton.BET5:
                    self.x = mh + (mh // 2) + modules.constants.BUTTON_WIDTH
                    self.y = area_two_y
                case pt.PokerButton.BET10:
                    self.x = mh + (mh // 2) + (modules.constants.BUTTON_WIDTH * 2)
                    self.y = area_two_y
                case pt.PokerButton.BETALLIN:
                    self.x = mh + (mh // 2) + modules.constants.BUTTON_WIDTH
                    self.y = area_three_y
                case pt.PokerButton.FOLD:
                    self.x = mh + (mh // 1.5) + modules.constants.BUTTON_WIDTH + 10
                    self.y = area_one_y
                case pt.PokerButton.NEW:
                    self.x = mh + (mh // 1.5)
                    self.y = area_one_y
                    
        self.rect = pygame.Rect(self.x, self.y, image_rect.width, image_rect.height)
        
    def update(self, event_list: list[pygame.event.Event]):
        """Function to register when someone clicks a button.

        Args:
            event_list (list[pygame.event.Event]): The list of events provided by pygame.
        """
        
        disabled = modules.globals.PLAYERS_TURN
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = not self.clicked
        
        if not disabled:
            if not self.clicked and self.pressed:
                self.pressed = not self.pressed
                self.image, image_rect = rm.get_poker_button_image(button=self.button, pressed=self.pressed)
                self.rect = pygame.Rect(self.x, self.y, image_rect.width, image_rect.height)  
            elif self.clicked:
                self.pressed = not self.pressed
                self.image, image_rect = rm.get_poker_button_image(button=self.button, pressed=self.pressed)
                self.rect = pygame.Rect(self.x, self.y, image_rect.width, image_rect.height)
                
                match self.button:
                    case pt.PokerButton.START:
                        # start function
                        pass
                    case pt.PokerButton.CALL:
                        # call function
                        pass
                    case pt.PokerButton.RAISE:
                        # raise function
                        pass
                    case pt.PokerButton.BET1:
                        # bet 1 function
                        pass
                    case pt.PokerButton.BET5:
                        # bet 5 function
                        pass
                    case pt.PokerButton.BET10:
                        # bet 10 function
                        pass
                    case pt.PokerButton.BETALLIN:
                        # bet all in function
                        pass
                    case pt.PokerButton.FOLD:
                        # fold function
                        pass
                    case pt.PokerButton.NEW:
                        # new function
                        pass
                    
                self.clicked = not self.clicked