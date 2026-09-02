import json
import os

from models.tournament import Tournament
from models.player import Player

DATA_DIR = "data"  # os.path.join : pour créer fichier windows/lunux ou mac
TOURNAMENTS_JSON = os.path.join(DATA_DIR, "tournaments.json")
PLAYERS_JSON = os.path.join(DATA_DIR, "players.json")


def _load_raw(file_path: str, root_key: str):
    if not os.path.exists(file_path):
        return []  # Si le fichier n'existe pas encore,
        # retourne une liste vide
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(root_key, [])


def _save_raw(file_path: str, root_key: str, items: list):
    # créer le dossier s'il n'existe pas
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({root_key: items}, f, indent=4, ensure_ascii=False)
        # ensure_ascii autorise les accents


def _next_id(items: list):
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


# ---------- Tournaments ----------


def load_tournaments(file_path: str = TOURNAMENTS_JSON):
    raw = _load_raw(file_path, "tournaments")
    return [Tournament.from_dict(t) for t in raw]


def save_tournaments(tournaments: list, file_path: str = TOURNAMENTS_JSON):
    _save_raw(file_path, "tournaments", [t.to_dict() for t in tournaments])


def create_tournament(tournament: Tournament, file_path: str = TOURNAMENTS_JSON):
    tournaments = load_tournaments(file_path)
    raw_items = [t.to_dict() for t in tournaments]
    tournament.id = _next_id(raw_items)
    tournaments.append(tournament)
    save_tournaments(tournaments, file_path)
    return tournament


# Charge l'existant, calcule le nouvel id
# l'assigne à l'objet, l'ajoute à la liste, sauvegarde tout,
# puis renvoie l'objet complet à l'appelant.


def get_tournament_by_id(tournament_id: int, file_path: str = TOURNAMENTS_JSON):
    for t in load_tournaments(file_path):
        if t.id == tournament_id:
            return t
    return None


def update_tournament(tournament: Tournament, file_path: str = TOURNAMENTS_JSON):
    tournaments = load_tournaments(file_path)
    for i, t in enumerate(tournaments):
        if t.id == tournament.id:
            tournaments[i] = tournament
            break
    save_tournaments(tournaments, file_path)


# ---------- Players ----------
# idem que tournaments


def load_players(file_path: str = PLAYERS_JSON):
    raw = _load_raw(file_path, "players")
    return [Player.from_dict(p) for p in raw]


def save_players(players: list, file_path: str = PLAYERS_JSON):
    _save_raw(file_path, "players", [p.to_dict() for p in players])


def create_player(player: Player, file_path: str = PLAYERS_JSON):
    players = load_players(file_path)
    raw_items = [p.to_dict() for p in players]
    player.id = _next_id(raw_items)
    players.append(player)
    save_players(players, file_path)
    return player


def get_player_by_id(player_id: int, file_path: str = PLAYERS_JSON):
    for p in load_players(file_path):
        if p.id == player_id:
            return p
    return None


def find_player_by_national_id(national_id: str, file_path: str = PLAYERS_JSON):
    """compare le national id au lieu de l'id interne auto-généré"""
    national_id = national_id.upper()
    for p in load_players(file_path):
        if p.national_id == national_id:
            return p
    return None
