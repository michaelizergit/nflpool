import requests
from nflpool.data.dbsession import DbSessionFactory
from nflpool.data.nflschedule import NFLSchedule
import nflpool.data.secret as secret
from requests.auth import HTTPBasicAuth
from nflpool.data.seasoninfo import SeasonInfo


'''After updating to a new season, get the NFL game schedule for all 17 weeks including the date of each game
to the database'''


class UpdateScheduleService:
    @classmethod
    def update_nflschedule(cls, season: int, game_id: int, game_date: str, away_team: int,
                              home_team: int, week: int):

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        response = requests.get('https://api.mysportsfeeds.com/v2.0/pull/nfl/' + str(season) +
                                '-regular/games.json',
                                auth=HTTPBasicAuth(secret.msf_api, secret.msf_v2pw))

        schedule_query = response.json()
        team_schedule = schedule_query["games"]

        for schedule in team_schedule:

            game_id = schedule["id"]
            week = schedule["week"]
            game_date = schedule["startTime"]
            away_team = schedule["awayTeam"]["id"]
            home_team = schedule["homeTeam"]["id"]

            season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
            season = season_row.current_season

            add_schedule = NFLSchedule(game_id=game_id, game_date=game_date, away_team=away_team,
                                       home_team=home_team, week=week, season=season)

            session.add(add_schedule)

            session.commit()
