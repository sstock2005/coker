import modules.poker_types as pt
import modules.sprites

GAMESTATE: pt.PokerGameState = pt.PokerGameState.TITLE

def start(player_starting_chips: int = 100, npc_starting_chips: int = 100):
    """Function to start the actual game, called from start button during title screen.

    Args:
        player_starting_chips (int, optional): Starting chips amount for player. Defaults to 100.
        npc_starting_chips (int, optional): Starting chips amount for NPC. Defaults to 100.
    """
    
    global PLAYER, NPC, STARTING_CHIPS_PLAYER, STARTING_CHIPS_NPC
    global PLAYERS_TURN, ROUND_WINRESULT, ROUND_WINREASON
    global GAMESTATE, ROUND_POT, PLAYER_DEALING
    global HOUSE_CARDS, DECK
    
    PLAYER = Player(is_npc=False)
    NPC = Player(is_npc=True)
    STARTING_CHIPS_PLAYER = player_starting_chips
    STARTING_CHIPS_NPC = npc_starting_chips
    PLAYERS_TURN = False
    ROUND_WINRESULT = None
    ROUND_WINREASON = None
    GAMESTATE = pt.PokerGameState.DRAW
    ROUND_POT = 0
    PLAYER_DEALING = True
    HOUSE_CARDS = []
    DECK = modules.sprites.PokerDeckSprite()
    
class Player:
    """Class for Player objects. If you can figure out a way to put this in a different file than globals.py, please PR!
    
    Args:
        is_npc (bool, optional): Is the current player object an NPC? Defaults to False.
        starting_chips (int, optional): Starting chips amount for player object. Default to 100.
    """
    def __init__(self, is_npc: bool = False, starting_chips: int = 100):
        
        self.is_npc = is_npc
        self.chips = starting_chips
        self.turn: bool = False
        """Returns true if it is the current player object's turn.
        """
        
        self.dealt = False
        """Returns true if the current player object has been dealt two cards.
        """
        
        self.bet = 0
        """The current player object's last put bet.
        """
        
        self.bet_total = 0
        """The current player object's total bet amount for this round.
        """
        
    def foldFunc(self):
        """Function to make current player object fold out of the current round.
        """
        
        global ROUND_WINRESULT, GAMESTATE
        
        if self.is_npc:
            ROUND_WINRESULT = pt.PokerResult.PLAYER_WIN
        else:
            ROUND_WINRESULT = pt.PokerResult.NPC_WIN
            
        GAMESTATE = pt.PokerGameState.END
        
    def callFunc(self):
        """Function to make current player object call in the current round.
        """
        
        cost = PLAYER.bet if self.is_npc else NPC.bet
        
        if cost <= self.chips:
            self.betFunc(cost)
    
    def raiseFunc(self):
        """Function to make current player object raise by 10 chips in the current round.
        """
        
        cost = PLAYER.bet if self.is_npc else NPC.bet
        
        cost += 10
        
        if cost <= self.chips:
            self.betFunc(cost)
            
    def betFunc(self, chips: int):
        """Function to make current player object bet n chips where n is argument chips in the current round.

        Args:
            chips (int): desired bet amount in chips
        """
        
        global ROUND_POT
        
        if self.turn:
            if chips == -1: # all in
                chips = self.chips
            self.chips -= chips
            self.bet = chips
            self.bet_total += self.bet
            
            ROUND_POT += self.bet
            
            self.turn = not self.turn
            
    def thinkFunc(self) -> int:
        """Function for NPC to think of it's choice.

        Raises:
            Exception: Player object cannot think unless it is an NPC!

        Returns:
            int: NPC's desired bet
        """
        
        if not self.is_npc:
            raise Exception("Player object cannot think unless it is an NPC!")
        
        return 1