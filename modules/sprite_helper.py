from modules.window_helper import get_middle_h

from typing import Tuple

import modules.constants

def get_hand_pos(hand_position: int, is_npc: bool = False) -> Tuple[Tuple[int, int]]:
    """Sprite helper function to calculate the positions for both cards in the player's hand.

    Args:
        hand_position (int): 0, 1 | first card, second card
        is_npc (bool): Should the function return the NPC's positions?

    Returns:
        Tuple: A tuple containing a tuple of int pairs.\nEx. (card_1_x, card_1_y), (card_2_x, card_2_y)
    """
    
    height = (modules.constants.WINDOW_HEIGHT // 4) * 3
    middle = get_middle_h(modules.constants.CARD_WIDTH)
    modifier = modules.constants.CARD_WIDTH * 0.55
    
    if is_npc:
        height -= modules.constants.CARD_HEIGHT * 0.7
        
    match hand_position:
        case 0:
            return middle - modifier, height
        case 1:
            return (middle + modifier, height)
        case _:
            raise ValueError("hand_position was not 0 or 1 in get_hand_pos()")
