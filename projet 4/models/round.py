from datetime import datetime


class Round:
    """
    Un tour de tournoi : un nom, une liste de matchs, une date/heure de
    début et de fin.

    Un match est stocké comme [joueur_id, score],
    """

    def __init__(
        self,
        name: str,
        matches: list = None,
        # crée une nouvelle liste vide si rien n'est fourni
        start_datetime=None,
        end_datetime=None,
    ):
        self.name = name
        self.matches = matches if matches is not None else []
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def __repr__(self):
        return (
            f"Round(name={self.name}, matches={len(self.matches)}, "
            f"start={self.start_datetime}, end={self.end_datetime})"
        )

    def add_match(
        self, player1_id: int, player2_id: int, score1: float = 0, score2: float = 0
    ):
        self.matches.append(([player1_id, score1], [player2_id, score2]))

    def is_finished(self):  # tour terminé s'il y a une date de fin
        return self.end_datetime is not None

    def to_dict(self):
        return {
            "name": self.name,
            # les tuples sont sérialisés en listes par json.dump automatiquement
            "matches": [list(m) for m in self.matches],
            "start_datetime": (
                self.start_datetime.isoformat() if self.start_datetime else None
            ),
            "end_datetime": (
                self.end_datetime.isoformat() if self.end_datetime else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict):  # récupère de JSON
        matches = [tuple(m) for m in data.get("matches", [])]
        start = data.get("start_datetime")
        end = data.get("end_datetime")
        return cls(
            name=data.get("name"),
            matches=matches,
            start_datetime=datetime.fromisoformat(start) if start else None,
            end_datetime=datetime.fromisoformat(end) if end else None,
        )
