"""
Chat Service

This service handles chatbot functionality for the AgriSense assistant.
It builds context from user profile and current conditions, then uses
the AI service to generate helpful responses.

Learning Notes:
- Context injection: User's farm info is added to AI system prompt
- Weather context: Current conditions included for relevant advice
- Session support: Optional session_id for conversation continuity
- Image routing: Image messages route to pest detection flow
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from services.ai_service import get_chatbot_response, is_ai_available
from models.user import User

# Logger
logger = logging.getLogger(__name__)


# ============================================================================
# CONTEXT BUILDING
# ============================================================================

async def build_weather_context(
    latitude: float,
    longitude: float
) -> Optional[str]:
    """
    Build weather context string for chatbot.

    Args:
        latitude: Farm latitude
        longitude: Farm longitude

    Returns:
        str: Weather context or None if fetch fails
    """
    from services.weather_service import fetch_current_weather, transform_current_weather

    try:
        weather_data = await fetch_current_weather(latitude, longitude)
        current = transform_current_weather(weather_data)

        return (
            f"Temperature: {current.temperature:.1f}°C, "
            f"Humidity: {current.humidity}%, "
            f"Conditions: {current.weather_description}"
        )
    except Exception as e:
        logger.warning(f"Failed to fetch weather for chat context: {e}")
        return None


def build_user_context(user: User) -> Dict[str, Any]:
    """
    Build user context dictionary for chatbot.

    Args:
        user: User model instance

    Returns:
        dict: User context for prompt building
    """
    return {
        "crop_type": user.crop_type,
        "location_name": user.farm_location_name,
        "latitude": user.farm_location_lat,
        "longitude": user.farm_location_lng,
        "username": user.username
    }


# ============================================================================
# CHAT FUNCTIONS
# ============================================================================

async def process_chat_message(
    message: str,
    user: User,
    session_id: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    include_weather: bool = True
) -> Dict[str, Any]:
    """
    Process a chat message and return AI response.

    Args:
        message: User's message
        user: User model instance
        session_id: Optional session identifier
        conversation_history: Previous messages in session
        include_weather: Whether to include weather context

    Returns:
        dict: Response with AI message and context used
    """
    # Build context
    user_context = build_user_context(user)

    # Optionally get weather context
    weather_context = None
    if include_weather:
        weather_context = await build_weather_context(
            user_context["latitude"],
            user_context["longitude"]
        )

    # Get AI response
    response = await get_chatbot_response(
        user_message=message,
        crop_type=user_context["crop_type"],
        location=user_context["location_name"],
        weather_context=weather_context,
        conversation_history=conversation_history
    )

    return {
        "message": response,
        "session_id": session_id,
        "context_used": {
            "crop_type": user_context["crop_type"],
            "location": user_context["location_name"],
            "weather_available": weather_context is not None,
            "weather_summary": weather_context
        },
        "ai_available": is_ai_available(),
        "timestamp": datetime.utcnow().isoformat()
    }


async def process_image_chat(
    image_url: str,
    message: Optional[str],
    user: User,
    db: Session
) -> Dict[str, Any]:
    """
    Process an image chat message by routing to pest detection.

    When user sends an image through chat, we run pest detection
    and return the results in a chat-friendly format.

    Args:
        image_url: URL/path to uploaded image
        message: Optional message accompanying image
        user: User model instance
        db: Database session

    Returns:
        dict: Detection results formatted for chat
    """
    from services.pest_risk_service import get_correlations_for_crop

    # Note: In production, this would call the actual ML service
    # For now, we return a helpful message about the image

    # Get pest correlations for context
    correlations = get_correlations_for_crop(db, user.crop_type)
    known_pests = [c.pest_name for c in correlations]

    response_message = (
        f"I've received your image. To analyze it for pests, please use the "
        f"'Upload & Detect' feature in the Pest Detection section.\n\n"
        f"Based on your crop type ({user.crop_type}), common pests to watch for include: "
        f"{', '.join(known_pests[:5])}.\n\n"
    )

    if message:
        response_message += f"Regarding your note '{message}' - "
        response_message += "please provide more details and I'll try to help!"

    return {
        "message": response_message,
        "action_suggested": "use_pest_detection",
        "pest_detection_url": "/api/v1/pest/detect/enhanced",
        "image_url": image_url,
        "context_used": {
            "crop_type": user.crop_type,
            "known_pests": known_pests[:5]
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# QUICK RESPONSES
# ============================================================================

# Pre-defined responses for common queries
QUICK_RESPONSES = {
    "help": (
        "I'm your AgriSense assistant! I can help with:\n\n"
        "🌦️ **Weather** - Current conditions and forecasts\n"
        "🐛 **Pest Detection** - Upload images to identify pests\n"
        "⚠️ **Risk Alerts** - Weather and pest risk warnings\n"
        "🌾 **Farming Tips** - Advice based on your crop and conditions\n\n"
        "Just ask me anything about farming in your area!"
    ),
    "weather": (
        "To check the weather, you can:\n\n"
        "1. Use the Weather section in the app\n"
        "2. Ask me 'What's the weather like?'\n"
        "3. Check the dashboard for weather summary\n\n"
        "I'll provide advice based on current conditions!"
    ),
    "pest": (
        "To identify pests, you can:\n\n"
        "1. Use the Pest Detection feature to upload an image\n"
        "2. Check the Pest Risk section for current risk levels\n"
        "3. Ask me about specific pests\n\n"
        "I'll help you identify and manage pests!"
    )
}


def get_quick_response(message: str) -> Optional[str]:
    """
    Check if message matches a quick response pattern.

    Args:
        message: User's message (lowercase)

    Returns:
        str: Quick response if matched, None otherwise
    """
    message_lower = message.lower().strip()

    if "help" in message_lower or message_lower == "?":
        return QUICK_RESPONSES["help"]

    if any(word in message_lower for word in ["weather", "forecast", "rain", "temperature"]):
        return None  # Let AI handle with context

    if any(word in message_lower for word in ["pest", "insect", "bug", "detect"]):
        return None  # Let AI handle with context

    return None


# ============================================================================
# LEARNING NOTES: Chat Service
# ============================================================================

"""
1. How the Chatbot Works:
   - User sends message through /chat/message endpoint
   - Service builds context (user profile, weather)
   - Context injected into AI system prompt
   - AI generates contextual response

2. Context Injection:
   - Crop type: AI gives crop-specific advice
   - Location: Regional pest/weather considerations
   - Weather: Real-time conditions for relevant tips

3. Image Handling:
   - Images sent via /chat/image route to detection
   - Detection results formatted for chat display
   - User guided to full detection feature

4. Session Management:
   - session_id tracks conversation continuity
   - conversation_history maintains context
   - Limited to last 10 messages to manage tokens

5. Quick Responses:
   - Common queries handled without AI call
   - Reduces API costs
   - Instant response for known patterns

6. Integration Points:
   - AI Service: get_chatbot_response()
   - Weather Service: Current conditions
   - Pest Detection: Image analysis routing
"""
