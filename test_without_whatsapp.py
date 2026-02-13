#!/usr/bin/env python3
"""
Test SnapCalories core functionality without WhatsApp.
Tests vision AI and nutrition calculation with a local image.
"""
import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.vision import vision_service
from app.services.nutrition import nutrition_service
from app.services.calculator import nutrition_calculator
from app.utils.formatting import format_nutrition_message


async def test_meal_analysis(image_path: str):
    """
    Test complete meal analysis pipeline.

    Args:
        image_path: Path to a meal image file
    """
    print("🍽️  SnapCalories - Standalone Test\n")
    print("=" * 50)

    # Check if image exists
    if not Path(image_path).exists():
        print(f"❌ Error: Image not found at {image_path}")
        print("\n💡 Usage: python test_without_whatsapp.py <path_to_meal_image>")
        return

    print(f"📸 Analyzing image: {image_path}\n")

    try:
        # Step 1: AI Vision Analysis
        print("1️⃣  Running AI vision analysis...")
        detected_foods = await vision_service.analyze_food_image(image_path)

        if not detected_foods:
            print("   ❌ No food detected in image")
            return

        print(f"   ✅ Detected {len(detected_foods)} food items:")
        for food in detected_foods:
            print(f"      • {food.name}: {food.quantity}g (confidence: {food.confidence:.0%})")

        # Step 2: Nutrition Lookup
        print("\n2️⃣  Looking up nutrition data...")
        nutrition_data = nutrition_service.aggregate_meal_nutrition(detected_foods)
        print(f"   ✅ Retrieved nutrition for all items")
        print(f"      • Total calories: {nutrition_data.get('calories', 0):.0f} kcal")
        print(f"      • Protein: {nutrition_data.get('protein', 0):.1f}g")
        print(f"      • Carbs: {nutrition_data.get('carbs', 0):.1f}g")
        print(f"      • Fat: {nutrition_data.get('fat', 0):.1f}g")

        # Step 3: Calculate Overall Confidence
        print("\n3️⃣  Calculating confidence score...")
        overall_confidence = await vision_service.calculate_overall_confidence(detected_foods)
        print(f"   ✅ Overall confidence: {overall_confidence:.0%}")

        # Step 4: Create Result
        print("\n4️⃣  Generating final result...")
        result = nutrition_calculator.create_nutrition_result(
            nutrition_data,
            detected_foods,
            overall_confidence
        )
        print("   ✅ Result created")

        # Step 5: Format Message
        print("\n5️⃣  Formatting WhatsApp message...\n")
        message = format_nutrition_message(result)

        # Display Result
        print("=" * 50)
        print("\n📱 WHATSAPP MESSAGE OUTPUT:\n")
        print(message)
        print("\n" + "=" * 50)

        print("\n✅ Test completed successfully!")
        print("\n💡 This is what users would see on WhatsApp")

    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python test_without_whatsapp.py <path_to_meal_image>")
        print("\nExample:")
        print("  python test_without_whatsapp.py meal.jpg")
        print("\n💡 Download a sample meal image from the internet to test")
        sys.exit(1)

    image_path = sys.argv[1]
    asyncio.run(test_meal_analysis(image_path))


if __name__ == "__main__":
    main()
