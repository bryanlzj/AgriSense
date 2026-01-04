"""
File Storage Utilities

This module provides utilities for handling file uploads and storage.
It includes functions for saving files with unique names, generating URLs,
and managing the uploads directory.

Learning Notes:
--------------
1. File Storage Strategy:
   - Store files in local filesystem (backend/uploads/)
   - Generate unique filenames using UUID to prevent conflicts
   - Preserve original file extension for proper MIME type handling
   
2. Security Considerations:
   - Never trust user-provided filenames (use UUID instead)
   - Validate file types before saving
   - Store files outside of web root when possible
   - Use proper file permissions
   
3. Production Considerations:
   - For production, consider cloud storage (AWS S3, Google Cloud Storage)
   - Implement CDN for faster image delivery
   - Add image optimization/compression
   - Consider using object storage services
"""

import os
import uuid
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile

# Configuration
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes


def ensure_upload_dir() -> None:
    """
    Ensure the upload directory exists.
    Creates the directory if it doesn't exist.
    """
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_file_extension(filename: str) -> str:
    """
    Extract file extension from filename.
    
    Args:
        filename: Original filename
        
    Returns:
        File extension (e.g., '.jpg', '.png')
    """
    return Path(filename).suffix.lower()


def is_allowed_extension(filename: str) -> bool:
    """
    Check if file extension is allowed.
    
    Args:
        filename: Original filename
        
    Returns:
        True if extension is allowed, False otherwise
    """
    ext = get_file_extension(filename)
    return ext in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename using UUID.
    Preserves the original file extension.
    
    Args:
        original_filename: Original filename from upload
        
    Returns:
        Unique filename (e.g., 'a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg')
        
    Example:
        >>> generate_unique_filename("my_photo.jpg")
        'a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg'
    """
    ext = get_file_extension(original_filename)
    unique_id = uuid.uuid4()
    return f"{unique_id}{ext}"


async def save_upload_file(file: UploadFile) -> Tuple[str, str]:
    """
    Save uploaded file to disk with unique filename.
    
    Args:
        file: FastAPI UploadFile object
        
    Returns:
        Tuple of (filename, file_path)
        
    Raises:
        ValueError: If file extension is not allowed
        
    Example:
        >>> filename, path = await save_upload_file(upload_file)
        >>> print(filename)  # 'a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg'
        >>> print(path)      # '/path/to/backend/uploads/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg'
    """
    # Validate file extension
    if not is_allowed_extension(file.filename):
        raise ValueError(
            f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Ensure upload directory exists
    ensure_upload_dir()
    
    # Generate unique filename
    filename = generate_unique_filename(file.filename)
    file_path = UPLOAD_DIR / filename
    
    # Save file to disk
    # Read file in chunks to handle large files efficiently
    with open(file_path, "wb") as buffer:
        while chunk := await file.read(8192):  # Read 8KB at a time
            buffer.write(chunk)
    
    return filename, str(file_path)


def delete_file(filename: str) -> bool:
    """
    Delete a file from the uploads directory.
    
    Args:
        filename: Name of file to delete
        
    Returns:
        True if file was deleted, False if file didn't exist
        
    Example:
        >>> delete_file('a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg')
        True
    """
    file_path = UPLOAD_DIR / filename
    
    if file_path.exists():
        file_path.unlink()
        return True
    
    return False


def get_file_path(filename: str) -> Path:
    """
    Get full path to a file in uploads directory.
    
    Args:
        filename: Name of file
        
    Returns:
        Full path to file
        
    Example:
        >>> path = get_file_path('a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg')
        >>> print(path)  # '/path/to/backend/uploads/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg'
    """
    return UPLOAD_DIR / filename


def file_exists(filename: str) -> bool:
    """
    Check if a file exists in uploads directory.
    
    Args:
        filename: Name of file to check
        
    Returns:
        True if file exists, False otherwise
    """
    return get_file_path(filename).exists()


def generate_file_url(filename: str, base_url: str = "") -> str:
    """
    Generate URL for accessing uploaded file.
    
    Args:
        filename: Name of file
        base_url: Base URL of the API (e.g., 'http://localhost:8000')
        
    Returns:
        Full URL to access the file
        
    Example:
        >>> url = generate_file_url('abc123.jpg', 'http://localhost:8000')
        >>> print(url)  # 'http://localhost:8000/uploads/abc123.jpg'
    """
    return f"{base_url}/uploads/{filename}"
