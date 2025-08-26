import modules.poker_types as pt
from typing import Tuple
import modules.sprites

######## WINNER LOGIC ########

# TODO:
# - Incorporate suit value into value calculations (happens sometimes but not everywhere)
# - Fix get_three_of_a_kind_value
# - Fix get_straight

#### HELPER FUNCTIONS ####

def _is_card_in_house(card: modules.sprites.PokerCardSprite, house: list[modules.sprites.PokerCardSprite]) -> bool:
    """Helper function to check if a given poker card is in the house cards list.

    Args:
        card (modules.sprites.PokerCardSprite): The given poker card.
        house (list[modules.sprites.PokerCardSprite]): The given house poker card list.

    Returns:
        bool: Returns true if given card is in given house poker card list.
    """
    
    return (card in house)

def _get_card_value(card: modules.sprites.PokerCardSprite) -> int:
    """Helper function to return a PokerCardSprite's value as an int

    Args:
        card (modules.sprites.PokerCardSprite): A PokerCardSprite

    Returns:
        int: A PokerCardSprite's value
    """
    
    return 14 if card.poker_number == pt.PokerNumber.ACE else card.poker_number.value + 1

def _get_card_value_via_suit(card: modules.sprites.PokerCardSprite) -> int:
    """Helper function to return a PokerCardSprite in terms of suit rank.

    Args:
        card (modules.sprites.PokerCardSprite): Given PokerCardSprite

    Returns:
        int: A PokerCardSprite's value in terms of suit rank.
    """
    
    return card.poker_suit.value

def _get_best_hand(hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> list[modules.sprites.PokerCardSprite]:
    """Helper function to return the best hand from given hand and house cards.

    Args:
        hand (list[modules.sprites.PokerCardSprite]): Player's hand
        house (list[modules.sprites.PokerCardSprite]): House cards

    Returns:
        list[modules.sprites.PokerCardSprite]: The player's best hand
    """
    
    pool = hand.copy() + house.copy()
    
    pool.sort(key=_get_card_value)
    
    return pool[:5]

def _get_card_number_count(poker_number: pt.PokerNumber, pool: list[modules.sprites.PokerCardSprite]) -> int:
    """Helper function to return count of poker number in a list of poker cards.

    Args:
        poker_number (pt.PokerNumber): Needle
        pool (list[modules.sprites.PokerCardSprite]): Haystack

    Returns:
        int: Count of needle in haystack
    """
    
    count = 0
    
    for c in pool:
        if c.poker_number == poker_number:
            count += 1
            
    return count

def _get_card_suit_count(poker_suit: pt.PokerSuit, pool: list[modules.sprites.PokerCardSprite]) -> int:
    """Helper function to return count of poker suit in a list of poker cards.

    Args:
        poker_suit (pt.PokerSuit): Needle
        pool (list[modules.sprites.PokerCardSprite]): Haystack

    Returns:
        int: Count of needle in haystack
    """
    
    count = 0
    
    for c in pool:
        if c.poker_suit == poker_suit:
            count += 1
            
    return count

#### VALUE CALCUALATION FUNCTIONS ####

def _get_cards_value_generic(generic_list: list[modules.sprites.PokerCardSprite]) -> int:
    """Value calculation function to determine the value of a list of poker cards.

    Args:
        generic_list (list[modules.sprites.PokerCardSprite]): A list of poker cards.

    Returns:
        int: The value of the given list of poker cards determined by _get_card_value.
    """
    
    value = 0
    
    for card in generic_list:
        value += _get_card_value(card)
        
    return value

def _get_three_of_a_kind_value(three_of_a_kind: list[modules.sprites.PokerCardSprite]) -> int:
    """Value calculation function to determine the value of the three of a kind poker hand type.

    Args:
        three_of_a_kind (list[modules.sprites.PokerCardSprite]): Three of a King poker hand

    Returns:
        int: THe value of the given hand determined by _get_card_value.
    """
    
    three_of_a_kind_value = 0

    # TODO: Warning: I can't figure out why I have to unpack three_of_a_kind once to access the card list?
    for lst in three_of_a_kind:
        for card in lst:
            card_value = _get_card_value(card)
            three_of_a_kind_value += card_value

    return three_of_a_kind_value

def _get_two_pair_value(two_pair: Tuple[Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite], Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite]]) -> int:
    """Value calculation function to determine the value of the two pair poker hand type.

    Args:
        two_pair (Tuple[Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite], Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite]]): Two Pair poker hand

    Returns:
        int: The value of the given hand determined by _get_card_value.
    """
    
    two_pair_value = 0
    for pair in two_pair:
        pair_value = 0
            
        for card in pair:
            card_value = _get_card_value(card)
            pair_value += card_value
            
        two_pair_value += pair_value
        
    return two_pair_value

def _get_pair_value(pair: Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite]) -> int:
    """Value calculation function to determine the value of the pair poker hand type.

    Args:
        pair (Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite]): Pair poker hand

    Returns:
        int: The value of the given hand determined by _get_card_value.
    """
    
    pair_value = 0
    
    for card in pair:
        card_value = _get_card_value(card)
        pair_value += card_value
    
    return pair_value

#### POKER HAND CALCULATION FUNCTIONS ####

def _get_four_of_a_kind(hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> list[modules.sprites.PokerCardSprite] | None:
    """Poker hand calculation function to determine if the given hand has a four of a kind in hand.

    Args:
        hand (list[modules.sprites.PokerCardSprite]): Player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        list[modules.sprites.PokerCardSprite] | None: Returns found hand if it exists, otherwise returns None.
    """
    
    pool = hand.copy() + house.copy()
    
    found: list[list[modules.sprites.PokerCardSprite]] = []
    
    for poker_number in pt.PokerNumber:
        count = _get_card_number_count(poker_number, pool)
        
        if count > 3 and count < 5:
            
            group = []
            
            for card in pool:
                if card.poker_number == poker_number:
                    group.append(card)
                    
            found.append(group)
    
    if found == []:
        return None
    
    return found

def _get_fullhouse(hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> list[modules.sprites.PokerCardSprite] | None:
    """Poker hand calculation function to determine if the given hand has a fullhouse in hand.

    Args:
        hand (list[modules.sprites.PokerCardSprite]): Player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        list[modules.sprites.PokerCardSprite] | None: Returns found hand if it exists, otherwise returns None.
    """
    
    three_of_a_kind = _get_three_of_a_kind(hand, house)
    
    if three_of_a_kind == None:
        return None
    
    if three_of_a_kind[0] == None:
        return None
    
    pairs = _get_pairs(hand, house)
    
    if pairs == None:
        return None
    
    highest_pair = pairs[0]
    
    if highest_pair[0] in three_of_a_kind[0]:
        highest_pair = pairs[1]
        
    if highest_pair == None:
        return None
    
    fullhouse = [highest_pair[0], highest_pair[1], three_of_a_kind[0][0], three_of_a_kind[0][1], three_of_a_kind[0][2]]
    
    return fullhouse

def _get_flush(hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> list[modules.sprites.PokerCardSprite] | None:
    """Poker hand calcualtion function to determine if the given hand has a flush in hand.

    Args:
        hand (list[modules.sprites.PokerCardSprite]): Player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        list[modules.sprites.PokerCardSprite] | None: Returns found hand if it exists, otherwise returns None.
    """
    
    pool = hand.copy() + house.copy()
    
    pool.sort(key=_get_card_value_via_suit)
    
    found: dict[int, list[modules.sprites.PokerCardSprite]] = {} # flush value, flush
    
    for poker_suit in pt.PokerSuit:
        count = _get_card_suit_count(poker_suit, pool)
        
        if count > 4:
            group: list[modules.sprites.PokerCardSprite] = []
            
            for card in pool:
                if card.poker_suit == poker_suit:
                    group.append(card)
                    
            found[_get_cards_value_generic(group)] = group
            
    highscore = -1
    for value in found.keys():
        if value > highscore:
            highscore = value
    
    if highscore != -1:
        return found[highscore]
    else:
        return None

def _get_straight(hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> list[modules.sprites.PokerCardSprite] | None:
    """Poker hand calculation function to determine if the given hand has a straight in hand.

    Args:
        hand (list[modules.sprites.PokerCardSprite]): Player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        list[modules.sprites.PokerCardSprite] | None: Returns found hand if it exists, otherwise return None.
    """
    
    # TODO: Implement high ace calculations, this only works with low aces
    
    pool = hand.copy() + house.copy()

    pool.sort(key=_get_card_value)
    
    straights: dict[int, list[modules.sprites.PokerCardSprite]] = {} # straight value, straight modules.sprites.PokerCardSprite list
    
    # remove duplicate suits
    cards: dict[pt.PokerNumber, modules.sprites.PokerCardSprite] = {}
    
    for card in pool:
        result = cards.get(card.poker_number)
        
        if not result or _get_card_value_via_suit(result) < _get_card_value_via_suit(card):
            cards[card.poker_number] = card
            
    for c in cards.values():
        try:
            if cards.get(pt.PokerNumber(c.poker_number.value + 1)).poker_number.value - c.poker_number.value > 1:
                continue
            elif cards.get(pt.PokerNumber(c.poker_number.value + 2)).poker_number.value - cards.get(pt.PokerNumber(c.poker_number.value + 1)).poker_number.value > 1:
                continue
            elif cards.get(pt.PokerNumber(c.poker_number.value + 3)).poker_number.value - cards.get(pt.PokerNumber(c.poker_number.value + 2)).poker_number.value > 1:
                continue
            elif cards.get(pt.PokerNumber(c.poker_number.value + 4)).poker_number.value - cards.get(pt.PokerNumber(c.poker_number.value + 3)).poker_number.value > 1:
                continue
        except AttributeError:
            continue # next card does not exist
        except ValueError as ve:
            if "is not a valid CardNumber" in str(ve):
                continue # next card does not exist
            
        result = []
        
        for i in range(5):
            result.append(cards.get(pt.PokerNumber(c.poker_number.value + i)))
            
        straights[_get_cards_value_generic(result)] = result
        
    highscore = -1
    for value in straights.keys():
        if value > highscore:
            highscore = value
    
    if highscore != -1:
        return straights[highscore]
    else:
        return None

def _get_three_of_a_kind(hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> list[list[modules.sprites.PokerCardSprite]] | None:
    """Poker hand calculation function to determine if the given hand has three of a kind in hand.

    Args:
        hand (list[modules.sprites.PokerCardSprite]): Player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        list[list[modules.sprites.PokerCardSprite]] | None: Returns found hand if it exists, otherwise return None.
    """
    
    pool = hand.copy() + house.copy()
    
    found = []
    
    for poker_number in pt.PokerNumber:
        count = _get_card_number_count(poker_number, pool)
        
        if count > 2 and count < 4:
            
            group = []
            
            for card in pool:
                if card.poker_number == poker_number:
                    group.append(card)
                    
            found.append(group)
    
    if found == []:
        return None
    else:
        return found

def _get_two_pair(hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> list[Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite]] | None:
    """Poker hand calculation function to determine if the given hand has two pair in hand.

    Args:
        hand (list[modules.sprites.PokerCardSprite]): Player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        list[Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite]] | None: Returns found hand if it exists, otherwise return None.
    """
    
    pool = hand.copy() + house.copy()
    
    # Group cards by their number
    card_groups = {}
    
    for card in pool:
        if card.poker_number not in card_groups:
            card_groups[card.poker_number] = []
        card_groups[card.poker_number].append(card)
    
    # Find all ranks that have at least 2 cards (pairs)
    pair_ranks = []
    for rank, cards in card_groups.items():
        if len(cards) >= 2:
            pair_ranks.append((rank, cards))
    
    # If we don't have at least 2 different ranks with pairs, return None
    if len(pair_ranks) < 2:
        return None
    
    # Sort by card value (highest first)
    pair_ranks.sort(key=lambda x: _get_card_value(x[1][0]))
    
    # Create pairs from the two highest ranks
    result = []
    for i in range(2):
        rank, cards = pair_ranks[i]
        # Take the first two cards of this rank to form a pair
        result.append(Tuple[cards[0], cards[1]])
    
    if result == []:
        return None
    else:
        return result

def _get_pairs(hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> list[Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite]] | None:
    """Poker hand calculation function to return any pairs found in player objects hand and house cards.
    
    Args:
        hand (list[modules.sprites.PokerCardSprite]): Player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        list[Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite]] | None: List of pairs sorted by highest value, if none are found returns None.
    """
    
    pool = hand.copy() + house.copy()
    
    pairs: list[Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite]] = []
    
    # get pairs
    for c1 in pool:
        for c2 in pool:
            c1num = c1.poker_number
            c2num = c2.poker_number
            
            if c1num == c2num and c1.poker_suit != c2.poker_suit:
                pairs.append(Tuple[c1, c2])
    
    if len(pairs) < 1:
        return None
    
    pairs.sort(key=_get_pair_value)
    
    return pairs

def _get_pair(hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite] | None:
    """Poker hand calculation function to determine if the given hand has a pair in hand.

    Args:
        hand (list[modules.sprites.PokerCardSprite]): Player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[modules.sprites.PokerCardSprite, modules.sprites.PokerCardSprite] | None: Returns found hand if it exists, otherwise return None.
    """
    
    pairs = _get_pairs(hand=hand, house=house)
    
    if pairs:
        return pairs[0]
    else:
        return None

#### WINNER CALCULATION FUNCITONS ####

def _get_four_of_a_kind_winner(player_hand: list[modules.sprites.PokerCardSprite], npc_hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[pt.PokerResult, str] | Tuple[None, None]:
    """Winner calculation function to determine the winner given two four of a kind hands.

    Args:
        player_hand (list[modules.sprites.PokerCardSprite]): PLAYER player object's hand
        npc_hand (list[modules.sprites.PokerCardSprite]): NPC player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[pt.PokerResult, str] | Tuple[None, None]: TIE | PLAYER_WIN | NPC_WIN | NONE, REASON | NONE
    """
    
    player_four_of_a_kind = _get_four_of_a_kind(player_hand, house)
    npc_four_of_a_kind = _get_four_of_a_kind(npc_hand, house)
    
    if player_four_of_a_kind == None and npc_four_of_a_kind != None:
        return pt.PokerResult.NPC_WIN, "FOUR OF A KIND"
    elif npc_four_of_a_kind == None and player_four_of_a_kind != None:
        return pt.PokerResult.PLAYER_WIN, "FOUR OF A KIND"
    elif player_four_of_a_kind == None and npc_four_of_a_kind == None:
        return None, None
    else:
        player_four_of_a_kind_value = _get_cards_value_generic(player_four_of_a_kind)
        npc_four_of_a_kind_value = _get_cards_value_generic(npc_four_of_a_kind)
            
        if player_four_of_a_kind_value == npc_four_of_a_kind_value:
            return pt.PokerResult.TIE, "FOUR OF A KIND"
        elif player_four_of_a_kind_value > npc_four_of_a_kind_value:
            return pt.PokerResult.PLAYER_WIN, "FOUR OF A KIND"
        else:
            return pt.PokerResult.NPC_WIN, "FOUR OF A KIND"

def _get_fullhouse_winner(player_hand: list[modules.sprites.PokerCardSprite], npc_hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[pt.PokerResult, str] | Tuple[None, None]:
    """Winner calculation function to determine the winner given two fullhouse hands.

    Args:
        player_hand (list[modules.sprites.PokerCardSprite]): PLAYER player object's hand
        npc_hand (list[modules.sprites.PokerCardSprite]): NPC player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[pt.PokerResult, str] | Tuple[None, None]: TIE | PLAYER_WIN | NPC_WIN | NONE, REASON | NONE
    """
    
    player_fullhouse = _get_fullhouse(player_hand, house)
    npc_fullhouse = _get_fullhouse(npc_hand, house)
        
    if player_fullhouse == None and npc_fullhouse != None:
        return pt.PokerResult.NPC_WIN, "FULLHOUSE"
    elif npc_fullhouse == None and player_fullhouse != None:
        return pt.PokerResult.PLAYER_WIN, "FULLHOUSE"
    elif player_fullhouse == None and npc_fullhouse == None:
        return None, None
    else:
            
        player_fullhouse_value = _get_cards_value_generic(player_fullhouse)
        npc_fullhouse_value = _get_cards_value_generic(npc_fullhouse)
        
        if player_fullhouse_value == npc_fullhouse_value:
            return pt.PokerResult.TIE, "FULLHOUSE"
        elif player_fullhouse_value > npc_fullhouse_value:
            return pt.PokerResult.PLAYER_WIN, "FULLHOUSE"
        else:
            return pt.PokerResult.NPC_WIN, "FULLHOUSE"

def _get_flush_winner(player_hand: list[modules.sprites.PokerCardSprite], npc_hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[pt.PokerResult, str] | Tuple[None, None]:
    """Winner calculation function to determine the winner given two flush hands.

    Args:
        player_hand (list[modules.sprites.PokerCardSprite]): PLAYER player object's hand
        npc_hand (list[modules.sprites.PokerCardSprite]): NPC player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[pt.PokerResult, str] | Tuple[None, None]: TIE | PLAYER_WIN | NPC_WIN | NONE, REASON | NONE
    """

    player_flush = _get_flush(player_hand, house)
    npc_flush = _get_flush(npc_hand, house)
    
    if player_flush == None and npc_flush != None:
        return pt.PokerResult.NPC_WIN, "FLUSH"
    elif npc_flush == None and player_flush != None:
        return pt.PokerResult.PLAYER_WIN, "FLUSH"
    elif player_flush == None and npc_flush == None:
        return None, None
    else:
        player_flush_value = _get_cards_value_generic(player_flush)
        npc_flush_value = _get_cards_value_generic(npc_flush)
        
        if player_flush_value == npc_flush_value:
            return pt.PokerResult.TIE, "FLUSH"
        elif player_flush_value > npc_flush_value:
            return pt.PokerResult.PLAYER_WIN, "FLUSH"
        else:
            return pt.PokerResult.NPC_WIN, "FLUSH"

def _get_straight_winner(player_hand: list[modules.sprites.PokerCardSprite], npc_hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[pt.PokerResult, str] | Tuple[None, None]:
    """Winner calculation function to determine the winner given two straight hands.

    Args:
        player_hand (list[modules.sprites.PokerCardSprite]): PLAYER player object's hand
        npc_hand (list[modules.sprites.PokerCardSprite]): NPC player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[pt.PokerResult, str] | Tuple[None, None]: TIE | PLAYER_WIN | NPC_WIN | NONE, REASON | NONE
    """

    player_straight = _get_straight(player_hand, house)
    npc_straight = _get_straight(npc_hand, house)
    
    if player_straight == None and npc_straight != None:
        return pt.PokerResult.NPC_WIN, "STRAIGHT"
    elif npc_straight == None and player_straight != None:
        return pt.PokerResult.PLAYER_WIN, "STRAIGHT"
    elif player_straight == None and npc_straight == None:
        return None, None
    else:
        player_straight_value = _get_cards_value_generic(player_straight)
        npc_straight_value = _get_cards_value_generic(npc_straight)
        
        if player_straight_value == npc_straight_value:
            return pt.PokerResult.TIE, "STRAIGHT"
        elif player_straight_value > npc_straight_value:
            return pt.PokerResult.PLAYER_WIN, "STRAIGHT"
        else:
            return pt.PokerResult.NPC_WIN, "STRAIGHT"

def _get_three_of_a_kind_winner(player_hand: list[modules.sprites.PokerCardSprite], npc_hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[pt.PokerResult, str] | Tuple[None, None]:
    """Winner calculation function to determine the winner given two three of a kind hands.

    Args:
        player_hand (list[modules.sprites.PokerCardSprite]): PLAYER player object's hand
        npc_hand (list[modules.sprites.PokerCardSprite]): NPC player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[pt.PokerResult, str] | Tuple[None, None]: TIE | PLAYER_WIN | NPC_WIN | NONE, REASON | NONE
    """
    
    player_three_of_a_kind = _get_three_of_a_kind(player_hand, house)
    npc_three_of_a_kind = _get_three_of_a_kind(npc_hand, house)
    
    if player_three_of_a_kind == None and npc_three_of_a_kind != None:
        return pt.PokerResult.NPC_WIN, "THREE OF A KIND"
    elif npc_three_of_a_kind == None and player_three_of_a_kind != None:
        return pt.PokerResult.PLAYER_WIN, "THREE OF A KIND"
    elif player_three_of_a_kind == None and npc_three_of_a_kind == None:
        return None, None
    else:
        player_three_of_a_kind_value = _get_three_of_a_kind_value(player_three_of_a_kind)
        npc_three_of_a_kind_value = _get_three_of_a_kind_value(npc_three_of_a_kind)
            
        if player_three_of_a_kind_value == npc_three_of_a_kind_value:
            return pt.PokerResult.TIE, "THREE OF A KIND"
        elif player_three_of_a_kind_value > npc_three_of_a_kind_value:
            return pt.PokerResult.PLAYER_WIN, "THREE OF A KIND"
        else:
            return pt.PokerResult.NPC_WIN, "THREE OF A KIND"

def _get_two_pair_winner(player_hand: list[modules.sprites.PokerCardSprite], npc_hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[pt.PokerResult, str] | Tuple[None, None]:
    """Winner calculation function to determine the winner given two two pair hands.

    Args:
        player_hand (list[modules.sprites.PokerCardSprite]): PLAYER player object's hand
        npc_hand (list[modules.sprites.PokerCardSprite]): NPC player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[pt.PokerResult, str] | Tuple[None, None]: TIE | PLAYER_WIN | NPC_WIN | NONE, REASON | NONE
    """
    
    player_two_pair = _get_two_pair(player_hand, house)
    npc_two_pair = _get_two_pair(npc_hand, house)
    
    if player_two_pair == None and npc_two_pair != None:
        return pt.PokerResult.NPC_WIN, "TWO PAIR"
    elif npc_two_pair == None and player_two_pair != None:
        return pt.PokerResult.PLAYER_WIN, "TWO PAIR"
    elif player_two_pair == None and npc_two_pair == None:
        return None, None
    else:
        player_two_pair_value = _get_two_pair_value(player_two_pair)
        npc_two_pair_value = _get_two_pair_value(npc_two_pair)
            
        if player_two_pair_value == npc_two_pair_value:
            return pt.PokerResult.TIE, "TWO PAIR"
        elif player_two_pair_value > npc_two_pair_value:
            return pt.PokerResult.PLAYER_WIN, "TWO PAIR"
        else:
            return pt.PokerResult.NPC_WIN, "TWO PAIR"

def _get_pair_winner(player_hand: list[modules.sprites.PokerCardSprite], npc_hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[pt.PokerResult, str] | Tuple[None, None]:
    """Winner calculation function to determine the winner given two pair hands.

    Args:
        player_hand (list[modules.sprites.PokerCardSprite]): PLAYER player object's hand
        npc_hand (list[modules.sprites.PokerCardSprite]): NPC player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[pt.PokerResult, str] | Tuple[None, None]: TIE | PLAYER_WIN | NPC_WIN | NONE, REASON | NONE
    """
    
    player_pair = _get_pair(player_hand, house)
    npc_pair = _get_pair(npc_hand, house)
    
    if player_pair == None and npc_pair != None:
        return pt.PokerResult.NPC_WIN, "PAIR"
    elif npc_pair == None and player_pair != None:
        return pt.PokerResult.PLAYER_WIN, "PAIR"
    elif player_pair == None and npc_pair == None:
        return None, None
    else:
        player_value = _get_card_value(player_pair[0]) + _get_card_value(player_pair[1])
        npc_value = _get_card_value(npc_pair[0]) + _get_card_value(npc_pair[1])
        
        if player_pair in house and npc_pair in house:
            return None
        elif player_value == npc_value:
            return pt.PokerResult.TIE, "PAIR"
        elif player_value > npc_value:
            return pt.PokerResult.PLAYER_WIN, "PAIR"
        else:
            return pt.PokerResult.NPC_WIN, "PAIR"

def _get_highcard_winner(player_hand: list[modules.sprites.PokerCardSprite], npc_hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[pt.PokerResult, str] | Tuple[None, None]:
    """Winner calculation function to determine the winner given two hands by highcard.

    Args:
        player_hand (list[modules.sprites.PokerCardSprite]): PLAYER player object's hand
        npc_hand (list[modules.sprites.PokerCardSprite]): NPC player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[pt.PokerResult, str] | Tuple[None, None]: TIE | PLAYER_WIN | NPC_WIN | NONE, REASON | NONE
    """
    
    players_best = _get_best_hand(player_hand, house)
    npc_best = _get_best_hand(npc_hand, house)

    for i in range(5):
        pcard = players_best[i]
        ncard = npc_best[i]
        
        if _get_card_value(pcard) > _get_card_value(ncard):
            return pt.PokerResult.PLAYER_WIN, "HIGHCARD"
        elif _get_card_value(pcard) < _get_card_value(ncard):
            return pt.PokerResult.NPC_WIN, "HIGHCARD"
        elif _get_card_value(pcard) == _get_card_value(ncard):
            continue
        
    # if the entire hand is equal
    return pt.PokerResult.TIE, "HIGHCARD"

def get_winner(player_hand: list[modules.sprites.PokerCardSprite], npc_hand: list[modules.sprites.PokerCardSprite], house: list[modules.sprites.PokerCardSprite]) -> Tuple[pt.PokerResult, str] | Tuple[None, None]:
    """Winner calculation function to determine the winner given each hand and the house cards.

    Args:
        player_hand (list[modules.sprites.PokerCardSprite]): PLAYER player object's hand
        npc_hand (list[modules.sprites.PokerCardSprite]): NPC player object's hand
        house (list[modules.sprites.PokerCardSprite]): The current house cards

    Returns:
        Tuple[pt.PokerResult, str] | Tuple[None, None]: TIE | PLAYER_WIN | NPC_WIN | NONE, REASON | NONE
    """
    
    # winner, reason = get_royale_flush_winner(player_hand, npc_hand, house)
    
    # if winner != None:
    #     return winner, reason
    
    # winner, reason = get_straight_flush_winner(player_hand, npc_hand, house)
    
    # if winner != None:
    #     return winner, reason
    
    winner, reason = _get_four_of_a_kind_winner(player_hand, npc_hand, house)
    
    if winner != None:
       print(winner, reason)
       return winner, reason
    
    winner, reason = _get_fullhouse_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = _get_flush_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = _get_straight_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = _get_three_of_a_kind_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = _get_two_pair_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = _get_pair_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    winner, reason = _get_highcard_winner(player_hand, npc_hand, house)
    
    if winner != None:
        print(winner, reason)
        return winner, reason
    
    return None, None

##############################