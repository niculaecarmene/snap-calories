"""
WhatsApp Cloud API integration for sending/receiving messages.
"""
import logging
import hmac
import hashlib
from typing import Optional
import httpx

from app.config import settings
from app.models.message import WhatsAppResponse, ImageMessage
from app.models.nutrition import NutritionResult
from app.utils.formatting import format_nutrition_message, format_error_message
from app.utils.image import ensure_temp_dir
from app.services.vision import vision_service
from app.services.nutrition import nutrition_service
from app.services.calculator import nutrition_calculator

logger = logging.getLogger(__name__)


class WhatsAppService:
    """Service for WhatsApp Cloud API integration."""

    def __init__(self):
        """Initialize WhatsApp service."""
        self.api_token = settings.whatsapp_api_token
        self.phone_number_id = settings.whatsapp_phone_number_id
        self.verify_token = settings.whatsapp_verify_token
        self.base_url = f"{settings.whatsapp_api_base_url}/{self.phone_number_id}"

    def verify_webhook(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """
        Verify WhatsApp webhook during setup.

        Args:
            mode: Verification mode
            token: Verification token
            challenge: Challenge string to return

        Returns:
            Challenge string if valid, None otherwise
        """
        if mode == "subscribe" and token == self.verify_token:
            logger.info("Webhook verified successfully")
            return challenge

        logger.warning("Webhook verification failed")
        return None

    def validate_signature(self, payload: bytes, signature: str) -> bool:
        """
        Validate webhook signature for security.

        Args:
            payload: Raw request payload
            signature: X-Hub-Signature-256 header value

        Returns:
            True if valid, False otherwise
        """
        try:
            # WhatsApp signs with sha256
            expected_signature = hmac.new(
                self.api_token.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(
                f"sha256={expected_signature}",
                signature
            )
        except Exception as e:
            logger.error(f"Error validating signature: {str(e)}")
            return False

    async def send_message(self, phone_number: str, message: str) -> bool:
        """
        Send text message via WhatsApp.

        Args:
            phone_number: Recipient phone number
            message: Message text to send

        Returns:
            True if sent successfully
        """
        try:
            url = f"{self.base_url}/messages"
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }

            response_obj = WhatsAppResponse.create_text_message(phone_number, message)

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json=response_obj.model_dump(),
                    timeout=10.0
                )
                response.raise_for_status()

            logger.info(f"Message sent to {phone_number}")
            return True

        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False

    async def download_image(self, media_id: str) -> Optional[str]:
        """
        Download image from WhatsApp.

        Args:
            media_id: WhatsApp media ID

        Returns:
            Path to downloaded image or None
        """
        try:
            # First, get media URL
            url = f"{settings.whatsapp_api_base_url}/{media_id}"
            headers = {"Authorization": f"Bearer {self.api_token}"}

            async with httpx.AsyncClient() as client:
                # Get media URL
                response = await client.get(url, headers=headers, timeout=10.0)
                response.raise_for_status()
                media_url = response.json()["url"]

                # Download the image
                response = await client.get(media_url, headers=headers, timeout=15.0)
                response.raise_for_status()

                # Save to temp directory
                temp_dir = ensure_temp_dir()
                image_path = temp_dir / f"{media_id}.jpg"

                with open(image_path, "wb") as f:
                    f.write(response.content)

                logger.info(f"Image downloaded: {image_path}")
                return str(image_path)

        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            return None

    async def process_meal_image(self, image_msg: ImageMessage) -> None:
        """
        Complete pipeline: download, analyze, calculate, respond.

        Args:
            image_msg: ImageMessage with sender and media info
        """
        image_paths = []

        try:
            # 1. Download image
            logger.info(f"Processing meal image from {image_msg.sender}")
            image_path = await self.download_image(image_msg.media_id)

            if not image_path:
                await self.send_message(
                    image_msg.sender,
                    format_error_message("invalid_image")
                )
                return

            image_paths.append(image_path)

            # 2. Analyze with AI vision
            detected_foods = await vision_service.analyze_food_image(image_path)

            if not detected_foods:
                await self.send_message(
                    image_msg.sender,
                    format_error_message("no_food_detected")
                )
                return

            # 3. Get nutrition data
            nutrition_data = nutrition_service.aggregate_meal_nutrition(detected_foods)

            # 4. Calculate overall confidence
            overall_confidence = await vision_service.calculate_overall_confidence(detected_foods)

            # 5. Create result
            result = nutrition_calculator.create_nutrition_result(
                nutrition_data,
                detected_foods,
                overall_confidence
            )

            # 6. Format and send response
            message = format_nutrition_message(result)
            await self.send_message(image_msg.sender, message)

            logger.info(f"Successfully processed meal for {image_msg.sender}")

        except Exception as e:
            logger.error(f"Error processing meal image: {str(e)}")
            await self.send_message(
                image_msg.sender,
                format_error_message("api_error", str(e))
            )

        finally:
            # 7. Cleanup (GDPR compliance)
            from app.utils.image import cleanup_temp_images
            cleanup_temp_images(image_paths)


# Global instance
whatsapp_service = WhatsAppService()
