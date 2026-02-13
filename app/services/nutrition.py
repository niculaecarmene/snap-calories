"""
USDA FoodData Central API integration for nutrition data.
"""
import logging
from typing import Optional, Dict, Any, List
import requests

from app.config import settings
from app.models.nutrition import FoodItem

logger = logging.getLogger(__name__)


class NutritionService:
    """Service for fetching nutrition data from USDA FoodData Central."""

    def __init__(self):
        """Initialize USDA API client."""
        self.base_url = settings.usda_api_base_url
        self.api_key = settings.usda_api_key

    def search_food(self, food_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for food in USDA database.

        Args:
            food_name: Name of the food to search

        Returns:
            Best matching food data or None
        """
        try:
            url = f"{self.base_url}/foods/search"
            params = {
                "api_key": self.api_key,
                "query": food_name,
                "pageSize": 5,
                "dataType": ["Foundation", "SR Legacy"]
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()

            if data.get('foods') and len(data['foods']) > 0:
                # Return the best match (first result)
                best_match = data['foods'][0]
                logger.info(f"Found match for '{food_name}': {best_match.get('description')}")
                return best_match

            logger.warning(f"No USDA data found for: {food_name}")
            return None

        except Exception as e:
            logger.error(f"Error searching USDA for '{food_name}': {str(e)}")
            return None

    def get_nutrition_for_food(self, food_item: FoodItem) -> Dict[str, float]:
        """
        Get nutrition data for a food item and scale to portion.

        Args:
            food_item: FoodItem with name and quantity

        Returns:
            Dict with nutrition values scaled to portion
        """
        # Search USDA database
        food_data = self.search_food(food_item.name)

        if not food_data:
            # Return default values if not found
            logger.warning(f"Using default values for: {food_item.name}")
            return self._get_default_nutrition(food_item)

        # Extract nutrients from USDA data
        nutrients = self._extract_nutrients(food_data)

        # Scale to portion size
        scaled_nutrients = self._scale_to_portion(nutrients, food_item.quantity)

        return scaled_nutrients

    def _extract_nutrients(self, food_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract relevant nutrients from USDA food data.

        Args:
            food_data: USDA food data response

        Returns:
            Dict of nutrient values per 100g
        """
        nutrients = {
            'protein': 0.0,
            'carbs': 0.0,
            'fat': 0.0,
            'fiber': 0.0,
            'calories': 0.0,
            # Micronutrients
            'vitamin_a': 0.0,
            'vitamin_c': 0.0,
            'vitamin_b12': 0.0,
            'iron': 0.0,
            'magnesium': 0.0,
            'potassium': 0.0,
        }

        # USDA nutrient ID mapping
        nutrient_mapping = {
            '1003': 'protein',  # Protein
            '1005': 'carbs',    # Carbohydrate
            '1004': 'fat',      # Total lipid (fat)
            '1079': 'fiber',    # Fiber
            '1008': 'calories', # Energy (kcal)
            '1106': 'vitamin_a',  # Vitamin A
            '1162': 'vitamin_c',  # Vitamin C
            '1178': 'vitamin_b12',  # Vitamin B-12
            '1089': 'iron',     # Iron
            '1090': 'magnesium',  # Magnesium
            '1092': 'potassium',  # Potassium
        }

        if 'foodNutrients' in food_data:
            for nutrient in food_data['foodNutrients']:
                nutrient_id = str(nutrient.get('nutrientId', ''))
                if nutrient_id in nutrient_mapping:
                    key = nutrient_mapping[nutrient_id]
                    value = nutrient.get('value', 0.0)
                    nutrients[key] = float(value)

        logger.debug(f"Extracted nutrients: {nutrients}")
        return nutrients

    def _scale_to_portion(self, nutrients: Dict[str, float], grams: float) -> Dict[str, float]:
        """
        Scale nutrient values from 100g to actual portion.

        Args:
            nutrients: Nutrient values per 100g
            grams: Actual portion size in grams

        Returns:
            Scaled nutrient values
        """
        scale_factor = grams / 100.0
        return {key: value * scale_factor for key, value in nutrients.items()}

    def _get_default_nutrition(self, food_item: FoodItem) -> Dict[str, float]:
        """
        Return default/estimated nutrition values when USDA data unavailable.

        Args:
            food_item: Food item needing default values

        Returns:
            Dict with estimated nutrition values
        """
        # Very basic defaults (should be improved with a local database)
        defaults_per_100g = {
            'protein': 15.0,
            'carbs': 25.0,
            'fat': 8.0,
            'fiber': 3.0,
            'calories': 200.0,
            'vitamin_a': 50.0,
            'vitamin_c': 10.0,
            'vitamin_b12': 0.5,
            'iron': 2.0,
            'magnesium': 30.0,
            'potassium': 200.0,
        }

        return self._scale_to_portion(defaults_per_100g, food_item.quantity)

    def aggregate_meal_nutrition(self, food_items: List[FoodItem]) -> Dict[str, float]:
        """
        Get total nutrition for all food items in a meal.

        Args:
            food_items: List of detected food items

        Returns:
            Aggregated nutrition values
        """
        total = {
            'protein': 0.0,
            'carbs': 0.0,
            'fat': 0.0,
            'fiber': 0.0,
            'calories': 0.0,
            'vitamin_a': 0.0,
            'vitamin_c': 0.0,
            'vitamin_b12': 0.0,
            'iron': 0.0,
            'magnesium': 0.0,
            'potassium': 0.0,
        }

        for food_item in food_items:
            nutrition = self.get_nutrition_for_food(food_item)
            for key in total.keys():
                total[key] += nutrition.get(key, 0.0)

        logger.info(f"Total meal nutrition: {total}")
        return total


# Global instance
nutrition_service = NutritionService()
