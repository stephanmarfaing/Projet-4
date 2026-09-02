from models.round import Round

DEFAULT_NUMBER_OF_ROUNDS = 4


class Tournament:
    def __init__(
        self,
        name: str,
        location: str,
        start_date: str,
        end_date: str,
        id: int = None,
        number_of_rounds: int = DEFAULT_NUMBER_OF_ROUNDS,
        current_round: int = 0,
        rounds: list = None,
        player_ids: list = None,
        description: str = "",
    ):
        self.id = id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.rounds = rounds if rounds is not None else []
        self.player_ids = player_ids if player_ids is not None else []
        self.description = description

    def __repr__(self):
        return (
            f"Tournament(id={self.id}, name={self.name}, location={self.location}, "
            f"start={self.start_date}, end={self.end_date}, "
            f"rounds={self.current_round}/{self.number_of_rounds}, "
            f"players={len(self.player_ids)})"
        )

    def add_player(self, player_id: int):
        if player_id in self.player_ids:
            return False
        self.player_ids.append(player_id)
        return True

    def add_round(self, round_obj: Round):
        self.rounds.append(round_obj)
        self.current_round += 1

    def compute_scores(self):
        """Calcule le score total de chaque joueur à partir des rounds joués."""
        scores = {player_id: 0 for player_id in self.player_ids}
        for round_ in self.rounds:
            for (p1_id, s1), (p2_id, s2) in round_.matches:
                scores[p1_id] += s1
                scores[p2_id] += s2
        return scores

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": [r.to_dict() for r in self.rounds],
            "player_ids": self.player_ids,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            location=data.get("location"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            number_of_rounds=data.get("number_of_rounds", DEFAULT_NUMBER_OF_ROUNDS),
            current_round=data.get("current_round", 0),
            rounds=[Round.from_dict(r) for r in data.get("rounds", [])],
            player_ids=data.get("player_ids", []),
            description=data.get("description", ""),
        )

    @property
    def is_finished(self):
        return self.current_round == self.number_of_rounds
