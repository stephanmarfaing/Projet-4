import random
from datetime import datetime

import db
from models.tournament import Tournament
from models.player import Player
from models.round import Round
from views.tournament_view import TournamentView


class TournamentController:
    @staticmethod
    def list_tournaments():
        tournaments = db.load_tournaments()
        TournamentView.display_tournaments(tournaments)

    @staticmethod
    def create_tournament():
        infos = TournamentView.get_create_tournament_infos()
        tournament = Tournament(
            name=infos["name"],
            location=infos["location"],
            start_date=infos["start_date"],
            end_date=infos["end_date"],
            number_of_rounds=infos["number_of_rounds"],
            description=infos["description"],
        )
        tournament = db.create_tournament(tournament)
        TournamentView.confirm_tournament_created(tournament)
        return tournament

    @staticmethod
    def add_player_to_tournament():
        tournaments = db.load_tournaments()
        tournament_id = TournamentView.select_tournament_id(tournaments)
        if tournament_id is None:
            return

        tournament = db.get_tournament_by_id(tournament_id)

        national_id = TournamentView.get_player_national_id()
        player = db.find_player_by_national_id(national_id)

        if player is None:
            infos = TournamentView.get_new_player_infos(national_id)
            player = Player(
                last_name=infos["last_name"],
                first_name=infos["first_name"],
                birth_date=infos["birth_date"],
                national_id=infos["national_id"],
            )
            player = db.create_player(player)

        added = tournament.add_player(player.id)
        if not added:
            TournamentView.notify_player_already_registered(player)
            return

        db.update_tournament(tournament)
        TournamentView.notify_player_added(player, tournament)

    @staticmethod
    def start_or_continue_tournament():
        """Propose les tournois non terminés"""
        tournaments = db.load_tournaments()
        tournament_id = TournamentView.select_unfinished_tournament_id(tournaments)
        if tournament_id is None:
            return
        tournament = db.get_tournament_by_id(tournament_id)

        if tournament.rounds and not tournament.rounds[-1].is_finished():
            current_round = tournament.rounds[-1]
        else:
            if len(tournament.player_ids) < 2:
                TournamentView.notify_not_enough_players()
                return
            current_round = TournamentController._generate_next_round(tournament)

        TournamentController._play_round(tournament, current_round)

    @staticmethod
    def show_standings():
        """Affiche le classement courant (même en cours de tournoi)."""
        tournaments = db.load_tournaments()
        # charge tous les tournois depuis le JSON
        tournament_id = TournamentView.select_tournament_id(tournaments)
        # affiche la liste et demande à l'utilisateur de choisir un id
        if tournament_id is None:
            return
        tournament = db.get_tournament_by_id(tournament_id)
        TournamentController._display_ranking(tournament)

    @staticmethod
    def _display_ranking(tournament):
        players = {p.id: p for p in db.load_players()}
        # pour retrouver un joueur par son id
        scores = tournament.compute_scores()
        ranking = sorted(
            tournament.player_ids, key=lambda pid: scores[pid], reverse=True
        )
        # trie les ids de joueurs par score décroissant
        TournamentView.display_ranking(tournament, ranking, scores, players)
        if tournament.is_finished and ranking:
            winner = players[ranking[0]]
            # annonce le vainqueur que si le tournoi est bien terminé
            # le winner est en position 0
            TournamentView.announce_winner(tournament, winner)

    @staticmethod
    def _get_played_pairs(tournament):
        """Rassemble tous les matchs déjà joués en un ensemble de paires."""
        played = set()
        for round_ in tournament.rounds:
            for (a, _), (b, _) in round_.matches:
                played.add(frozenset((a, b)))
        return played

    @staticmethod
    def _generate_pairs(tournament):
        """Génère les paires selon le système suisse :
        - 1er tour : appariement aléatoire
        - tours suivants : tri par score décroissant, puis appariement des
          joueurs les plus proches au classement, en évitant les matchs
          déjà joués (repli sur un match déjà joué si aucun autre choix)."""
        played_pairs = TournamentController._get_played_pairs(tournament)
        players = tournament.player_ids.copy()
        random.shuffle(players)

        if tournament.current_round > 0:
            scores = tournament.compute_scores()
            players.sort(key=lambda pid: scores[pid], reverse=True)

        pairs = []
        remaining = players.copy()

        while remaining:
            p1 = remaining.pop(0)
            opponent = None
            for p2 in remaining:
                if frozenset((p1, p2)) not in played_pairs:
                    opponent = p2
                    break
            if opponent is None and remaining:
                opponent = remaining[0]

            if opponent is not None:
                remaining.remove(opponent)
                pairs.append((p1, opponent))

        return pairs

    @staticmethod
    def _generate_next_round(tournament):
        """Crée l'objet Round et l'enregistre"""
        round_name = TournamentView.build_round_name(tournament.current_round + 1)
        new_round = Round(name=round_name, start_datetime=datetime.now())
        pairs = TournamentController._generate_pairs(tournament)
        for p1_id, p2_id in pairs:
            new_round.add_match(p1_id, p2_id)
        tournament.rounds.append(new_round)
        tournament.current_round += 1
        db.update_tournament(tournament)
        TournamentView.notify_round_generated(new_round, len(pairs))
        return new_round

    @staticmethod
    def _play_round(tournament, round_obj):
        players = {p.id: p for p in db.load_players()}
        for i, ((p1_id, s1), (p2_id, s2)) in enumerate(round_obj.matches):
            if s1 or s2:
                continue
            p1 = players[p1_id]
            p2 = players[p2_id]
            score1, score2 = TournamentView.get_match_result(p1, p2)
            round_obj.matches[i] = ([p1_id, score1], [p2_id, score2])
            db.update_tournament(tournament)

        round_obj.end_datetime = datetime.now()
        db.update_tournament(tournament)
        TournamentView.notify_round_finished(round_obj)

        if tournament.is_finished:
            TournamentView.notify_tournament_finished(tournament)
            TournamentController._display_ranking(tournament)
            # affichage automatique du classement dès que le dernier tour est terminé
