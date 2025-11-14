"""Utilities for loading botanical datasets."""

from __future__ import annotations

from csv import DictReader
from pathlib import Path
from typing import Any

NORMALIZED_HEADERS = {
    "Nom commun": "nom_commun",
    "Nom scientifique": "nom_scientifique",
    "Type": "type",
    "Description générale": "description",
    "Hauteur cm": ("hauteur_min", "hauteur_max"),
    "Largeur cm": ("largeur_min", "largeur_max"),
    "Plantes compagnons": "compagnons",
    "Utilisation": "utilisation",
    "pH": ("ph_min", "ph_max"),
    "Humidité": "humidite",
    "Exposition": "exposition",
    "Feuillage": "feuillage",
    "Port": "port",
    "Racines": "racines",
    "Ecologie": "ecologie",
    "Usages paysagers": "usages_paysagers",
    "Engrais": "engrais",
    "Floraison": "floraison",
    "Couleur fleur": "couleur_fleur",
    "Fructification": "fructification",
    "Toxique": "toxique",
    "Remarques": "remarques",
}


def _coerce_numeric(value: str) -> float | int | None:
    """Convert a numeric string into an int or float when possible."""
    candidate = value.replace(",", ".").strip()
    if not candidate:
        return None

    try:
        number = float(candidate)
    except ValueError:
        return None

    if number.is_integer():
        return int(number)
    return number


def _parse_range(value: str) -> tuple[float | int | None, float | int | None]:
    cleaned = (value or "").strip()
    if not cleaned:
        return None, None

    parts = [part.strip() for part in cleaned.split("-", maxsplit=1)]
    if len(parts) == 2:
        start = _coerce_numeric(parts[0])
        end = _coerce_numeric(parts[1])
    else:
        start = end = _coerce_numeric(parts[0])
    return start, end


def load_plants_csv(path: Path) -> list[dict[str, Any]]:
    """Load a CSV file describing plants into a list of normalized dictionaries."""
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = DictReader(handle, delimiter=";")
        for row in reader:
            normalized: dict[str, Any] = {}
            for header, normalized_key in NORMALIZED_HEADERS.items():
                value = row.get(header, "") if row else ""
                if isinstance(normalized_key, tuple):
                    lower, upper = _parse_range(value or "")
                    first_key, second_key = normalized_key
                    normalized[first_key] = lower
                    normalized[second_key] = upper
                else:
                    normalized[normalized_key] = (value or "").strip()
            records.append(normalized)
    return records
