import pyramid_handlers
from nflpool.controllers.base_controller import BaseController
from nflpool.services.new_season_service import NewSeasonService


class StandingsController(BaseController):
    @pyramid_handlers.action(renderer='templates/standings/standings.pt')
    def index(self):
        # data / service access
        # all_seasons = SeasonsService.get_seasons()

        # return the model - remove '' from all_seasons below once model is written
        return {'seasons': 'all_seasons'}