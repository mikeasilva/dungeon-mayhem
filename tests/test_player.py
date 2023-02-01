import pytest
from dungeon import mayhem as dm

def test_create_player_starts_with_10_hp():
    player = dm.player("Lia")
    assert player.health_points == 10

def test_create_player_knocked_out_after_10_attacks():
    player = dm.player("Lia")
    player.is_attacked()
    assert player.knocked_out is False
    player.is_attacked()
    assert player.knocked_out is False
    player.is_attacked()
    assert player.knocked_out is False
    player.is_attacked()
    assert player.knocked_out is False
    player.is_attacked()
    assert player.knocked_out is False
    player.is_attacked()
    assert player.knocked_out is False
    player.is_attacked()
    assert player.knocked_out is False
    player.is_attacked()
    assert player.knocked_out is False
    player.is_attacked()
    assert player.knocked_out is False
    player.is_attacked()
    assert player.knocked_out is True