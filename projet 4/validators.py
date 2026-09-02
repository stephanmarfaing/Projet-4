"""
Fonctions de validation des saisies utilisateur.
Chaque fonction retourne (True, "") si la valeur est valide,
ou (False, "message d'erreur") sinon.
"""

import re
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"
NATIONAL_ID_PATTERN = re.compile(r"^[A-Z]{2}[0-9]{5}$")  # ex: AB12345


def validate_non_empty(value: str, field_name: str = "Ce champ"):
    if value is None or value.strip() == "":  # retire les espaces avant/après
        return False, f"{field_name} ne peut pas être vide."
    return True, ""


def validate_date(
    value: str, field_name: str = "La date"
):  # valide la date au bon format
    ok, msg = validate_non_empty(value, field_name)
    if not ok:
        return ok, msg
    try:
        datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        return False, f"{field_name} doit être au format AAAA-MM-JJ (ex: 2024-01-31)."
    return True, ""


def validate_optional_positive_int(value: str, field_name: str = "Ce champ"):
    """Valide un entier positif, ou une chaîne vide (valeur par défaut acceptée)."""
    if value is None or value.strip() == "":
        return True, ""
    if not value.strip().isdigit() or int(value.strip()) <= 0:
        return False, f"{field_name} doit être un nombre entier positif (ou vide)."
    return True, ""


def validate_national_id(value: str):
    ok, msg = validate_non_empty(value, "L'identifiant national d'échecs")
    if not ok:
        return ok, msg
    if not NATIONAL_ID_PATTERN.match(value.strip().upper()):
        return (
            False,
            "L'identifiant doit être au format AB12345 (2 lettres + 5 chiffres).",
        )
    return True, ""


def validate_tournament_id(value: str, valid_ids: set):
    """Valide qu'une saisie correspond à l'id d'un tournoi existant."""
    if not value.isdigit() or int(value) not in valid_ids:
        return False, "Merci d'entrer l'id d'un tournoi existant."
    return True, ""
