"""
Nutrition data models for food analysis and results.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class MacroNutrients(BaseModel):
    """Macronutrient breakdown in grams."""
    protein: float = Field(..., ge=0, description="Protein in grams")
    carbohydrates: float = Field(..., ge=0, description="Carbohydrates in grams")
    fat: float = Field(..., ge=0, description="Fat in grams")
    fiber: float = Field(..., ge=0, description="Fiber in grams")


class MicroNutrients(BaseModel):
    """Micronutrient breakdown with Daily Value percentages."""
    vitamin_a_dv: Optional[float] = Field(None, ge=0, le=1000, description="Vitamin A as % DV")
    vitamin_c_dv: Optional[float] = Field(None, ge=0, le=1000, description="Vitamin C as % DV")
    vitamin_b12_dv: Optional[float] = Field(None, ge=0, le=1000, description="Vitamin B12 as % DV")
    iron_dv: Optional[float] = Field(None, ge=0, le=1000, description="Iron as % DV")
    magnesium_dv: Optional[float] = Field(None, ge=0, le=1000, description="Magnesium as % DV")
    potassium_dv: Optional[float] = Field(None, ge=0, le=1000, description="Potassium as % DV")


class FoodItem(BaseModel):
    """Individual food item detected in the image."""
    name: str = Field(..., description="Name of the food item")
    quantity: float = Field(..., gt=0, description="Estimated quantity")
    unit: str = Field(default="g", description="Unit of measurement (g, oz, cup, etc.)")
    confidence: float = Field(..., ge=0, le=1, description="Detection confidence (0-1)")


class NutritionResult(BaseModel):
    """Complete nutrition analysis result."""
    total_calories: float = Field(..., ge=0, description="Total estimated calories")
    macros: MacroNutrients
    micros: Optional[MicroNutrients] = None
    detected_foods: List[FoodItem] = Field(default_factory=list)
    overall_confidence: float = Field(..., ge=0, le=1, description="Overall confidence score (0-1)")
    disclaimer: str = Field(
        default="This is an AI estimate. For medical nutrition advice, consult a healthcare professional.",
        description="Disclaimer message"
    )

    @property
    def confidence_percentage(self) -> int:
        """Convert confidence to percentage for display."""
        return int(self.overall_confidence * 100)
