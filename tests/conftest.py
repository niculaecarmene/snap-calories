"""
Pytest configuration and fixtures for testing.
"""
import pytest
from typing import Generator
from fastapi.testclient import TestClient

from app.main import app
from app.models.nutrition import FoodItem, MacroNutrients, MicroNutrients


@pytest.fixture
def client() -> Generator:
    """FastAPI test client fixture."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_food_item() -> FoodItem:
    """Sample FoodItem for testing."""
    return FoodItem(
        name="Grilled Chicken",
        quantity=150.0,
        unit="g",
        confidence=0.85
    )


@pytest.fixture
def sample_macros() -> MacroNutrients:
    """Sample MacroNutrients for testing."""
    return MacroNutrients(
        protein=42.0,
        carbohydrates=58.0,
        fat=28.0,
        fiber=9.0
    )


@pytest.fixture
def sample_micros() -> MicroNutrients:
    """Sample MicroNutrients for testing."""
    return MicroNutrients(
        vitamin_a_dv=35.0,
        vitamin_c_dv=42.0,
        vitamin_b12_dv=60.0,
        iron_dv=22.0,
        magnesium_dv=18.0,
        potassium_dv=25.0
    )


@pytest.fixture
def sample_nutrition_data() -> dict:
    """Sample nutrition data dict for testing."""
    return {
        'protein': 42.0,
        'carbs': 58.0,
        'fat': 28.0,
        'fiber': 9.0,
        'calories': 645.0,
        'vitamin_a': 315.0,  # mcg
        'vitamin_c': 38.0,   # mg
        'vitamin_b12': 1.4,  # mcg
        'iron': 4.0,         # mg
        'magnesium': 76.0,   # mg
        'potassium': 1175.0, # mg
    }
