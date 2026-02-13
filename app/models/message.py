"""
WhatsApp message models for webhook handling.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


class WhatsAppMedia(BaseModel):
    """Media information from WhatsApp message."""
    id: str = Field(..., description="Media ID from WhatsApp")
    mime_type: str = Field(..., description="MIME type of the media")


class WhatsAppMessageContent(BaseModel):
    """Content of a WhatsApp message."""
    messaging_product: str = "whatsapp"
    from_number: str = Field(..., alias="from", description="Sender's phone number")
    id: str = Field(..., description="Message ID")
    timestamp: str = Field(..., description="Message timestamp")
    type: str = Field(..., description="Message type (text, image, etc.)")

    # Optional fields based on message type
    text: Optional[Dict[str, str]] = None
    image: Optional[WhatsAppMedia] = None

    class Config:
        populate_by_name = True


class WhatsAppValue(BaseModel):
    """Value object in WhatsApp webhook payload."""
    messaging_product: str = "whatsapp"
    metadata: Dict[str, Any]
    contacts: Optional[List[Dict[str, Any]]] = None
    messages: Optional[List[WhatsAppMessageContent]] = None


class WhatsAppEntry(BaseModel):
    """Entry object in WhatsApp webhook payload."""
    id: str
    changes: List[Dict[str, Any]]


class WhatsAppWebhookPayload(BaseModel):
    """Complete WhatsApp webhook payload structure."""
    object: str = Field(..., description="Should be 'whatsapp_business_account'")
    entry: List[WhatsAppEntry]


class ImageMessage(BaseModel):
    """Parsed image message for processing."""
    sender: str = Field(..., description="Sender's phone number")
    media_id: str = Field(..., description="WhatsApp media ID")
    mime_type: str = Field(..., description="Image MIME type")
    timestamp: str = Field(..., description="Message timestamp")
    message_id: str = Field(..., description="WhatsApp message ID")


class WhatsAppResponse(BaseModel):
    """Response message to send via WhatsApp."""
    messaging_product: str = "whatsapp"
    recipient_type: str = "individual"
    to: str = Field(..., description="Recipient phone number")
    type: str = "text"
    text: Dict[str, str] = Field(..., description="Message body")

    @classmethod
    def create_text_message(cls, phone_number: str, message: str) -> "WhatsAppResponse":
        """Create a text message response."""
        return cls(
            to=phone_number,
            text={"body": message}
        )
