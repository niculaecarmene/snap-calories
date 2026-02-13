"""
Unit tests for response formatting.
"""
import pytest
from app.utils.formatting import (
    format_nutrition_message,
    format_error_message,
    format_welcome_message
)
from app.models.nutrition import NutritionResult, MacroNutrients, MicroNutrients, FoodItem


class TestFormatting:
    """Test cases for message formatting."""

    def test_format_nutrition_message_with_micros(self):
        """Test formatting complete nutrition result."""
        result = NutritionResult(
            total_calories=645.0,
            macros=MacroNutrients(
                protein=42.0,
                carbohydrates=58.0,
                fat=28.0,
                fiber=9.0
            ),
            micros=MicroNutrients(
                vitamin_a_dv=35.0,
                vitamin_c_dv=42.0,
                vitamin_b12_dv=60.0,
                iron_dv=22.0,
                magnesium_dv=18.0,
                potassium_dv=25.0
            ),
            detected_foods=[],
            overall_confidence=0.78
        )

        message = format_nutrition_message(result)

        # Check key elements are present
        assert "SnapCalories" in message
        assert "645 kcal" in message
        assert "42.0g" in message  # Protein
        assert "58.0g" in message  # Carbs
        assert "28.0g" in message  # Fat
        assert "78%" in message     # Confidence
        assert "Vitamin A: 35% DV" in message
        assert "Iron: 22% DV" in message

    def test_format_nutrition_message_without_micros(self):
        """Test formatting result without micronutrients."""
        result = NutritionResult(
            total_calories=500.0,
            macros=MacroNutrients(
                protein=30.0,
                carbohydrates=50.0,
                fat=20.0,
                fiber=5.0
            ),
            micros=None,
            detected_foods=[],
            overall_confidence=0.65
        )

        message = format_nutrition_message(result)

        # Should have macros but no vitamin/mineral section
        assert "500 kcal" in message
        assert "30.0g" in message
        assert "65%" in message
        # Should not have vitamin sections
        assert message.count("Vitamins:") == 0

    def test_format_error_message_known_type(self):
        """Test formatting known error types."""
        message = format_error_message("invalid_image")
        assert "❌" in message
        assert "image" in message.lower()

        message = format_error_message("no_food_detected")
        assert "🤔" in message
        assert "food" in message.lower()

    def test_format_error_message_with_details(self):
        """Test error message with additional details."""
        message = format_error_message("api_error", "Connection timeout")
        assert "Details: Connection timeout" in message

    def test_format_welcome_message(self):
        """Test welcome message formatting."""
        message = format_welcome_message()

        assert "Welcome" in message
        assert "SnapCalories" in message
        assert "photo" in message.lower()
        assert "📸" in message or "🍽" in message
