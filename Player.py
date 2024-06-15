import json

class Player:
    """Player object. Stores name info and if that player is currently in game."""

    in_game = False

    def __init__(self, summoner_name, puuid, tagline, discord_id, discord_username):
        self.summoner_name = summoner_name
        self.puuid = puuid
        self.tagline = tagline
        self.discord_id = discord_id
        self.discord_username = discord_username

    def __eq__(self, other):
        return self.puuid == other.puuid


async def update_players_list(players):
    """
    Updates a players list if that player is not already in the list.
    """
    with open("squad.json", "r+", encoding="utf-8") as file:
        squad = json.load(file)  # dict squad

    for user in squad:
        player = Player(
            squad[user]["summoner_name"],
            squad[user]["puuid"],
            squad[user]["tagline"],
            squad[user]["discord_id"],
            squad[user]["discord_username"]
        )

        if player not in players:
            players.append(player)
    
    return players