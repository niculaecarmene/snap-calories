"""
Image processing utilities for validation, resizing, and cleanup.
"""
import os
import logging
from pathlib import Path
from typing import Tuple
from PIL import Image
import base64

from app.config import settings

logger = logging.getLogger(__name__)

# Supported image formats
SUPPORTED_FORMATS = {"JPEG", "JPG", "PNG"}
TEMP_IMAGE_DIR = Path("temp_images")


def ensure_temp_dir() -> Path:
    """Ensure temporary image directory exists."""
    TEMP_IMAGE_DIR.mkdir(exist_ok=True)
    return TEMP_IMAGE_DIR


def validate_image(image_path: str) -> Tuple[bool, str]:
    """
    Validate image format and size.

    Args:
        image_path: Path to the image file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return False, "Image file not found"

        # Check file size
        file_size = os.path.getsize(image_path)
        if file_size > settings.max_image_size_bytes:
            size_mb = file_size / (1024 * 1024)
            return False, f"Image too large ({size_mb:.1f}MB). Max size: {settings.max_image_size_mb}MB"

        # Check if it's a valid image
        with Image.open(image_path) as img:
            # Check format
            if img.format not in SUPPORTED_FORMATS:
                return False, f"Unsupported format: {img.format}. Supported: {', '.join(SUPPORTED_FORMATS)}"

            # Check dimensions (minimum 480x480 recommended)
            width, height = img.size
            if width < 200 or height < 200:
                return False, f"Image too small ({width}x{height}). Minimum 480x480 recommended"

        return True, ""

    except Exception as e:
        logger.error(f"Error validating image: {str(e)}")
        return False, f"Invalid image file: {str(e)}"


def resize_image(image_path: str, max_size: int = 1024) -> str:
    """
    Resize image if larger than max_size while maintaining aspect ratio.

    Args:
        image_path: Path to the image file
        max_size: Maximum dimension (width or height)

    Returns:
        Path to resized image (or original if no resize needed)
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size

            # Only resize if necessary
            if width <= max_size and height <= max_size:
                return image_path

            # Calculate new dimensions maintaining aspect ratio
            if width > height:
                new_width = max_size
                new_height = int((max_size / width) * height)
            else:
                new_height = max_size
                new_width = int((max_size / height) * width)

            # Resize and save
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            resized_path = image_path.replace(".jpg", "_resized.jpg").replace(".png", "_resized.png")
            resized_img.save(resized_path, quality=85, optimize=True)

            logger.info(f"Resized image from {width}x{height} to {new_width}x{new_height}")
            return resized_path

    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        return image_path


def encode_image_base64(image_path: str) -> str:
    """
    Encode image to base64 string for API transmission.

    Args:
        image_path: Path to the image file

    Returns:
        Base64 encoded string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def cleanup_temp_images(image_paths: list[str]) -> None:
    """
    Delete temporary image files (GDPR compliance).

    Args:
        image_paths: List of image paths to delete
    """
    for image_path in image_paths:
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
                logger.info(f"Deleted temporary image: {image_path}")
        except Exception as e:
            logger.error(f"Error deleting image {image_path}: {str(e)}")


def cleanup_all_temp_images() -> None:
    """Delete all files in the temporary image directory."""
    if TEMP_IMAGE_DIR.exists():
        for file in TEMP_IMAGE_DIR.iterdir():
            try:
                if file.is_file():
                    file.unlink()
                    logger.debug(f"Cleaned up: {file}")
            except Exception as e:
                logger.error(f"Error cleaning up {file}: {str(e)}")
