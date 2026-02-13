"""
Response formatting utilities for WhatsApp messages.
"""
from app.models.nutrition import NutritionResult


def format_nutrition_message(result: NutritionResult) -> str:
    """
    Format nutrition result into WhatsApp message.

    Args:
        result: NutritionResult object

    Returns:
        Formatted message string
    """
    message_parts = [
        "🍽 *Meal Analysis – SnapCalories*",
        "",
        f"*Estimated Calories:* {result.total_calories:.0f} kcal",
        "",
        "*Macros:*",
        f"• Protein: {result.macros.protein:.1f}g",
        f"• Carbohydrates: {result.macros.carbohydrates:.1f}g",
        f"• Fat: {result.macros.fat:.1f}g",
        f"• Fiber: {result.macros.fiber:.1f}g",
    ]

    # Add micronutrients if available
    if result.micros:
        message_parts.extend([
            "",
            "*Vitamins:*",
        ])

        if result.micros.vitamin_a_dv is not None:
            message_parts.append(f"• Vitamin A: {result.micros.vitamin_a_dv:.0f}% DV")
        if result.micros.vitamin_c_dv is not None:
            message_parts.append(f"• Vitamin C: {result.micros.vitamin_c_dv:.0f}% DV")
        if result.micros.vitamin_b12_dv is not None:
            message_parts.append(f"• Vitamin B12: {result.micros.vitamin_b12_dv:.0f}% DV")

        message_parts.extend([
            "",
            "*Minerals:*",
        ])

        if result.micros.iron_dv is not None:
            message_parts.append(f"• Iron: {result.micros.iron_dv:.0f}% DV")
        if result.micros.magnesium_dv is not None:
            message_parts.append(f"• Magnesium: {result.micros.magnesium_dv:.0f}% DV")
        if result.micros.potassium_dv is not None:
            message_parts.append(f"• Potassium: {result.micros.potassium_dv:.0f}% DV")

    # Add confidence and disclaimer
    message_parts.extend([
        "",
        f"*Confidence:* {result.confidence_percentage}%",
        "",
        f"_{result.disclaimer}_"
    ])

    return "\n".join(message_parts)


def format_error_message(error_type: str, details: str = "") -> str:
    """
    Format error messages for users.

    Args:
        error_type: Type of error
        details: Additional error details

    Returns:
        User-friendly error message
    """
    error_messages = {
        "invalid_image": "❌ Sorry, I couldn't process that image. Please send a clear photo of your meal (JPG or PNG, under 10MB).",
        "no_food_detected": "🤔 I couldn't detect any food in this image. Please send a clearer photo of your meal.",
        "api_error": "⚠️ Something went wrong with the analysis. Please try again in a moment.",
        "timeout": "⏱ The analysis is taking too long. Please try again with a simpler meal photo.",
        "unsupported_message": "📝 Please send me a photo of your meal so I can analyze its nutrition!",
        "rate_limit": "⏸ You're sending photos too quickly! Please wait a moment and try again.",
    }

    base_message = error_messages.get(error_type, "❌ An error occurred. Please try again.")

    if details:
        return f"{base_message}\n\nDetails: {details}"

    return base_message


def format_welcome_message() -> str:
    """Format welcome message for new users."""
    return """👋 *Welcome to SnapCalories!*

Send me a photo of your meal, and I'll instantly analyze its nutritional content.

📸 *How to use:*
1. Take a clear photo of your meal
2. Send it to me
3. Get instant nutrition breakdown!

🎯 I'll tell you:
• Calories and macros
• Vitamins and minerals
• Confidence score

_Note: This is an AI estimate, not medical advice._

Ready? Send your first meal photo! 🍽"""


def format_detected_foods(detected_foods: list) -> str:
    """
    Format list of detected foods.

    Args:
        detected_foods: List of FoodItem objects

    Returns:
        Formatted string of detected foods
    """
    if not detected_foods:
        return ""

    foods = [f"• {food.name} ({food.quantity:.0f}{food.unit})" for food in detected_foods]
    return "\n".join(["", "*Detected items:*"] + foods)
