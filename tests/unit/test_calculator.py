"""
Unit tests for nutrition calculator.
"""
import pytest
from app.services.calculator import NutritionCalculator
from app.models.nutrition import FoodItem


class TestNutritionCalculator:
    """Test cases for NutritionCalculator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = NutritionCalculator()

    def test_calculate_macros(self, sample_nutrition_data):
        """Test macronutrient calculation."""
        macros = self.calculator.calculate_macros(sample_nutrition_data)

        assert macros.protein == 42.0
        assert macros.carbohydrates == 58.0
        assert macros.fat == 28.0
        assert macros.fiber == 9.0

    def test_calculate_calories_from_provided(self, sample_macros, sample_nutrition_data):
        """Test calorie calculation using provided calories."""
        calories = self.calculator.calculate_calories(sample_macros, sample_nutrition_data)

        assert calories == 645.0

    def test_calculate_calories_from_macros(self, sample_macros):
        """Test calorie calculation from macros when not provided."""
        # No calories in data, should calculate from macros
        nutrition_data = {'calories': 0.0}
        calories = self.calculator.calculate_calories(sample_macros, nutrition_data)

        # (42*4) + (58*4) + (28*9) = 168 + 232 + 252 = 652
        assert calories == 652.0

    def test_calculate_micronutrients(self, sample_nutrition_data):
        """Test micronutrient calculation and DV percentages."""
        micros = self.calculator.calculate_micronutrients(sample_nutrition_data)

        # Check calculated percentages
        assert micros.vitamin_a_dv == 35.0  # 315/900 * 100 = 35%
        assert micros.vitamin_c_dv == 42.0  # 38/90 * 100 = 42%
        assert micros.iron_dv == 22.0       # 4/18 * 100 = 22%

    def test_calculate_dv_percentage(self):
        """Test Daily Value percentage calculation."""
        # 90mg of Vitamin C, DV is 90mg
        percentage = self.calculator._calculate_dv_percentage(90, 90)
        assert percentage == 100.0

        # 45mg of Vitamin C, DV is 90mg
        percentage = self.calculator._calculate_dv_percentage(45, 90)
        assert percentage == 50.0

        # Zero amount
        percentage = self.calculator._calculate_dv_percentage(0, 90)
        assert percentage == 0.0

    def test_create_nutrition_result(self, sample_nutrition_data, sample_food_item):
        """Test complete NutritionResult creation."""
        detected_foods = [sample_food_item]
        overall_confidence = 0.85

        result = self.calculator.create_nutrition_result(
            sample_nutrition_data,
            detected_foods,
            overall_confidence
        )

        assert result.total_calories == 645.0
        assert result.macros.protein == 42.0
        assert result.overall_confidence == 0.85
        assert result.confidence_percentage == 85
        assert len(result.detected_foods) == 1
        assert result.micros is not None
