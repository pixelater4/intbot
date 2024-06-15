from random import choice
from riot_api_requests import *

generic_good_messages = (
    "balled out",
    "is him",
)

generic_bad_messages = (
    "sprinted it",
    "ran it down",
    "inted",
    "is trolling",
)


def match_performance(player, match):
    """
    Returns string based on player's performance in a given match
    Throws UnboundLocalError if no notable performance
    """
    for participant in match["info"]["participants"]:
        if player.puuid == participant["puuid"]:  # filters just the player we want
            try:
                kills = participant["kills"]
                deaths = participant["deaths"]
                assists = participant["assists"]
                kda = participant["challenges"]["kda"]
                kp = participant["challenges"]["killParticipation"]
                champion_name = participant["championName"]
                win = participant["win"]  # bool win
                game_length = participant["challenges"]["gameLength"]
                cs = (
                    participant["neutralMinionsKilled"]
                    + participant["totalMinionsKilled"]
                )
            except KeyError as e:
                print(e)

            cspm = round((cs / (game_length / 60)), 2)

            # arbitrarily lowers the value of assists as the game length goes on
            # according the function https://www.desmos.com/calculator/pzdgm6dkil
            adjusted_assists = (
                assists
                if game_length < 15 * 60
                else assists * (20 / (game_length / 60 + 5))
            )
            adjusted_kda = (kills + adjusted_assists) / deaths

            message = None

            # precedence:
            # good > bad
            # unique > non-unique
            if cspm >= 10:
                message = "might be chovy"
            elif adjusted_kda > 6:
                message = choice(generic_good_messages)
            elif kills == 0 and assists == 0 and deaths >= 5:
                message = "has cancer"
                break
            elif adjusted_kda < 1:
                message = choice(generic_bad_messages)

            if message is not None:
                performance_string = f"<@{player.discord_id}> {message}"
                performance_string += "\n**Victory**" if win is True else "\n**Defeat**"
                performance_string += f"\n{champion_name}"
                performance_string += (
                    f"\n{kills}/{deaths}/{assists} ({int(kp * 100)}% KP)"
                )
                performance_string += f"\n{cs} CS ({cspm}/min)"
                performance_string += (
                    f"\n{int(game_length / 60)}m {int(game_length % 60)}s"
                )

            print(performance_string)
            return performance_string
