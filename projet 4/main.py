from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController

MAIN_MENU = [
    ("Lister les tournois", TournamentController.list_tournaments),
    ("Créer un tournoi", TournamentController.create_tournament),
    ("Ajouter un joueur à un tournoi", TournamentController.add_player_to_tournament),
    (
        "Commencer/Continuer un tournoi",
        TournamentController.start_or_continue_tournament,
    ),
    ("Voir le classement d'un tournoi", TournamentController.show_standings),
    ("Rapports", "REPORTS_SUBMENU"),
]

REPORTS_MENU = [
    (
        "Liste de tous les joueurs (ordre alphabétique)",
        ReportController.show_all_players,
    ),
    ("Liste de tous les tournois", ReportController.show_all_tournaments),
    ("Nom et dates d'un tournoi", ReportController.show_tournament_details),
    (
        "Liste des joueurs d'un tournoi (ordre alphabétique)",
        ReportController.show_tournament_players,
    ),
    (
        "Liste des tours et matchs d'un tournoi",
        ReportController.show_tournament_rounds_and_matches,
    ),
]


def run_menu(title, menu, allow_back=False):
    """Boucle générique d'affichage de menu et de sélection d'une option."""
    while True:
        print(f"\n{title} :")
        for i, (label, _) in enumerate(menu, start=1):
            print(f"{i}. {label}")
        exit_label = "0. Retour" if allow_back else "0. Quitter"
        print(exit_label)

        choice = input("Choisissez une option : ").strip()
        if choice == "0":
            return

        if choice.isdigit() and 1 <= int(choice) <= len(menu):
            _, action = menu[int(choice) - 1]
            if action == "REPORTS_SUBMENU":
                run_menu("Rapports", REPORTS_MENU, allow_back=True)
                # pour afficher "Retour" au lieu de "Quitter"
            else:
                action()
        else:
            print("Choix invalide. Veuillez réessayer.")


def main():
    run_menu("Menu principal", MAIN_MENU)


if __name__ == "__main__":
    main()
