"""
Unit tests for Pydantic models.
"""
import pytest
from pydantic import ValidationError
from app.models.nutrition import (
    MacroNutrients,
    MicroNutrients,
    FoodItem,
    NutritionResult
)
from app.models.message import WhatsAppResponse, ImageMessage


class TestNutritionModels:
    """Test cases for nutrition models."""

    def test_macro_nutrients_valid(self):
        """Test valid MacroNutrients creation."""
        macros = MacroNutrients(
            protein=30.0,
            carbohydrates=50.0,
            fat=20.0,
            fiber=8.0
        )

        assert macros.protein == 30.0
        assert macros.carbohydrates == 50.0
        assert macros.fat == 20.0
        assert macros.fiber == 8.0

    def test_macro_nutrients_negative_values(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValidationError):
            MacroNutrients(
                protein=-10.0,
                carbohydrates=50.0,
                fat=20.0,
                fiber=8.0
            )

    def test_food_item_valid(self):
        """Test valid FoodItem creation."""
        food = FoodItem(
            name="Chicken Breast",
            quantity=150.0,
            unit="g",
            confidence=0.85
        )

        assert food.name == "Chicken Breast"
        assert food.quantity == 150.0
        assert food.unit == "g"
        assert food.confidence == 0.85

    def test_food_item_confidence_bounds(self):
        """Test that confidence is bounded 0-1."""
        with pytest.raises(ValidationError):
            FoodItem(
                name="Test",
                quantity=100.0,
                confidence=1.5  # Invalid: > 1
            )

    def test_nutrition_result_confidence_percentage(self):
        """Test confidence percentage property."""
        result = NutritionResult(
            total_calories=500.0,
            macros=MacroNutrients(
                protein=30.0,
                carbohydrates=50.0,
                fat=20.0,
                fiber=5.0
            ),
            overall_confidence=0.78
        )

        assert result.confidence_percentage == 78


class TestMessageModels:
    """Test cases for message models."""

    def test_whatsapp_response_create_text_message(self):
        """Test WhatsApp response creation."""
        response = WhatsAppResponse.create_text_message(
            phone_number="1234567890",
            message="Hello World"
        )

        assert response.to == "1234567890"
        assert response.text["body"] == "Hello World"
        assert response.type == "text"
        assert response.messaging_product == "whatsapp"

    def test_image_message_valid(self):
        """Test valid ImageMessage creation."""
        img_msg = ImageMessage(
            sender="1234567890",
            media_id="abc123",
            mime_type="image/jpeg",
            timestamp="1234567890",
            message_id="msg_123"
        )

        assert img_msg.sender == "1234567890"
        assert img_msg.media_id == "abc123"
        assert img_msg.mime_type == "image/jpeg"
