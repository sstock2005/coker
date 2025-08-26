from enum import Enum

class PokerResult(Enum):
    """Enum class for Poker game results.
    """
    
    TIE = 0
    PLAYER_WIN = 1
    NPC_WIN = 2
    NO_WIN = 3
    
class PokerHand(Enum):
    """Enum class for Poker hand types.
    """
    
    NONE = 0
    HIGHCARD = 1
    ONEPAIR = 2
    TWOPAIR = 3
    THREEOFAKIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULLHOUSE = 7
    FOUROFAKIND = 8
    STRAIGHTFLUSH = 9
    
class PokerSuit(Enum):
    """Enum class for Poker card suit types.
    """
    
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    
class PokerNumber(Enum):
    """Enum class for Poker card number types.
    """
    
    ACE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 12
    KING = 13
    
class PokerGameState(Enum):
    """Enum class for Poker game state types.
    """

    TITLE = 0
    DRAW = 1
    HOUSECARDS = 2
    BETTING = 3
    END = 4
    
class PokerButton(Enum):
    """Enum class for Poker button types.
    """
    
    START = 0
    CALL = 1
    RAISE = 2
    BET1 = 3
    BET5 = 4
    BET10 = 5
    BETALLIN = 6
    FOLD = 7
    NEW = 8