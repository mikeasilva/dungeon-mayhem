import random


class game:
    def __init__(
        self,
        n_players: int = 2,
        base_deck=True,
        monster_madness=False,
        battle_for_baldurs_gate=False,
        log_this_game=False,
    ) -> None:
        self.n_players = n_players
        # Add in the 5+ player rules
        self.zone_of_influence = n_players > 4
        self.vengeful_ghost = n_players > 4
        # Get the list of decks
        if base_deck:
            decks = ["Lia", "Sutha", "Oriax", "Azzan"]
        else:
            decks = []

        if monster_madness:
            decks += [
                "Delilah Deathray",
                "Hoots McGoots",
                "Mimi LeChaise",
                "Dr. Tentaculous",
                "Lord Cinderpuff",
                "Blorp",
            ]

        if battle_for_baldurs_gate:
            deck += ["Jaheira", "Minsc and Boo"]

        self.active_players = random.sample(decks, n_players)
        self.knocked_out_players = []
        self.current_player = 0
        self.data = []
        self.log = []
        self.log_this_game = log_this_game

    def log_this(self, message: str):
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

    def play_one_round(self):
        pass


class player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.health_points = 10
        self.knocked_out = False
        self.deck = deck(name).shuffle()
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
    def __init__(self, player_name: str) -> None:
        if player_name == "Azzan":
            self.cards = [
                card("Burning Hands", attack=2),
                card("Burning Hands", attack=2),
                card("Burning Hands", attack=2),
                card("Lightning Bolt", attack=3),
                card("Lightning Bolt", attack=3),
                card("Lightning Bolt", attack=3),
                card("Lightning Bolt", attack=3),
                card("Evil Sneer", healing=1, play_again=1),
                card("Evil Sneer", healing=1, play_again=1),
                card("Stoneskin", defense=2),
                card("Mirror Image", defense=3),
                card("Shield", defense=1, draw=1),
                card("Shield", defense=1, draw=1),
                card("Speed of Thought", play_again=2),
                card("Speed of Thought", play_again=2),
                card("Speed of Thought", play_again=2),
                card("Magic Missile", attack=1, play_again=1),
                card("Magic Missile", attack=1, play_again=1),
                card("Magic Missile", attack=1, play_again=1),
                card("Knowledge is Power", draw=3),
                card("Knowledge is Power", draw=3),
                card("Knowledge is Power", draw=3),
                mighty_power_card("Charm"),
                mighty_power_card("Charm"),
                mighty_power_card("Vampiric Touch"),
                mighty_power_card("Vampiric Touch"),
                mighty_power_card("Fireball"),
                mighty_power_card("Fireball"),
            ]
        elif player_name == "Lia":
            self.cards = [
                card("Fluffy", defense=2),
                card("Divine Shield", defense=3),
                card("Divine Shield", defense=3),
                card("Divine Smite", attack=3, healing=1),
                card("Divine Smite", attack=3, healing=1),
                card("Divine Smite", attack=3, healing=1),
                card("Fighting Words", attack=2, healing=1),
                card("Fighting Words", attack=2, healing=1),
                card("Fighting Words", attack=2, healing=1),
                card("For Justice", attack=1, play_again=1),
                card("For Justice", attack=1, play_again=1),
                card("For Justice", attack=1, play_again=1),
                card("For Even More Justice", attack=2),
                card("For Even More Justice", attack=2),
                card("For Even More Justice", attack=2),
                card("For Even More Justice", attack=2),
                card("For The Most Justice", attack=3),
                card("For The Most Justice", attack=3),
                card("Finger-Wag of Judgment", play_again=2),
                card("Finger-Wag of Judgment", play_again=2),
                card("High Charisma", draw=2),
                card("High Charisma", draw=2),
                card("Spinning Parry", defense=1, draw=1),
                card("Spinning Parry", defense=1, draw=1),
                card("Cure Wounds", draw=2, healing=1),
                mighty_power_card("Divine Inspiration"),
                mighty_power_card("Divine Inspiration"),
                mighty_power_card("Banishing Smite"),
            ]
        elif player_name == "Oriax":
            self.cards = [
                card("Cunning Action", play_again=2),
                card("Cunning Action", play_again=2),
                card("Stolen Potion", play_again=1, healing=1),
                card("Stolen Potion", play_again=1, healing=1),
                card("Winged Serpent", defense=1, draw=1),
                card("Winged Serpent", defense=1, draw=1),
                card("Even More Daggers", healing=1, draw=2),
                card("The Goon Squad", defense=2),
                card("The Goon Squad", defense=2),
                card("My Little Friend", defense=3),
                card("One Thrown Dagger", attack=1, play_again=1),
                card("One Thrown Dagger", attack=1, play_again=1),
                card("One Thrown Dagger", attack=1, play_again=1),
                card("One Thrown Dagger", attack=1, play_again=1),
                card("One Thrown Dagger", attack=1, play_again=1),
                card("Two Thrown Daggers", attack=2),
                card("Two Thrown Daggers", attack=2),
                card("Two Thrown Daggers", attack=2),
                card("Two Thrown Daggers", attack=2),
                card("All The Thrown Daggers", attack=3),
                card("All The Thrown Daggers", attack=3),
                card("All The Thrown Daggers", attack=3),
                mighty_power_card("Clever Disguise"),
                mighty_power_card("Clever Disguise"),
                mighty_power_card("Pick Pocket"),
                mighty_power_card("Pick Pocket"),
                mighty_power_card("Sneak Attack!"),
            ]
        elif player_name == "Sutha":
            self.cards = [
                card("Head Butt", attack=1, play_again=1),
                card("Head Butt", attack=1, play_again=1),
                card("Brutal Punch", attack=2),
                card("Brutal Punch", attack=2),
                card("Big Axe is Best Axe", attack=3),
                card("Big Axe is Best Axe", attack=3),
                card("Big Axe is Best Axe", attack=3),
                card("Big Axe is Best Axe", attack=3),
                card("Big Axe is Best Axe", attack=3),
                card("Rage", attack=4),
                card("Rage", attack=4),
                card("Flex", healing=1, draw=1),
                card("Flex", healing=1, draw=1),
                card("Spiked Shield", defense=2),
                card("Riff", defense=3),
                card("Raff", defense=3),
                card("Open the Amory", draw=2),
                card("Open the Amory", draw=2),
                card("Two Axes are Better Than One", play_again=2),
                card("Two Axes are Better Than One", play_again=2),
                card("Bag of Rats", defense=1, draw=1),
                card("Snack Time", draw=2, healing=1),
                mighty_power_card("Battle Roar"),
                mighty_power_card("Battle Roar"),
                mighty_power_card("Mighty Toss"),
                mighty_power_card("Mighty Toss"),
                mighty_power_card("Whirling Axes"),
                mighty_power_card("Whirling Axes"),
            ]
        else:
            raise ValueError(f"Invalid player name: {player_name}")

    def shuffle(self):
        random.shuffle(self.cards)
        return self


class card:
    def __init__(
        self,
        name: str,
        attack: int = 0,
        defense: int = 0,
        draw: int = 0,
        healing: int = 0,
        play_again: int = 0,
    ) -> None:
        self.name = name
        self.attack = attack
        self.defense = defense
        self.draw = draw
        self.healing = healing
        self.play_again = play_again
        self.mighty_power_card = False


class mighty_power_card:
    def __init__(self, name: str) -> None:
        self.name = name
        self.mighty_power_card = False
