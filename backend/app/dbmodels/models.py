# -*- coding: utf-8 -*-
"""Contains models related to stats"""
from django.db import models

# Identifies each team
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'Team'

    def __str__(self):
        return self.name
    
# Identifies each game
class Game(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    homeTeam = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    awayTeam = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Game'

    def __str__(self):
        return f"Game {self.id} on {self.date}"
    
# Identifies each player 
class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
        
    class Meta:
        db_table = 'Player'

    def __str__(self):
        return self.name

# Identifies each players performance in each game
class PlayerStats(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, related_name='stats', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='player_stats', on_delete=models.CASCADE)
    isStarter = models.BooleanField(default=False)
    minutes = models.IntegerField()
    points = models.IntegerField()
    assists = models.IntegerField()
    offensiveRebounds = models.IntegerField()
    defensiveRebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    defensiveFouls = models.IntegerField()
    offensiveFouls = models.IntegerField()
    freeThrowsMade = models.IntegerField()
    freeThrowsAttempted = models.IntegerField()
    twoPointersMade = models.IntegerField()
    twoPointersAttempted = models.IntegerField()
    threePointersMade = models.IntegerField()
    threePointersAttempted = models.IntegerField()
    
    class Meta:
        db_table = 'PlayerStats'
        unique_together = ('player', 'game')

    def __str__(self):
        return f"Stats for {self.player.name} in game {self.game.id}"

# Identifies all shots taken in each game by each player
class Shot(models.Model):
    id = models.AutoField(primary_key=True)
    playerStats = models.ForeignKey(PlayerStats, related_name='shots', on_delete=models.CASCADE)
    isMake = models.BooleanField()
    locationX = models.FloatField()
    locationY = models.FloatField()
    
    class Meta:
        db_table = 'Shot'

    def __str__(self):
        return f"Shot by {self.player_stats.player.name}, Made: {self.is_make}"
