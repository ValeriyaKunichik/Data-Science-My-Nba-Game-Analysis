Part I

Create a function analyse_nba_game(play_by_play_moves) which receives an array of play and will return a dictionary summary of the game.

Each play follows this format:

PERIOD|REMAINING_SEC|RELEVANT_TEAM|AWAY_TEAM|HOME_TEAM|AWAY_SCORE|HOME_SCORE|DESCRIPTION They are ordered by time.

The return dictionary (hash) will have this format:

{"home_team": {"name": TEAM_NAME, "players_data": DATA}, "away_team": {"name": TEAM_NAME, "players_data": DATA}} DATA will be an array of hashes with this format: {"player_name": XXX, "FG": XXX, "FGA": XXX, "FG%": XXX, "3P": XXX, "3PA": XXX, "3P%": XXX, "FT": XXX, "FTA": XXX, "FT%": XXX, "ORB": XXX, "DRB": XXX, "TRB": XXX, "AST": XXX, "STL": XXX, "BLK": XXX, "TOV": XXX, "PF": XXX, "PTS": XXX} Percent are on 100. Player is a string everything else are integers.

Part II

Create a print_nba_game_stats(team_dict) function which will a dictionary with name and players_data will print it with the following format (each column is separated by a tabulation (' ')):

HEADER FOR PLAYER IN PLAYERS PLAYER TOTAL Example 00

Players FG FGA FG% 3P 3PA 3P% FT FTA FT% ORB DRB TRB AST STL BLK TOV PF PTS Player00 XX XX .XXX X XX .XXX XX XX .XXX XX XX XX XX X X XX XX XX Totals XX XX .XXX X XX .XXX XX XX .XXX XX XX XX XX X X XX XX XX
