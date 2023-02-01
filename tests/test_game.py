import pytest
from dungeon import mayhem as dm

def test_create_game():
    game = dm.game(n_players=2)
    assert len(game.active_players) == 2

def test_random_players():
    game_1 = dm.game()
    game_2 = dm.game()
    assert game_1 != game_2

def test_monster_madness():
    game_1 = dm.game(monster_madness=True)
    game_2 = dm.game(monster_madness=True)
    assert game_1 != game_2

def test_game_log():
    message = "testing"
    game = dm.game()
    game.log_this(message)
    # Test that it returns a list
    assert game.get_log() == [message]
    # Test that multiple items can be logged
    game.log_this(message).log_this("1").log_this("2").log_this("3")
    assert len(game.get_log()) == 5