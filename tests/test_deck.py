import pytest
from dungeon import mayhem as dm

def get_card_names(deck):
    return [card.name for card in deck.cards]

def test_deck_initialization():
    for player_name in ["Azzan", "Lia", "Oriax", "Sutha"]:
        deck = dm.deck(player_name)
        assert isinstance(deck.cards, list)

def test_shuffle():
    # Test that they are initialized in the identical order
    deck1 = dm.deck("Azzan")
    deck1_order = get_card_names(deck1)
    deck2 = dm.deck("Azzan")
    deck2_order = get_card_names(deck2)
    assert deck1_order == deck2_order
    # Test the shuffle
    deck1 = deck1.shuffle()
    deck2 = deck2.shuffle()
    # Testing against two deck b/c chance of getting two decks that look the same after randomizing is small
    assert get_card_names(deck1) != deck1_order or get_card_names(deck2) != deck2_order

def test_draw():
    deck = dm.deck("Azzan")
    card_names = get_card_names(deck)
    top_card_name = card_names[0]
    top_card = deck.draw(1)
    # The deck should have one less card
    assert len(get_card_names(deck)) == len(card_names) - 1
    # The name of the top card should be the first card of the whole deck
    assert top_card.name == top_card_name


def test_for_errors():
    with pytest.raises(ValueError):
        deck = dm.deck("Garbage In")