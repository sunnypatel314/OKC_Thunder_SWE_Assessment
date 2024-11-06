# -*- coding: utf-8 -*-
import logging
from functools import partial
import json
import os

from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from django.forms.models import model_to_dict
from app.dbmodels.models import Player, Team, Game, PlayerStats, Shot


LOGGER = logging.getLogger('django')


class PlayerSummary(APIView):
    logger = LOGGER

    def get(self, request, playerID):
        """Return player data"""
        print(playerID)
        # TODO: Complete API response, replace placeholder below with actual implementation that sources data from database
        # print(os.path.dirname(os.path.abspath(__file__)))
        # with open(os.path.dirname(os.path.abspath(__file__)) + '/sample_response/sample_response.json') as sample_response:
        #     data = json.load(sample_response)
        # return Response(data)
        try:
            player = Player.objects.get(id=playerID)
        except Exception as e:
            return Response({"error": f"Player with ID #{playerID} does not exist"}, status=404)
            
        response_object = {"name": player.name, "games": []}
        
        player_stats = PlayerStats.objects.filter(player=player) # stats for each game for player
        
        for statline in player_stats:
            shots = Shot.objects.filter(playerStats=statline)
            game = Game.objects.get(id=statline.game.id)
            player_statline_dict = {"date": game.date.strftime('%Y-%m-%d')}
            player_statline_dict.update(model_to_dict(statline))
            player_statline_dict.pop("player")
            player_statline_dict.pop("game")
            player_statline_dict.pop("id")
            
            player_statline_dict["shots"] = []
            for shot in shots:
                shot_dict = model_to_dict(shot)
                shot_dict.pop("playerStats")
                shot_dict.pop("id")
                player_statline_dict["shots"].append(shot_dict)
            
            response_object["games"].append(player_statline_dict)
        
        return Response(response_object, status=200)
