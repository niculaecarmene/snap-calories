"""
Food recognition using Hugging Face vision models.
"""
import logging
from typing import List, Dict, Any
from huggingface_hub import InferenceClient
from PIL import Image

from app.config import settings
from app.models.nutrition import FoodItem

logger = logging.getLogger(__name__)


class VisionService:
    """Service for AI-powered food recognition."""

    def __init__(self):
        """Initialize Hugging Face client."""
        self.client = InferenceClient(token=settings.hugging_face_token)
        # Using free food classification model
        self.model_id = "nateraw/food"

    async def analyze_food_image(self, image_path: str) -> List[FoodItem]:
        """
        Analyze food image and return detected items.

        Args:
            image_path: Path to the meal image

        Returns:
            List of detected FoodItem objects
        """
        try:
            logger.info(f"Analyzing image: {image_path}")

            # Open and prepare image
            with Image.open(image_path) as img:
                # Classify the image
                predictions = self.client.image_classification(
                    img,
                    model=self.model_id
                )

            logger.info(f"Received {len(predictions)} predictions")

            # Convert predictions to FoodItem objects
            detected_foods = []
            for pred in predictions[:5]:  # Top 5 predictions
                if pred['score'] > 0.1:  # Only include confident predictions
                    food_item = self._create_food_item(pred)
                    detected_foods.append(food_item)
                    logger.info(f"Detected: {food_item.name} (confidence: {food_item.confidence:.2f})")

            if not detected_foods:
                logger.warning("No food items detected with sufficient confidence")

            return detected_foods

        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            raise Exception(f"Vision analysis failed: {str(e)}")

    def _create_food_item(self, prediction: Dict[str, Any]) -> FoodItem:
        """
        Create FoodItem from prediction.

        Args:
            prediction: Prediction dict from Hugging Face

        Returns:
            FoodItem object
        """
        # Clean up food name
        food_name = prediction['label'].replace('_', ' ').title()

        # Estimate portion (simplified heuristic for MVP)
        # In production, this would use more sophisticated computer vision
        estimated_grams = self._estimate_portion(food_name, prediction['score'])

        return FoodItem(
            name=food_name,
            quantity=estimated_grams,
            unit="g",
            confidence=prediction['score']
        )

    def _estimate_portion(self, food_name: str, confidence: float) -> float:
        """
        Estimate portion size in grams (simplified for MVP).

        Args:
            food_name: Name of the food
            confidence: Detection confidence

        Returns:
            Estimated grams
        """
        # Simple heuristic-based estimation
        # In production, this would use object detection with size estimation

        # Default portions by food type (very simplified)
        default_portions = {
            'protein': 150,  # 150g protein serving
            'vegetable': 100,  # 100g vegetables
            'grain': 150,  # 150g grains/carbs
            'fruit': 120,  # 120g fruit
            'dairy': 100,  # 100g dairy
        }

        # Categorize food (very basic)
        food_lower = food_name.lower()
        if any(word in food_lower for word in ['chicken', 'beef', 'fish', 'meat', 'pork']):
            portion = default_portions['protein']
        elif any(word in food_lower for word in ['salad', 'vegetable', 'broccoli', 'carrot']):
            portion = default_portions['vegetable']
        elif any(word in food_lower for word in ['rice', 'pasta', 'bread', 'potato']):
            portion = default_portions['grain']
        elif any(word in food_lower for word in ['apple', 'banana', 'berry', 'fruit']):
            portion = default_portions['fruit']
        else:
            portion = 100  # Default

        # Adjust based on confidence (lower confidence = might be seeing less of it)
        adjusted_portion = portion * confidence

        return round(adjusted_portion, 0)

    async def calculate_overall_confidence(self, food_items: List[FoodItem]) -> float:
        """
        Calculate overall confidence score.

        Args:
            food_items: List of detected food items

        Returns:
            Overall confidence (0-1)
        """
        if not food_items:
            return 0.0

        # Average confidence of all detected items
        total_confidence = sum(item.confidence for item in food_items)
        return total_confidence / len(food_items)


# Global instance
vision_service = VisionService()
