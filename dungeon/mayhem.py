import random
import polars as pl


class game:
    def __init__(
        self,
        n_players: int = 2,
        base_deck=True,
        monster_madness=False,
        battle_for_baldurs_gate=False,
        log_this_game=False,
        use_these_players=None,
    ) -> None:
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
            decks += ["Jaheira", "Minsc and Boo"]

        if n_players > len(decks):
            raise ValueError("There are not enough decks")

        if use_these_players is None:
            player_names = random.sample(decks, n_players)
        else:
            player_names = use_these_players

        self.n_players = len(player_names)
        # Add in the 5+ player rules
        self.zone_of_influence = len(player_names) > 4
        self.vengeful_ghost = len(player_names) > 4
        self.active_players = player_names
        self.players = dict(
            zip(player_names, [player(player_name) for player_name in player_names])
        )
        self.knocked_out_players = []
        self.round = 0
        self.winner = "Unknown"
        self.log_this_game = log_this_game
        if log_this_game:
            self.data = []
            self.log_player_stats()
            self.log = []

    def play_the_game(self):
        while len(self.active_players) > 1:
            self.play_one_round()
        winner = self.active_players[0]
        self.log_this(f"{winner} Wins the game!!")
        self.winner = winner
        return self

    def log_this(self, message: str):
        if self.log_this_game:
            self.log.append(message)
        return self

    def log_player_stats(self):
        if self.log_this_game:
            data = []
            for player_name, player in self.players.items():
                stats = player.get_stats()
                stats["Round"] = self.round
                data.append(stats)
            self.data += data
        return self

    def get_log(self) -> list:
        return self.log

    def get_player_stats(self) -> list:
        return [player.health_points for key, player in self.players.items()]

    def save_stats(self):
        df = pl.from_dicts(self.data)
        df.write_csv("stats.csv", sep=",")
        return self

    def knock_out_player(self, player_name):
        self.active_players.remove(player_name)
        self.knocked_out_players.append(player_name)
        if self.log_this_game:
            self.log_this(player_name + " is knocked out.")
        return self

    def s(self, n):
        if n == 1:
            return ""
        return "s"

    def play_one_round(self):
        self.round += 1
        for player_name in self.active_players:
            # Play the first card in their hand
            player = self.players[player_name].reset()
            while player.n_turns > 0:
                if len(player.hand) > 0:
                    card = player.hand.pop(0)
                    # We assume the card will be discarded at the end of their turn
                    discard_card = True
                    self.log_this(f'{player_name} plays "{card.name}."')
                
                    if not card.mighty_power_card:
                        if card.attack > 0:
                            if self.zone_of_influence:
                                player_index = self.active_players.index(player_name)
                                possible_targets = [
                                    self.active_players[player_index - 1],
                                    self.active_players[player_index - 1],
                                ]
                            else:
                                possible_targets = self.active_players.copy()
                                possible_targets.remove(player_name)
                            if len(possible_targets) > 0:
                                target_name = random.sample(possible_targets, 1)[0]
                                target = self.players[target_name]
                                target.is_attacked(card.attack)
                                self.log_this(
                                    f"  {player_name} deals {target_name} {card.attack} damage. Their health points are now at {target.health_points}."
                                )
                                if target.health_points == 0:
                                    target.knocked_out = True
                                    self.knock_out_player(target_name)

                        if card.healing > 0:
                            player.heal(card.healing)
                            self.log_this(
                                f"  {player_name} gain {card.healing} health points.  Their health is now at {player.health_points}."
                            )

                        if card.draw > 0:
                            s = self.s(card.draw)
                            new_cards = player.deck.draw(card.draw)
                            if isinstance(new_cards, list):
                                player.hand += new_cards
                            else:
                                player.hand += [new_cards]
                            n_cards = len(player.hand)
                            self.log_this(
                                f"  Draws {card.draw} card{s}.  They have {n_cards} cards in their hand."
                            )

                        if card.defense > 0:
                            s = self.s(card.defense)
                            self.log_this(
                                f"  Gives {player_name} {card.defense} shield{s}."
                            )
                            player.defense_cards[card] = card.defense
                            discard_card = False

                        if card.play_again > 0:
                            s = self.s(card.play_again)
                            self.log_this(f"  Plays {card.play_again} more time{s}.")
                            player.add_turns(card.play_again)
                    else:
                        self.log_this(f"  What a mighty turn!")
                    player.n_turns -= 1

                if discard_card:
                    player.deck.discard_pile.append(card)

                if len(player.hand) == 0:
                    # Draw 3 new cards
                    player.hand = player.deck.draw(3)
        self.log_player_stats()
        return self

    def print_log(self):
        for line in self.log:
            print(line)


class player:
    def __init__(self, name: str) -> None:
        self.deck = deck(name).shuffle()
        self.name = name
        self.health_points = 10
        self.n_turns = 1
        self.knocked_out = False
        self.vengeful_ghost = False
        self.vengeful_ghost_targets = []
        self.knocked_out = []
        self.hand = self.deck.draw(3)
        self.defense_cards = {}  # Key is card and value is n shields left

    def heal(self, health_points):
        return self.set_health_points(min(self.health_points + health_points, 10))

    def add_turns(self, n_turns):
        self.n_turns += n_turns
        return self

    def reset(self):
        self.n_turns = 1
        return self

    def get_shields(self):
        shields = 0
        if len(self.defense_cards) > 0:
            for card, defense_points in self.defense_cards.items():
                shields += defense_points
        return shields
    
    def get_stats(self):
        return {
            "Name": self.name,
            "HP": self.health_points,
            "Shields": self.get_shields(),
            "Deck": len(self.deck.cards),
            "Hand": len(self.hand),
            "Discard Pile": len(self.deck.discard_pile),
            "Defense": len(self.defense_cards.keys())
        }
    
    def set_health_points(self, health_points:int):
        self.health_points = health_points
        return self

    def is_attacked(self, n_hits: int = 1):
        if not self.knocked_out:
            if len(self.defense_cards) > 0:
                discard = []
                for card, defense_points in self.defense_cards.items():
                    if n_hits > 0:
                        if n_hits >= defense_points:
                            discard.append(card)
                            n_hits -= defense_points
                        else:
                            self.defense_cards[card] -= n_hits
                            n_hits = 0

                if len(discard) > 0:
                    for card in discard:
                        self.defense_cards.pop(card)
                        self.deck.discard_pile.append(card)

            self.health_points = max(self.health_points - n_hits, 0)
            self.knocked_out = self.health_points == 0
        return self


class deck:
    def __init__(self, player_name: str) -> None:
        self.discard_pile = []
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
        elif player_name == "Blorp":
            self.cards = [
                card("Acid Burp", attack=1, play_again=1),
                card("Acid Burp", attack=1, play_again=1),
                card("Fastest Cube Alive", attack=1, draw=1, healing=1),
                card("Fastest Cube Alive", attack=1, draw=1, healing=1),
                card("Fastest Cube Alive", attack=1, draw=1, healing=1),
                card("Slime Time", play_again=2),
                card("Slime Time", play_again=2),
                card("Sugar Rush", draw=2),
                card("Sugar Rush", draw=2),
                card("Open Wide", draw=2, play_again=1),
                card("D6 of Doom", attack=2),
                card("Former Friends", defense=2),
                card("Combat Cubed", attack=3),
                card("Combat Cubed", attack=3),
                card("Combat Cubed", attack=3),
                card("Arcane Appetizer", attack=2, draw=1),
                card("Arcane Appetizer", attack=2, draw=1),
                card("Cubes Have Feelings Too", healing=1, play_again=1),
                card("Cubes Have Feelings Too", healing=1, play_again=1),
                card("Cleric a la Slime", healing=1, attack=2),
                card("Cleric a la Slime", healing=1, attack=2),
                mighty_power_card("Burped-Up Bones"),
                mighty_power_card("Burped-Up Bones"),
                mighty_power_card("Here I Come"),
                mighty_power_card("Here I Come"),
                mighty_power_card("Hugs!"),
                mighty_power_card("Hugs!"),
            ]
        elif player_name == "Lord Cinderpuff":
            self.cards = [
                card("Bull Market", play_again=2),
                card("Bull Market", play_again=2),
                card("Peaceful Nap", draw=3),
                card("Investment Opportunity", healing=1, draw=1),
                card("Investment Opportunity", healing=1, draw=1),
                card("Mob of Lawyers", defense=3),
                card("Wall of Money", defense=2),
                card("Wall of Money", defense=2),
                card("Eviler Sneer", healing=1, play_again=1),
                card("Eviler Sneer", healing=1, play_again=1),
                card("Ancient Anger", attack=1, play_again=1),
                card("Ancient Anger", attack=1, play_again=1),
                card("Ancient Anger", attack=1, play_again=1),
                card("Tooth and Claw", attack=3),
                card("Tooth and Claw", attack=3),
                card("Wisdom of Ages", draw=2),
                card("Wisdom of Ages", draw=2),
                card("Kobold Maid", defense=1, attack=1),
                card("Kobold Maid", defense=1, attack=1),
                card("Wing Buffet", attack=2),
                card("Wing Buffet", attack=2),
                mighty_power_card("Liquidate Assets"),
                mighty_power_card("Liquidate Assets"),
                mighty_power_card("Murders and Acquisitions"),
                mighty_power_card("Murders and Acquisitions"),
                mighty_power_card("Hostile Takeover"),
                mighty_power_card("Hostile Takeover"),
                mighty_power_card("Hostile Takeover"),
            ]
        elif player_name == "Dr. Tentaculous":
            self.cards = [
                card("Just a Nibble", draw=1, healing=1, play_again=1),
                card("Receptionist", defense=1, attack=1),
                card("Sip Tea", healing=2, draw=1),
                card("Sip Tea", healing=2, draw=1),
                card("Diagnosis Evil", draw=1, attack=2),
                card("Diagnosis Evil", draw=1, attack=2),
                card("Diagnosis Evil", draw=1, attack=2),
                card("Id Insinuation", attack=1, play_again=1),
                card("Id Insinuation", attack=1, play_again=1),
                card("Id Insinuation", attack=1, play_again=1),
                card("Ego Whip", attack=2),
                card("Ego Whip", attack=2),
                card("Superego Whip", attack=3),
                card("Superego Whip", attack=3),
                card("Enthralled Thrall", defense=2),
                card("Enthralled Thrall", defense=2),
                card("PhD in Psycology", play_again=2),
                card("PhD in Psycology", play_again=2),
                card("Relax at Work", draw=3),
                card("Puppet Therapy", defense=1, attack=2),
                card("Puppet Therapy", defense=1, attack=2),
                card("Puppet Therapy", defense=1, attack=2),
                mighty_power_card("Mind Blast"),
                mighty_power_card("Mind Blast"),
                mighty_power_card("Mind Games"),
                mighty_power_card("Mind Games"),
                mighty_power_card("Tell Me About Your Mother"),
                mighty_power_card("Tell Me About Your Mother"),
            ]
        elif player_name == "Mimi LeChaise":
            self.cards = [
                card("Completely Safe Door", play_again=2),
                card("Completely Safe Door", play_again=2),
                card("Harmless Pile of Rocks", attack=2, play_again=1),
                card("A Potted Plant (Honest!)", defense=1, attack=1),
                card("Just Another Coat Rack", healing=2),
                card("Just Another Coat Rack", healing=2),
                card("Actually an Empty Chest", defense=1, draw=1),
                card("Actually an Empty Chest", defense=1, draw=1),
                card("A Well-Fitted Hat", attack=1, play_again=1),
                card("A Well-Fitted Hat", attack=1, play_again=1),
                card("Probably Just Dirty Socks", draw=3),
                card("Probably Just Dirty Socks", draw=3),
                card("A Delicous Pie!", attack=2, draw=1),
                card("A Delicous Pie!", attack=2, draw=1),
                card("Definitely Not a Trap", attack=2),
                card("Definitely Not a Trap", attack=2),
                card("Definitely Not a Trap", attack=2),
                card("Non-Carnivorous Couch", attack=2, healing=1),
                card("Non-Carnivorous Couch", attack=2, healing=1),
                card("Not a Mimic (Really)", defense=2),
                mighty_power_card("A Book (Cannot Bite)"),
                mighty_power_card("A Book (Cannot Bite)"),
                mighty_power_card("A Book (Cannot Bite)"),
                mighty_power_card("Definitely Just a Mirror"),
                mighty_power_card("Definitely Just a Mirror"),
                mighty_power_card("It's Not a Trap"),
                mighty_power_card("It's Not a Trap"),
            ]
        elif player_name == "Hoots McGoots":
            self.cards = [
                card("Look Out Below!", attack=2),
                card("Look Out Below!", attack=2),
                card("Strong as a Bear", attack=2, healing=1),
                card("Strong as a Bear", attack=2, healing=1),
                card("Talk to my Agent", defense=3),
                card("Talk to my Agent", defense=3),
                card("Send in the Clowns", defense=1, play_again=1),
                card("Send in the Clowns", defense=1, play_again=1),
                card("Send in the Clowns", defense=1, play_again=1),
                card("Grand Finale", attack=3),
                card("Grand Finale", attack=3),
                card("Intermission", draw=2),
                card("Wise as an Owl", draw=3),
                card("The Hoots Fan Club", defense=2, healing=1),
                card("The Hoots Fan Club", defense=2, healing=1),
                card("Crushing Hug", attack=2, healing=2),
                card("Crushing Hug", attack=2, healing=2),
                card("Made You Look", draw=2, play_again=1),
                card("Very Very Fast", attack=1, play_again=1),
                card("Very Very Fast", attack=1, play_again=1),
                card("Very Very Fast", attack=1, play_again=1),
                card("Very Very Fast", attack=1, play_again=1),
                mighty_power_card("To The Face"),
                mighty_power_card("To The Face"),
                mighty_power_card("Owlbear Boogie"),
                mighty_power_card("Owlbear Boogie"),
                mighty_power_card("For My Next Trick..."),
                mighty_power_card("For My Next Trick..."),
            ]
        elif player_name == "Delilah Deathray":
            self.cards = [
                card("Fashion Police", defense=3),
                card("Fashion Police", defense=3),
                card("Tyranny of Beauty", attack=1, healing=1, play_again=1),
                card("Rays for Days", play_again=2),
                card("Rays for Days", play_again=2),
                card("Me, Myself, and Eye", healing=1, draw=1),
                card("Laser Show", attack=1, play_again=1),
                card("Laser Show", attack=1, play_again=1),
                card("Laser Show", attack=1, play_again=1),
                card("Mirror, Mirror", defense=2),
                card("Mirror, Mirror", defense=2),
                card("Multitask", attack=2, healing=1),
                card("Multitask", attack=2, healing=1),
                card("Cuter Than You", draw=2),
                card("Make it Work", healing=2, draw=1),
                card("Make it Work", healing=2, draw=1),
                card("Beauty Barrage", attack=3),
                card("Beauty Barrage", attack=3),
                card("Beauty Barrage", attack=3),
                card("Double Trouble", attack=2),
                card("Double Trouble", attack=2),
                mighty_power_card("Death Ray"),
                mighty_power_card("Death Ray"),
                mighty_power_card("Death Ray"),
                mighty_power_card("Charm Ray"),
                mighty_power_card("Charm Ray"),
                mighty_power_card("Praise Me"),
                mighty_power_card("Praise Me"),
            ]
        else:
            raise ValueError(f"Invalid player name: {player_name}")

    def shuffle(self):
        random.shuffle(self.cards)
        return self
    
    def discard(self, card):
        self.discard_pile.append(card)
        return self

    def draw(self, n_cards: int = 1):
        if n_cards == 1:
            the_draw = self.cards.pop(0)
        else:
            the_draw = []
            for i in range(n_cards):
                the_draw.append(self.draw())
        if len(self.cards) == 0:
            self.cards = self.discard_pile
            self.discard_pile = []
            self.shuffle()
        return the_draw


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
        self.mighty_power_card = True
