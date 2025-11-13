from __future__ import annotations

import pytest

from mycelia_ai.botany.database import BotanyDatabase


@pytest.fixture(scope="module")
def botany_db() -> BotanyDatabase:
    return BotanyDatabase()


def test_database_contains_plants(botany_db: BotanyDatabase) -> None:
    plants = botany_db.all_plants()
    assert len(plants) >= 10


def test_find_by_common_name(botany_db: BotanyDatabase) -> None:
    results = botany_db.find_by_common_name("Achillée")
    scientific_names = {plant["nom_scientifique"] for plant in results}
    assert "Achillea millefolium" in scientific_names


def test_find_by_scientific_name(botany_db: BotanyDatabase) -> None:
    results = botany_db.find_by_scientific_name("Lavandula angustifolia")
    assert results


def test_height_fields_are_numeric(botany_db: BotanyDatabase) -> None:
    sample = next(
        (
            plant
            for plant in botany_db.all_plants()
            if plant.get("hauteur_min") is not None
            and plant.get("hauteur_max") is not None
        ),
        None,
    )
    assert sample is not None
    assert isinstance(sample["hauteur_min"], (int, float))
    assert isinstance(sample["hauteur_max"], (int, float))
