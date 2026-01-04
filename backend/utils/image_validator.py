"""
Image Validation Utilities

This module provides utilities for validating uploaded images.
It checks file type, size, and dimensions to ensure images meet requirements.

Learning Notes:
--------------
1. Image Validation:
   - File type validation (JPEG, PNG only)
   - File size validation (max 5MB)
   - Image dimension validation (min 224x224 for ML models)
   
2. Why These Validations?:
   - File type: Prevent malicious file uploads (executables, scripts)
   - File size: Prevent DoS attacks and storage issues
   - Dimensions: Ensure images are suitable for ML model input
   
3. PIL/Pillow Library:
   - Used for image processing in Python
   - Can read, manipulate, and save images
   - Provides image dimension information
   
4. Security Best Practices:
   - Always validate on server-side (never trust client)
   - Check actual file content, not just extension
   - Use try-except to handle corrupted images
"""

from io import BytesIO
from typing import Tuple, Optional
from PIL import Image
from fastapi import UploadFile, HTTPException

# Configuration
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
MIN_IMAGE_WIDTH = 224
MIN_IMAGE_HEIGHT = 224


async def validate_image_file(file: UploadFile) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded image file.
    Checks file type, size, and dimensions.
    
    Args:
        file: FastAPI UploadFile object
        
    Returns:
        Tuple of (is_valid, error_message)
        If valid: (True, None)
        If invalid: (False, "error message")
        
    Example:
        >>> is_valid, error = await validate_image_file(upload_file)
        >>> if not is_valid:
        ...     raise HTTPException(status_code=400, detail=error)
    """
    # Read file content
    content = await file.read()
    await file.seek(0)  # Reset file pointer for later use
    
    # 1. Validate file size
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        size_mb = file_size / (1024 * 1024)
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, f"File too large ({size_mb:.1f}MB). Maximum size is {max_mb}MB"
    
    if file_size == 0:
        return False, "File is empty"
    
    # 2. Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        return False, f"Invalid file type. Allowed types: JPEG, PNG"
    
    # 3. Validate actual image content and dimensions
    try:
        # Open image using PIL
        image = Image.open(BytesIO(content))
        
        # Verify it's actually an image (PIL will raise exception if not)
        image.verify()
        
        # Re-open image for dimension check (verify() closes the image)
        image = Image.open(BytesIO(content))
        width, height = image.size
        
        # Check minimum dimensions
        if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
            return False, (
                f"Image too small ({width}x{height}). "
                f"Minimum size is {MIN_IMAGE_WIDTH}x{MIN_IMAGE_HEIGHT}"
            )
        
        return True, None
        
    except Exception as e:
        return False, f"Invalid or corrupted image file: {str(e)}"


async def validate_image_or_raise(file: UploadFile) -> None:
    """
    Validate image file and raise HTTPException if invalid.
    Convenience function for use in API endpoints.
    
    Args:
        file: FastAPI UploadFile object
        
    Raises:
        HTTPException: If image is invalid (status 400)
        
    Example:
        >>> @router.post("/upload")
        >>> async def upload_image(file: UploadFile):
        ...     await validate_image_or_raise(file)
        ...     # Continue with upload...
    """
    is_valid, error = await validate_image_file(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)


def get_image_info(content: bytes) -> dict:
    """
    Get information about an image from its content.
    
    Args:
        content: Image file content as bytes
        
    Returns:
        Dictionary with image information (format, size, dimensions)
        
    Example:
        >>> info = get_image_info(image_bytes)
        >>> print(info)
        {
            'format': 'JPEG',
            'mode': 'RGB',
            'width': 1024,
            'height': 768,
            'size_bytes': 245760
        }
    """
    try:
        image = Image.open(BytesIO(content))
        return {
            "format": image.format,
            "mode": image.mode,
            "width": image.size[0],
            "height": image.size[1],
            "size_bytes": len(content)
        }
    except Exception as e:
        return {"error": str(e)}


async def get_image_dimensions(file: UploadFile) -> Tuple[int, int]:
    """
    Get dimensions of uploaded image.
    
    Args:
        file: FastAPI UploadFile object
        
    Returns:
        Tuple of (width, height)
        
    Raises:
        ValueError: If file is not a valid image
        
    Example:
        >>> width, height = await get_image_dimensions(upload_file)
        >>> print(f"Image size: {width}x{height}")
    """
    content = await file.read()
    await file.seek(0)  # Reset file pointer
    
    try:
        image = Image.open(BytesIO(content))
        return image.size
    except Exception as e:
        raise ValueError(f"Cannot read image dimensions: {str(e)}")
