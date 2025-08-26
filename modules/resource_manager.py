from typing import Tuple
import pygame
import os

import modules.poker_types as pt
import modules.constants

def get_poker_card_image(poker_suit: pt.PokerSuit, poker_number: pt.PokerNumber, is_hidden: bool = False) -> Tuple[pygame.Surface, pygame.Rect]:
    """Resource management funciton that returns a card's image and `pygame.Rect`.

    Args:
        poker_suit (poker_types.PokerSuit): The card's suit
        poker_number (poker_types.PokerNumber): The card's number
        is_hidden (bool, optional): If true, returns a card back image. Defaults to False.

    Returns:
        Tuple: The corresponding image and rectangle if it exists.\nEx. (image: pygame.Surface, image_rect: pygame.Rect)
    """
    
    if is_hidden:
        filepath = os.path.join(modules.constants.CARDS_FOLDER, 'Card_Back-88x124.png')
        image = pygame.image.load(filepath)
        image_rect = pygame.Rect(0, 0, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        
        return image, image_rect
    
    match poker_suit:
        case pt.PokerSuit.CLUBS:
            filepath = os.path.join(modules.constants.CARDS_FOLDER, 'Clubs-88x124.png')
        case pt.PokerSuit.DIAMONDS:
            filepath = os.path.join(modules.constants.CARDS_FOLDER, 'Diamonds-88x124.png')
        case pt.PokerSuit.HEARTS:
            filepath = os.path.join(modules.constants.CARDS_FOLDER, 'Hearts-88x124.png')
        case pt.PokerSuit.SPADES:
            filepath = os.path.join(modules.constants.CARDS_FOLDER, 'Spades-88x124.png')
            
    match poker_number:
        case pt.PokerNumber.ACE:
            image_rect = pygame.Rect(0, 0, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.TWO:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH, 0, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.THREE:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH * 2, 0, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.FOUR:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH * 3, 0, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.FIVE:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH * 4, 0, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.SIX:
            image_rect = pygame.Rect(0, modules.constants.CARD_HEIGHT, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.SEVEN:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.EIGHT:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH * 2, modules.constants.CARD_HEIGHT, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.NINE:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH * 3, modules.constants.CARD_HEIGHT, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.TEN:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH * 4, modules.constants.CARD_HEIGHT, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.JACK:
            image_rect = pygame.Rect(0, modules.constants.CARD_HEIGHT * 2, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.QUEEN:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT * 2, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        case pt.PokerNumber.KING:
            image_rect = pygame.Rect(modules.constants.CARD_WIDTH * 2, modules.constants.CARD_HEIGHT * 2, modules.constants.CARD_WIDTH, modules.constants.CARD_HEIGHT)
        
    image = pygame.image.load(filepath)
    
    return image, image_rect

def get_poker_deck_image() -> Tuple[pygame.Surface, pygame.Rect]:
    """Resource management funciton that returns the deck's image and `pygame.Rect`.
    
    Returns:
        Tuple: The corresponding image and rectangle if it exists.\nEx. (image: pygame.Surface, image_rect: pygame.Rect)
    """
    
    filepath = os.path.join(modules.constants.CARDS_FOLDER, 'Card_DeckA-88x140.png')
    image = pygame.image.load(filepath)
    image_rect = pygame.Rect(88, 0, 88, 150)
    
    return image, image_rect

def get_poker_button_image(button: pt.PokerButton, pressed: bool = False) -> Tuple[pygame.Surface, pygame.Rect]:
    """Resource management funciton that returns the corresponding button image and `pygame.Rect`.
    
    Args:
        button (poker_types.PokerButton): The corresponding button defined by poker_types.PokerButton
        pressed (bool, optional): render button as pressed? Defaults to False.

    Returns:
        Tuple: The corresponding image and rectangle if it exists.\nEx. (image: pygame.Surface, image_rect: pygame.Rect)
    """
    
    match button:
        case pt.PokerButton.START:
            filename = 'start_button.png'
        case pt.PokerButton.CALL:
            filename = 'call_button.png'
        case pt.PokerButton.RAISE:
            filename = 'raise_button.png'
        case pt.PokerButton.BET1:
            filename = 'bet_1_button.png'
        case pt.PokerButton.BET5:
            filename = 'bet_5_button.png'
        case pt.PokerButton.BET10:
            filename = 'bet_10_button.png'
        case pt.PokerButton.BETALLIN:
            filename = 'bet_all_in_button.png'
        case pt.PokerButton.FOLD:
            filename = 'fold_button.png'
        case pt.PokerButton.NEW:
            filename = 'new_button.png'
            
    filepath = os.path.join(modules.constants.BUTTON_FOLDER, filename)
    
    image = pygame.image.load(filepath)
    
    if pressed:
        image_rect = pygame.Rect(modules.constants.BUTTON_WIDTH, 0, modules.constants.BUTTON_WIDTH, modules.constants.BUTTON_HEIGHT)
    else:
        image_rect = pygame.Rect(0, 0, modules.constants.BUTTON_WIDTH, modules.constants.BUTTON_HEIGHT)
        
    return image, image_rect