class ReportView:
    @staticmethod
    def display_players_alphabetical(players):
        if not players:
            print("Aucun joueur enregistré.")
            return
        print("\nListe des joueurs (ordre alphabétique) :")
        print("-" * 40)
        for p in players:
            print(f"{p.last_name} {p.first_name} (id {p.id}, national {p.national_id})")
        print("-" * 40)

    @staticmethod
    def display_tournament_details(tournament):
        print(f"\n{tournament.name} - {tournament.location}")
        print(f"Du {tournament.start_date} au {tournament.end_date}")
        if tournament.description:
            print(f"Description : {tournament.description}")

    @staticmethod
    def display_tournament_rounds(tournament, players):
        if not tournament.rounds:
            print("Aucun tour n'a encore été joué pour ce tournoi.")
            return
        for round_ in tournament.rounds:
            print(f"\n{round_.name}")
            print(f"  Début : {round_.start_datetime}")
            print(
                f"  Fin   : {round_.end_datetime if round_.is_finished() else 'en cours'}"
            )
            for (p1_id, s1), (p2_id, s2) in round_.matches:
                p1 = players[p1_id]
                p2 = players[p2_id]
                print(
                    f"  {p1.first_name} {p1.last_name} ({s1}) vs "
                    f"{p2.first_name} {p2.last_name} ({s2})"
                )
