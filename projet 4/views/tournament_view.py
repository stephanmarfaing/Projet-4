from validators import (
    validate_non_empty,
    validate_date,
    validate_national_id,
    validate_optional_positive_int,
    validate_tournament_id,
)
from models.tournament import DEFAULT_NUMBER_OF_ROUNDS


def _prompt_valid(prompt: str, validator, *args):
    """Redemande la saisie tant qu'elle n'est pas valide selon validator."""
    while True:
        value = input(prompt).strip()
        ok, error = validator(value, *args)
        if ok:
            return value
        print(f"Erreur : {error}")


class TournamentView:
    @staticmethod
    def display_tournaments(tournaments):
        if not tournaments:
            print("Aucun tournoi enregistré.")
            return
        for t in tournaments:
            print(
                f"[{t.id}] {t.name} - {t.location} - du {t.start_date} au {t.end_date} "
                f"- tour {t.current_round}/{t.number_of_rounds} "
                f"({len(t.player_ids)} joueur(s))"
            )

    @staticmethod
    def get_create_tournament_infos():
        name = _prompt_valid("Nom du tournoi : ", validate_non_empty, "Le nom")
        location = _prompt_valid("Lieu du tournoi : ", validate_non_empty, "Le lieu")
        start_date = _prompt_valid(
            "Date de début (AAAA-MM-JJ) : ", validate_date, "La date de début"
        )
        end_date = _prompt_valid(
            "Date de fin (AAAA-MM-JJ) : ", validate_date, "La date de fin"
        )
        nb_rounds_raw = _prompt_valid(
            f"Nombre de tours (défaut {DEFAULT_NUMBER_OF_ROUNDS}, laisser vide pour "
            f"la valeur par défaut) : ",
            validate_optional_positive_int,
            "Le nombre de tours",
        )
        number_of_rounds = (
            int(nb_rounds_raw) if nb_rounds_raw else DEFAULT_NUMBER_OF_ROUNDS
        )
        description = input("Description / remarques générales (facultatif) : ").strip()
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "number_of_rounds": number_of_rounds,
            "description": description,
        }

    @staticmethod
    def confirm_tournament_created(tournament):
        print(f"Tournoi créé avec succès : {tournament}")

    @staticmethod
    def select_tournament_id(tournaments):
        TournamentView.display_tournaments(tournaments)
        if not tournaments:
            return None
        valid_ids = {t.id for t in tournaments}
        chosen = _prompt_valid("Id du tournoi : ", validate_tournament_id, valid_ids)
        return int(chosen)

    @staticmethod
    def get_player_national_id():
        return _prompt_valid(
            "Identifiant national d'échecs (ex: AB12345) : ", validate_national_id
        )

    @staticmethod
    def get_new_player_infos(national_id):
        last_name = _prompt_valid("Nom du joueur : ", validate_non_empty, "Le nom")
        first_name = _prompt_valid(
            "Prénom du joueur : ", validate_non_empty, "Le prénom"
        )
        birth_date = _prompt_valid("Date de naissance (AAAA-MM-JJ) : ", validate_date)
        return {
            "last_name": last_name,
            "first_name": first_name,
            "birth_date": birth_date,
            "national_id": national_id,
        }

    @staticmethod
    def display_message(message: str):
        print(message)

    @staticmethod
    def notify_player_already_registered(player):
        print(f"{player.first_name} {player.last_name} est déjà inscrit à ce tournoi.")

    @staticmethod
    def notify_player_added(player, tournament):
        print(
            f"{player.first_name} {player.last_name} a été ajouté au tournoi "
            f"'{tournament.name}'."
        )

    @staticmethod
    def notify_not_enough_players():
        print("Il faut au moins 2 joueurs inscrits pour démarrer un tour.")

    @staticmethod
    def build_round_name(round_number: int):
        return f"Round {round_number}"

    @staticmethod
    def notify_round_generated(round_obj, nb_matches: int):
        print(f"{round_obj.name} généré avec {nb_matches} match(s).")

    @staticmethod
    def notify_round_finished(round_obj):
        print(f"{round_obj.name} terminé.")

    @staticmethod
    def notify_tournament_finished(tournament):
        print(f"Tournoi '{tournament.name}' terminé !")

    @staticmethod
    def select_unfinished_tournament_id(tournaments):
        unfinished = [t for t in tournaments if not t.is_finished]
        if not unfinished:
            print("Aucun tournoi en cours ou à démarrer.")
            return None
        return TournamentView.select_tournament_id(unfinished)

    @staticmethod
    def get_match_result(player1, player2):
        print(
            f"\n{player1.first_name} {player1.last_name}  vs  "
            f"{player2.first_name} {player2.last_name}"
        )
        choice = _prompt_valid(
            "Résultat (1 = victoire joueur 1, 2 = victoire joueur 2, 3 = match nul) : ",
            lambda v, _="": (v in ("1", "2", "3"), "Entrez 1, 2 ou 3."),
        )
        if choice == "1":
            return 1, 0
        if choice == "2":
            return 0, 1
        return 0.5, 0.5

    @staticmethod
    def display_ranking(tournament, ranking, scores, players):
        print(f"\nClassement - {tournament.name}")
        print("-" * 40)
        for rank, player_id in enumerate(ranking, start=1):
            player = players[player_id]
            print(
                f"{rank}. {player.first_name} {player.last_name} "
                f"- {scores[player_id]} pt(s)"
            )
        print("-" * 40)

    @staticmethod
    def announce_winner(tournament, winner):
        print(
            f"\n🏆 Vainqueur du tournoi '{tournament.name}' : "
            f"{winner.first_name} {winner.last_name} 🏆\n"
        )
