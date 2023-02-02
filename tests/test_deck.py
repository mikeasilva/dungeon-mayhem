import pytest
from dungeon import mayhem as dm

def test_deck_initialization():
    for player_name in ["Azzan", "Lia", "Oriax", "Sutha"]:
        deck = dm.deck(player_name)
        assert isinstance(deck.cards, list)

def test_shuffle():
    def get_card_names(deck):
        return [card.name for card in deck.cards]
    # Test that they are initialized in the identical order
    deck1 = dm.deck("Azzan")
    deck1_order = get_card_names(deck1)
    deck2 = dm.deck("Azzan")
    assert deck1_order == get_card_names(deck2)
    # Test the shuffle
    deck1 = deck1.shuffle()
    assert get_card_names(deck1) != deck1_order

def test_for_errors():
    with pytest.raises(ValueError):
        deck = dm.deck("Garbage In")