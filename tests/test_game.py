import pytest
from dungeon import mayhem as dm


def test_game_initialization():
    game = dm.game(n_players=2)
    assert len(game.active_players) == 2


def test_random_players():
    assert (
        dm.game().active_players != dm.game().active_players
        or dm.game().active_players != dm.game().active_players
    )


def test_monster_madness():
    assert (
        dm.game(monster_madness=True).active_players
        != dm.game(monster_madness=True).active_players
    )


def test_logging():
    message = "testing"
    game = dm.game(log_this_game=True)
    game.log_this(message)
    # Test that it returns a list
    assert game.get_log() == [message]
    # Test that multiple items can be logged
    game.log_this(message).log_this("1").log_this("2").log_this("3")
    assert len(game.get_log()) == 5


def test_use_these_players():
    valid_players = ["Lia", "Sutha", "Oriax", "Azzan"]
    game = dm.game(use_these_players=valid_players)
    assert game.active_players == valid_players


def test_should_raise_errors():
    with pytest.raises(ValueError):
        game = dm.game(use_these_players=["Larry", "Curley", "Moe"])


def test_one_round():
    game = dm.game(use_these_players=["Lia", "Sutha"])
    lia = game.players["Lia"]
    assert len(lia.discard_pile) == 0
    game.play_one_round()
    assert len(lia.discard_pile) > 0 or lia.get_shields() > 0
