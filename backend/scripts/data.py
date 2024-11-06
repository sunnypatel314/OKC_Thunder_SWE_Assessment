import os
import json

from app.models import Player, Team, Game, Shot, PlayerStats  

"""
This run() function will automatically execute because Django is looking for file with run() when you use "runscript".
The function transfers all data from the 3 JSON files in the raw_data folder to the PostgreSQL database.
This avoids duplicates so if you have a game, player, or team in the JSON data that already exists, this script will skip over that. 
"""
def run():
    print("This script will transfer all data from JSON files into the PostgreSQL database.")
    print("Starting script...")
    
    # Get the directory of the current script (data.py)
    current_dir = os.path.dirname(__file__)

    # Construct the absolute path to the raw_data folder for all 3 JSON files
    players_path = os.path.join(current_dir, "../raw_data/players.json")
    teams_path = os.path.join(current_dir, "../raw_data/teams.json")
    games_path = os.path.join(current_dir, "../raw_data/games.json")
    
    # Load players data
    with open(players_path) as f:
        players_data = json.load(f)

    # Load teams data
    with open(teams_path) as f:
        teams_data = json.load(f)

    # Load games data
    with open(games_path) as f:
        games_data = json.load(f)

    # Create teams
    for team_data in teams_data:
        if Team.objects.filter(id=team_data['id']).exists():
            continue
        team = Team(id=team_data['id'], name=team_data['name'])
        team.save()

    # Create players
    for player_data in players_data:
        if Player.objects.filter(id=player_data['id']).exists():
            continue
        player = Player(id=player_data['id'], name=player_data['name'])
        player.save()

    # Create games
    for game_data in games_data:
        home_team = Team.objects.get(id=game_data['homeTeam']['id'])
        away_team = Team.objects.get(id=game_data['awayTeam']['id'])

        if Game.objects.filter(id=game_data['id']).exists():
            continue
        game = Game(id=game_data['id'], date=game_data['date'], homeTeam=home_team, awayTeam=away_team)
        game.save()

        # Create player statistics for away team
        for team in ["homeTeam", "awayTeam"]:
            for player_data in game_data[team]['players']:
                player = Player.objects.get(id=player_data['id'])  # Retrieve player
                    
                # Skips the iteration if a PlayerStat with the current gameID and playerID already exists    
                if PlayerStats.objects.filter(player=player, game=game).exists():
                    continue
                
                player_stats = PlayerStats(
                    player=player,
                    game=game,
                    isStarter=player_data['isStarter'],
                    minutes=player_data['minutes'],
                    points=player_data['points'],
                    assists=player_data['assists'],
                    offensiveRebounds=player_data['offensiveRebounds'],
                    defensiveRebounds=player_data['defensiveRebounds'],
                    steals=player_data['steals'],
                    blocks=player_data['blocks'],
                    turnovers=player_data['turnovers'],
                    defensiveFouls=player_data['defensiveFouls'],
                    offensiveFouls=player_data['offensiveFouls'],
                    freeThrowsMade=player_data['freeThrowsMade'],
                    freeThrowsAttempted=player_data['freeThrowsAttempted'],
                    twoPointersMade=player_data['twoPointersMade'],
                    twoPointersAttempted=player_data['twoPointersAttempted'],
                    threePointersMade=player_data['threePointersMade'],
                    threePointersAttempted=player_data['threePointersAttempted'],
                )
                player_stats.save()
                for shot in player_data["shots"]:
                    single_shot = Shot(
                        playerStats=player_stats, 
                        isMake=shot["isMake"],
                        locationX=shot["locationX"],
                        locationY=shot["locationY"]
                    )
                    single_shot.save()   
            
    print("Script finished!")    
