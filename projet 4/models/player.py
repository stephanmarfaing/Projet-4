class Player:
    def __init__(self, last_name: str, first_name: str, birth_date: str,
                 national_id: str, id: int = None):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_id = national_id.upper()

    def __repr__(self):  # défini ce qu'il s'affiche quand on fait print(un_joueur)
        return (f"Player(id={self.id}, name={self.first_name} {self.last_name}, "
                f"national_id={self.national_id})")

    def to_dict(self):       # Transforme en dictionnaire pour JSON
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "national_id": self.national_id,
        }

    @classmethod           # Reconstruit le player via le dictionnaire JSON
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            last_name=data.get("last_name"),
            first_name=data.get("first_name"),
            birth_date=data.get("birth_date"),
            national_id=data.get("national_id"),
        )
