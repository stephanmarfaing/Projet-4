import db
from views.report_view import ReportView
from views.tournament_view import TournamentView


class ReportController:
    @staticmethod
    def _sorted_players(players):
        return sorted(
            players, key=lambda p: (p.last_name.lower(), p.first_name.lower())
        )

    @staticmethod
    def show_all_players():
        players = ReportController._sorted_players(db.load_players())
        ReportView.display_players_alphabetical(players)

    @staticmethod
    def show_all_tournaments():
        tournaments = db.load_tournaments()
        TournamentView.display_tournaments(tournaments)

    @staticmethod
    def show_tournament_details():
        tournaments = db.load_tournaments()
        tournament_id = TournamentView.select_tournament_id(tournaments)
        if tournament_id is None:
            return
        tournament = db.get_tournament_by_id(tournament_id)
        ReportView.display_tournament_details(tournament)

    @staticmethod
    def show_tournament_players():
        tournaments = db.load_tournaments()
        tournament_id = TournamentView.select_tournament_id(tournaments)
        if tournament_id is None:
            return
        tournament = db.get_tournament_by_id(tournament_id)
        all_players = {p.id: p for p in db.load_players()}
        players = ReportController._sorted_players(
            [all_players[pid] for pid in tournament.player_ids]
        )
        # liste qui convertit les ids inscrits au tournoi en objets Player complets
        ReportView.display_players_alphabetical(players)

    @staticmethod
    def show_tournament_rounds_and_matches():
        tournaments = db.load_tournaments()
        tournament_id = TournamentView.select_tournament_id(tournaments)
        if tournament_id is None:
            return
        tournament = db.get_tournament_by_id(tournament_id)
        all_players = {p.id: p for p in db.load_players()}
        ReportView.display_tournament_rounds(tournament, all_players)
