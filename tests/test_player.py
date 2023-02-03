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


def test_shields_work():
    player = dm.player("Lia")
    player.defense_cards = {"Shield": 2}
    assert player.get_shields() == 2
    player.is_attacked()
    assert player.get_shields() == 1
    assert player.health_points == 10
    player.is_attacked()
    assert len(player.defense_cards) == 0
    assert len(player.discard_pile) == 1
    player.is_attacked()
    assert player.health_points == 9
