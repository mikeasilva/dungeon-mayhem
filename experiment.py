import dungeon.mayhem as dm

game = dm.game(2, log_this_game=True, monster_madness=True, use_these_players=["Sutha", "Lia"])

#print(game.active_
# players)
game.play_the_game()
game.print_log()
game.save_stats()
#deck = dm.deck(game.active_players[0])
#print(deck.top_card())