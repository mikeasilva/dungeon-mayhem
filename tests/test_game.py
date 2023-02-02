import pytest
from dungeon import mayhem as dm

def test_game_initialization():
    game = dm.game(n_players=2)
    assert len(game.active_players) == 2

def test_random_players():    
    assert dm.game().active_players != dm.game().active_players or dm.game().active_players != dm.game().active_players

def test_monster_madness():
    assert dm.game(monster_madness=True).active_players != dm.game(monster_madness=True).active_players

def test_logging():
    message = "testing"
    game = dm.game()
    game.log_this(message)
    # Test that it returns a list
    assert game.get_log() == [message]
    # Test that multiple items can be logged
    game.log_this(message).log_this("1").log_this("2").log_this("3")
    assert len(game.get_log()) == 5

