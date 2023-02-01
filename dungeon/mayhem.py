import random

class game:
    def __init__(self, n_players:int = 2, base_deck = True, monster_madness = False, log_this_game = False) -> None:
        self.n_players = n_players
        if base_deck:
            decks = ["Lia", "Sutha", "Oriax", "Azzan"]
        else:
            decks = []
        
        if monster_madness:
            decks = decks + ["Delilah Deathray", "Hoots McGoots", "Mimi LeChaise", "Dr. Tentaculous", "Lord Cinderpuff", "Blorp"]

        self.active_players = random.sample(decks, n_players)
        self.knocked_out_players = []
        self.current_player = 0
        self.log = []
        self.log_this_game = log_this_game
    
    def log_this(self, message:str):
        self.log.append(message)
        return self

    def get_log(self) -> list:
        return self.log

    def knock_out_player(self, player_name):
        self.active_players.remove(player_name)
        self.knocked_out_players.append(player_name)
        if self.log_this_game:
            self.log_this(player_name + " is knocked out")
        return self




class player:
    def __init__(self, name:str) -> None:
        self.name = name
        self.health_points = 10
        self.knocked_out = False
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.defense_cards = {}

    def is_attacked(self):
        if not self.knocked_out:
            self.health_points = self.health_points - 1
            if self.health_points <= 0:
                self.knocked_out = True
                self.health_points = 0
        return self


class deck:
    def __init__(self, player_name:str) -> None:
        pass

    def shuffle(self):
        pass