"""
Nutrition calculation engine for macros, calories, and micronutrients.
"""
import logging
from typing import Dict, List

from app.models.nutrition import MacroNutrients, MicroNutrients, NutritionResult, FoodItem

logger = logging.getLogger(__name__)


class NutritionCalculator:
    """Calculator for nutrition values and daily value percentages."""

    # Daily Value (DV) reference values based on 2000 calorie diet
    DAILY_VALUES = {
        'vitamin_a': 900,  # mcg RAE
        'vitamin_c': 90,   # mg
        'vitamin_b12': 2.4,  # mcg
        'iron': 18,  # mg
        'magnesium': 420,  # mg
        'potassium': 4700,  # mg
    }

    def calculate_macros(self, nutrition_data: Dict[str, float]) -> MacroNutrients:
        """
        Extract macronutrient values.

        Args:
            nutrition_data: Dict with nutrition values

        Returns:
            MacroNutrients object
        """
        return MacroNutrients(
            protein=nutrition_data.get('protein', 0.0),
            carbohydrates=nutrition_data.get('carbs', 0.0),
            fat=nutrition_data.get('fat', 0.0),
            fiber=nutrition_data.get('fiber', 0.0)
        )

    def calculate_calories(self, macros: MacroNutrients, nutrition_data: Dict[str, float]) -> float:
        """
        Calculate total calories.
        Uses provided calories if available, otherwise calculates from macros.

        Args:
            macros: MacroNutrients object
            nutrition_data: Raw nutrition data

        Returns:
            Total calories
        """
        # Use provided calories if available
        if nutrition_data.get('calories', 0.0) > 0:
            return round(nutrition_data['calories'], 0)

        # Otherwise calculate from macros
        # Protein: 4 cal/g, Carbs: 4 cal/g, Fat: 9 cal/g
        calculated = (
            (macros.protein * 4.0) +
            (macros.carbohydrates * 4.0) +
            (macros.fat * 9.0)
        )

        return round(calculated, 0)

    def calculate_micronutrients(self, nutrition_data: Dict[str, float]) -> MicroNutrients:
        """
        Calculate micronutrient values with Daily Value percentages.

        Args:
            nutrition_data: Dict with nutrition values

        Returns:
            MicroNutrients object with DV percentages
        """
        return MicroNutrients(
            vitamin_a_dv=self._calculate_dv_percentage(
                nutrition_data.get('vitamin_a', 0.0),
                self.DAILY_VALUES['vitamin_a']
            ),
            vitamin_c_dv=self._calculate_dv_percentage(
                nutrition_data.get('vitamin_c', 0.0),
                self.DAILY_VALUES['vitamin_c']
            ),
            vitamin_b12_dv=self._calculate_dv_percentage(
                nutrition_data.get('vitamin_b12', 0.0),
                self.DAILY_VALUES['vitamin_b12']
            ),
            iron_dv=self._calculate_dv_percentage(
                nutrition_data.get('iron', 0.0),
                self.DAILY_VALUES['iron']
            ),
            magnesium_dv=self._calculate_dv_percentage(
                nutrition_data.get('magnesium', 0.0),
                self.DAILY_VALUES['magnesium']
            ),
            potassium_dv=self._calculate_dv_percentage(
                nutrition_data.get('potassium', 0.0),
                self.DAILY_VALUES['potassium']
            )
        )

    def _calculate_dv_percentage(self, amount: float, daily_value: float) -> float:
        """
        Calculate Daily Value percentage.

        Args:
            amount: Amount of nutrient
            daily_value: Daily Value reference

        Returns:
            Percentage of Daily Value
        """
        if daily_value == 0:
            return 0.0

        percentage = (amount / daily_value) * 100.0
        return round(percentage, 0)

    def create_nutrition_result(
        self,
        nutrition_data: Dict[str, float],
        detected_foods: List[FoodItem],
        overall_confidence: float
    ) -> NutritionResult:
        """
        Create complete NutritionResult from all data.

        Args:
            nutrition_data: Aggregated nutrition data
            detected_foods: List of detected food items
            overall_confidence: Overall detection confidence

        Returns:
            Complete NutritionResult object
        """
        macros = self.calculate_macros(nutrition_data)
        calories = self.calculate_calories(macros, nutrition_data)
        micros = self.calculate_micronutrients(nutrition_data)

        return NutritionResult(
            total_calories=calories,
            macros=macros,
            micros=micros,
            detected_foods=detected_foods,
            overall_confidence=overall_confidence
        )


# Global instance
nutrition_calculator = NutritionCalculator()
