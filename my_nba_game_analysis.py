import re
import pandas as pd

def print_team_stats(team, team_dict):
    print(team_dict[team]["name"])
    print("Players FG FGA FG% 3P 3PA 3P% FT FTA FT% ORB DRB TRB AST STL BLK TOV PF PTS")
    stat_list = []

    for i in range(len(team_dict[team]["players_data"])):
        stat_dict = team_dict[team]["players_data"][i]
        stat_list.append(list(stat_dict.values()))        
        stat_str = ""
        for j in stat_dict:
            stat_str += str(stat_dict[j]) + "  "
        print(stat_str)
    
    team_totals = []
    team_totals.append("Team Totals")

    for i in range(len(stat_list)):
        for j in range(1, len(stat_list[i])):
            if (i == 0):
                team_totals.append(0)
            team_totals[j] += stat_list[i][j]

    team_totals[3] = round(team_totals[1]/team_totals[2], 3)
    team_totals[6] = round(team_totals[4]/team_totals[5], 3)
    team_totals[9] = round(team_totals[7]/team_totals[8], 3)
    total_str = ""

    for i in range(len(team_totals)):
        total_str += str(team_totals[i]) + " "

    print (total_str)

def print_nba_game_stats(team_dict):
    print_team_stats("home_team", team_dict)
    print_team_stats("away_team", team_dict)

def analyse_nba_game(play_by_play_moves):
    away_team = play_by_play_moves.iloc[0]["AWAY_TEAM"]
    home_team = play_by_play_moves.iloc[0]["HOME_TEAM"]   
    description = play_by_play_moves["DESCRIPTION"].tolist()    
    df = pd.DataFrame(columns=('TEAM_NAME', 'player_name'))

    for i in range(len(play_by_play_moves)):       
        team_name = play_by_play_moves.loc[i, 'RELEVANT_TEAM']
        player_name = re.search('[A-Z]. [a-zA-Z]+', play_by_play_moves.loc[i, 'DESCRIPTION'])

        if (re.search('Shooting foul|Personal foul', play_by_play_moves.loc[i, 'DESCRIPTION'])):
            if (team_name == away_team):
                df.loc[i] = [home_team, player_name.group()]
            else:
                df.loc[i] = [away_team, player_name.group()]
        elif (player_name != None):
            df.loc[i] = [team_name, player_name.group()]
        
    df = df.drop_duplicates(ignore_index = True)
    df = df.sort_values('TEAM_NAME')   
    array = df["player_name"].tolist()

    for i in range (len(array)):
        char = 0
        array[i] = array[i][3:]

    df.index = array
    players_stat = ["FG", "FGA", "FG%","3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS", "2P", "2PA"]

    for i in players_stat:
        df[i] = 0

    for i in range (len(description)):
        if (re.search('makes 3-pt', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "3P"] += 1
        if (re.search('3-pt', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "3PA"] += 1
        if (re.search('makes free', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "FT"] += 1
        if (re.search('misses|makes free', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "FTA"] += 1
        if (re.search('Offensive rebound by \w\.\s\w+', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "ORB"] += 1
        if (re.search('Defensive rebound by \w\.\s\w+', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "DRB"] += 1 
        if (re.search('assist', description[i])):
            df.at[re.search('by +[A-Z]. [a-zA-Z]+', description[i])[0][6:], "AST"] += 1
        if (re.search('steal', description[i])):
            df.at[re.search('by +[A-Z]. [a-zA-Z]+', description[i])[0][6:], "STL"] += 1
        if (re.search('block', description[i])):
            df.at[re.search('by +[A-Z]. [a-zA-Z]+', description[i])[0][6:], "BLK"] += 1
        if (re.search('Turnover by \w\.\s\w+', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "TOV"] += 1
        if (re.search('foul by', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "PF"] += 1
        if (re.search('makes 2-pt', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "2P"] += 1
        if (re.search('2-pt', description[i])):
            df.at[re.search('[A-Z]. [a-zA-Z]+', description[i])[0][3:], "2PA"] += 1
            
    df = df.reset_index(drop = True)                                       
    df['FG'] = df['3P'] + df['2P']
    df['FGA'] = df['3PA'] + df['2PA']
    df['FG%'] = df['FG'] / df['FGA']
    df['3P%'] = df['3P'] / df['3PA']
    df['FT%'] = df['FT'] / df['FTA']
    df['TRB'] = df['ORB'] + df['DRB']
    df['PTS'] = 2*df['2P'] + 3*df['3P'] + df['FT']
    df = df.round({'FG%': 3, 'FT%': 3, '3P%': 3})
    df = df.fillna(0)   
    df = df.drop(columns=['2P', '2PA'])   
    grouped_by_team = df.groupby(df.TEAM_NAME)
    df_home_team = grouped_by_team.get_group(home_team)   
    df_away_team = grouped_by_team.get_group(away_team)
    df_home_team = df_home_team.drop(columns=['TEAM_NAME'])
    df_away_team = df_away_team.drop(columns=['TEAM_NAME']) 
    DATA_home = df_home_team.to_dict('records')
    DATA_away = df_away_team.to_dict('records')
    home_team_hash = {"name": home_team, "players_data": DATA_home}
    away_team_hash = {"name": away_team, "players_data": DATA_away}
    return_hash = {"home_team": home_team_hash, "away_team": away_team_hash}

    return return_hash

play_by_play_moves = pd.read_csv("play_by_play.txt", '|', names=["PERIOD","REMAINING_SEC","RELEVANT_TEAM","AWAY_TEAM","HOME_TEAM","AWAY_SCORE","HOME_SCORE","DESCRIPTION"])
team_dict = analyse_nba_game(play_by_play_moves)              
print_nba_game_stats(team_dict)
