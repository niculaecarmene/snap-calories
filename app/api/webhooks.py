"""
WhatsApp webhook endpoints for receiving messages.
"""
import logging
from fastapi import APIRouter, Request, Response, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional

from app.services.whatsapp import whatsapp_service
from app.models.message import WhatsAppWebhookPayload, ImageMessage
from app.utils.formatting import format_error_message, format_welcome_message

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhooks"])


@router.get("")
async def verify_webhook(request: Request) -> Response:
    """
    Verify WhatsApp webhook during setup.
    Meta will call this endpoint with specific query parameters.

    Query Parameters:
        hub.mode: Should be 'subscribe'
        hub.verify_token: Token to verify (matches WHATSAPP_VERIFY_TOKEN)
        hub.challenge: Challenge string to return

    Returns:
        Challenge string if verification succeeds
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    logger.info(f"Webhook verification request: mode={mode}")

    if not mode or not token:
        raise HTTPException(status_code=400, detail="Missing parameters")

    result = whatsapp_service.verify_webhook(mode, token, challenge)

    if result:
        return Response(content=result, media_type="text/plain")

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("")
async def receive_webhook(
    request: Request,
    background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """
    Receive WhatsApp webhook notifications.
    Processes incoming messages and triggers analysis in background.

    Returns:
        200 OK immediately (processing continues in background)
    """
    try:
        # Get raw body for signature validation
        body = await request.body()

        # Validate signature (optional but recommended for production)
        signature = request.headers.get("X-Hub-Signature-256", "")
        if signature and not whatsapp_service.validate_signature(body, signature):
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=403, detail="Invalid signature")

        # Parse webhook payload
        data = await request.json()
        logger.info(f"Received webhook: {data}")

        # Parse and process the message
        try:
            payload = WhatsAppWebhookPayload(**data)
            image_msg = _extract_image_message(payload)

            if image_msg:
                # Process image in background to return 200 quickly
                background_tasks.add_task(
                    whatsapp_service.process_meal_image,
                    image_msg
                )
                logger.info(f"Queued image processing for {image_msg.sender}")
            else:
                # Handle non-image messages
                text_sender = _extract_text_sender(payload)
                if text_sender:
                    background_tasks.add_task(
                        whatsapp_service.send_message,
                        text_sender,
                        format_error_message("unsupported_message")
                    )

        except Exception as e:
            logger.error(f"Error parsing webhook payload: {str(e)}")
            # Still return 200 to acknowledge receipt

        # Always return 200 OK immediately
        return {"status": "received"}

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        # Return 200 even on errors to prevent WhatsApp from retrying
        return {"status": "error", "message": str(e)}


def _extract_image_message(payload: WhatsAppWebhookPayload) -> Optional[ImageMessage]:
    """
    Extract image message from webhook payload.

    Args:
        payload: Parsed webhook payload

    Returns:
        ImageMessage if found, None otherwise
    """
    try:
        for entry in payload.entry:
            for change in entry.changes:
                value = change.get("value", {})
                messages = value.get("messages", [])

                for message in messages:
                    if message.get("type") == "image":
                        image_data = message.get("image", {})
                        return ImageMessage(
                            sender=message.get("from"),
                            media_id=image_data.get("id"),
                            mime_type=image_data.get("mime_type", "image/jpeg"),
                            timestamp=message.get("timestamp"),
                            message_id=message.get("id")
                        )
    except Exception as e:
        logger.error(f"Error extracting image message: {str(e)}")

    return None


def _extract_text_sender(payload: WhatsAppWebhookPayload) -> Optional[str]:
    """
    Extract sender phone number from text message.

    Args:
        payload: Parsed webhook payload

    Returns:
        Phone number if found, None otherwise
    """
    try:
        for entry in payload.entry:
            for change in entry.changes:
                value = change.get("value", {})
                messages = value.get("messages", [])

                for message in messages:
                    if message.get("type") == "text":
                        return message.get("from")
    except Exception as e:
        logger.error(f"Error extracting text sender: {str(e)}")

    return None
