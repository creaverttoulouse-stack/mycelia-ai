"""In-memory botanical database backed by the CSV dataset."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any
import unicodedata

from .importer import load_plants_csv


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _normalize_common_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    stripped = "".join(char for char in normalized if not unicodedata.combining(char))
    return stripped.lower()


def _normalize_scientific_name(value: str) -> str:
    return value.lower()


class BotanyDatabase:
    """Simple in-memory search API for plants."""

    def __init__(self, csv_path: Path | None = None) -> None:
        if csv_path is None:
            csv_path = _project_root() / "data" / "plants_massif.csv"
        self._csv_path = csv_path
        self.plants = load_plants_csv(csv_path)
        self._common_lookup: dict[str, list[dict[str, Any]]] = {}
        self._common_keys: list[tuple[str, dict[str, Any]]] = []
        self._scientific_lookup: dict[str, list[dict[str, Any]]] = {}
        self._scientific_keys: list[tuple[str, dict[str, Any]]] = []
        self._build_indexes()

    def _build_indexes(self) -> None:
        for plant in self.plants:
            common = plant.get("nom_commun", "")
            if common:
                normalized = _normalize_common_name(common)
                self._common_lookup.setdefault(normalized, []).append(plant)
                self._common_keys.append((normalized, plant))
            scientific = plant.get("nom_scientifique", "")
            if scientific:
                normalized_scientific = _normalize_scientific_name(scientific)
                self._scientific_lookup.setdefault(normalized_scientific, []).append(plant)
                self._scientific_keys.append((normalized_scientific, plant))

    def all_plants(self) -> list[dict[str, Any]]:
        return list(self.plants)

    def find_by_common_name(self, query: str) -> list[dict[str, Any]]:
        normalized_query = _normalize_common_name(query)
        results = list(self._common_lookup.get(normalized_query, []))
        for key, plant in self._common_keys:
            if normalized_query in key and plant not in results:
                results.append(plant)
        return results

    def find_by_scientific_name(self, query: str) -> list[dict[str, Any]]:
        normalized_query = _normalize_scientific_name(query)
        results = list(self._scientific_lookup.get(normalized_query, []))
        for key, plant in self._scientific_keys:
            if normalized_query in key and plant not in results:
                results.append(plant)
        return results

    def search(
        self,
        *,
        ph: float | tuple[float | int | None, float | int | None] | None = None,
        soleil: Any | None = None,
        humidite: str | None = None,
    ) -> list[dict[str, Any]]:
        results = self.plants
        if ph is not None:
            if isinstance(ph, (tuple, list)) and len(ph) == 2:
                min_ph, max_ph = ph
            else:
                min_ph = max_ph = ph
            filtered: list[dict[str, Any]] = []
            for plant in results:
                plant_min = plant.get("ph_min")
                plant_max = plant.get("ph_max")
                if plant_min is None and plant_max is None:
                    continue
                if min_ph is not None and plant_max is not None and plant_max < min_ph:
                    continue
                if max_ph is not None and plant_min is not None and plant_min > max_ph:
                    continue
                filtered.append(plant)
            results = filtered

        if humidite is not None:
            query = humidite.strip().lower()
            results = [
                plant
                for plant in results
                if query in (plant.get("humidite") or "").lower()
            ]

        # soleil parameter is reserved for future use.
        return list(results)


@lru_cache(maxsize=1)
def get_default_botany_db() -> BotanyDatabase:
    return BotanyDatabase()
