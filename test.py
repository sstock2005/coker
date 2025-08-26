from poker import CardDeck, CardNumber, PlayingCard, WinResult, Pair, Suit

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

#### POKER HAND CALCULATION FUNCTIONS ####
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
    
    return found

def get_three_of_a_kind(hand: list[PlayingCard], house: list[PlayingCard]) -> list[PlayingCard]:
    pool = hand.copy() + house.copy()
    
    found: list[list[PlayingCard]] = []
    
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

def get_flush_winner(player_hand: list[PlayingCard], npc_hand: list[PlayingCard], house: list[PlayingCard]):
    player_flush = get_flush(player_hand, house)
    npc_flush = get_flush(player_hand, house)
    
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
    npc_straight = get_straight(player_hand, house)
    
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
    
    # winner, reason = get_four_of_a_kind_winner(player_hand, npc_hand, house)
    
    # if winner != None:
    #     return winner, reason
    
    # winner, reason = get_full_house_winner(player_hand, npc_hand, house)
    
    # if winner != None:
    #     return winner, reason
    
    winner, reason = get_flush_winner(player_hand, npc_hand, house)
    
    if winner != None:
        return winner, reason
    
    winner, reason = get_straight_winner(player_hand, npc_hand, house)
    
    if winner != None:
        return winner, reason
    
    winner, reason = get_three_of_a_kind_winner(player_hand, npc_hand, house)
    
    if winner != None:
        return winner, reason
    
    winner, reason = get_two_pair_winner(player_hand, npc_hand, house)
    
    if winner != None:
        return winner, reason
    
    winner, reason = get_pair_winner(player_hand, npc_hand, house)
    
    if winner != None:
        return winner, reason
    
    winner, reason = get_highcard_winner(player_hand, npc_hand, house)
    
    if winner != None:
        return winner, reason
    
    return None, None
     
#### TEST FUNCITONS ####
   
def simulate_game():
    
    deck = CardDeck()
    
    deck.shuffle()
    
    house_cards = []
    player_cards = []
    npc_cards = []
        
    for c in house_cards:
        deck.cards.remove(c)
    
    for c in player_cards:
        deck.cards.remove(c)
        
    player_cards.append(deck.draw())
    npc_cards.append(deck.draw())
    player_cards.append(deck.draw())
    npc_cards.append(deck.draw())
    
    while len(house_cards) < 5:
        house_cards.append(deck.draw())
    
    winner, reason = get_winner(player_cards, npc_cards, house_cards)
    
    print("player = ", end="")
    
    for c in player_cards:
        print(c.tostring() + ", ", end="")
    
    print()
    
    print("npc = ", end="")
    
    for c in npc_cards:
        print(c.tostring() + ", ", end="")
    
    print()
    
    print("house = ", end="")
    
    for c in house_cards:
        print(c.tostring() + ", ", end="")
    
    print()
    
    print("winner =", winner)
    print("reason =", reason)
    
    return winner, reason

if __name__ == '__main__':    
    for _ in range(200):
        simulate_game()