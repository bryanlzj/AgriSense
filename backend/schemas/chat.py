"""
Chat Schemas

Pydantic models for chatbot API requests and responses.
Used for the AgriSense agricultural assistant chatbot.

Learning Notes:
- Chat messages include optional session tracking
- Context is automatically injected (crop, location, weather)
- Image messages route to pest detection
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    """
    Request schema for sending a chat message.
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's message to the chatbot"
    )
    session_id: Optional[str] = Field(
        None,
        description="Optional session ID for conversation continuity"
    )
    include_weather: bool = Field(
        True,
        description="Whether to include current weather in context"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What pests should I watch out for in this weather?",
                "session_id": "abc123",
                "include_weather": True
            }
        }


class ChatContextUsed(BaseModel):
    """
    Context that was used to generate the response.
    """
    crop_type: str = Field(..., description="User's crop type")
    location: str = Field(..., description="User's farm location")
    weather_available: bool = Field(..., description="Whether weather data was available")
    weather_summary: Optional[str] = Field(None, description="Weather conditions summary")

    class Config:
        json_schema_extra = {
            "example": {
                "crop_type": "rice",
                "location": "Kedah",
                "weather_available": True,
                "weather_summary": "Temperature: 28.5°C, Humidity: 85%, Conditions: scattered clouds"
            }
        }


class ChatMessageResponse(BaseModel):
    """
    Response schema for chat message.
    """
    message: str = Field(..., description="AI response message")
    session_id: Optional[str] = Field(None, description="Session ID for continuity")
    context_used: ChatContextUsed = Field(..., description="Context used for response")
    ai_available: bool = Field(..., description="Whether AI service was available")
    timestamp: str = Field(..., description="Response timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Based on the current weather conditions (28°C, 85% humidity), you should watch out for Brown Planthopper...",
                "session_id": "abc123",
                "context_used": {
                    "crop_type": "rice",
                    "location": "Kedah",
                    "weather_available": True,
                    "weather_summary": "Temperature: 28.5°C, Humidity: 85%"
                },
                "ai_available": True,
                "timestamp": "2025-01-09T10:30:00"
            }
        }


class ChatImageRequest(BaseModel):
    """
    Request schema for sending an image message.
    """
    image_url: str = Field(
        ...,
        description="URL/path to the uploaded image"
    )
    message: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional message accompanying the image"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "/uploads/pest_images/abc123.jpg",
                "message": "What is this insect on my rice plant?"
            }
        }


class ChatImageResponse(BaseModel):
    """
    Response schema for image chat message.
    """
    message: str = Field(..., description="Response message about the image")
    action_suggested: str = Field(..., description="Suggested action to take")
    pest_detection_url: str = Field(..., description="URL for pest detection endpoint")
    image_url: str = Field(..., description="Image URL that was processed")
    context_used: Dict[str, Any] = Field(..., description="Context used")
    timestamp: str = Field(..., description="Response timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "I've received your image. To analyze it for pests...",
                "action_suggested": "use_pest_detection",
                "pest_detection_url": "/api/v1/pest/detect/enhanced",
                "image_url": "/uploads/pest_images/abc123.jpg",
                "context_used": {
                    "crop_type": "rice",
                    "known_pests": ["Rice Stem Borer", "Brown Planthopper"]
                },
                "timestamp": "2025-01-09T10:30:00"
            }
        }


class ChatHistoryItem(BaseModel):
    """
    Single item in chat history.
    """
    role: str = Field(..., description="Role: user or assistant")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="Message timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "What should I do about high humidity?",
                "timestamp": "2025-01-09T10:30:00"
            }
        }


class ChatSession(BaseModel):
    """
    Chat session with history.
    """
    session_id: str = Field(..., description="Session identifier")
    user_id: int = Field(..., description="User ID")
    messages: List[ChatHistoryItem] = Field(default_factory=list, description="Message history")
    created_at: str = Field(..., description="Session creation time")
    last_activity: str = Field(..., description="Last activity time")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "abc123",
                "user_id": 1,
                "messages": [
                    {"role": "user", "content": "Hello", "timestamp": "2025-01-09T10:30:00"},
                    {"role": "assistant", "content": "Hi! How can I help?", "timestamp": "2025-01-09T10:30:01"}
                ],
                "created_at": "2025-01-09T10:30:00",
                "last_activity": "2025-01-09T10:30:01"
            }
        }
