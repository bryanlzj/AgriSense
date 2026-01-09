"""
Chat Router

API endpoints for the AgriSense chatbot assistant.
Provides agricultural Q&A with context-aware responses.

Learning Notes:
- Chat uses AI service (OpenRouter) for responses
- Context automatically injected (crop type, location, weather)
- Image messages route to pest detection guidance
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from dependencies.auth import get_current_user
from schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatImageRequest,
    ChatImageResponse,
    ChatContextUsed
)
from services.chat_service import (
    process_chat_message,
    process_image_chat,
    get_quick_response
)
from services.ai_service import is_ai_available

router = APIRouter(prefix="/chat", tags=["Chatbot 💬"])


@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    request: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the AgriSense chatbot.

    **Chatbot Feature** 💬

    The chatbot provides agricultural advice tailored to your farm:
    - Answers questions about farming, pests, and weather
    - Uses your crop type and location for relevant advice
    - Includes current weather conditions in context

    **Context Automatically Included:**
    - Your crop type (rice, vegetables, etc.)
    - Your farm location
    - Current weather conditions (if include_weather=true)

    **Session Support:**
    - Pass `session_id` to maintain conversation context
    - Previous messages are remembered within session

    **Example Questions:**
    - "What pests should I watch for in this weather?"
    - "When is the best time to irrigate my rice field?"
    - "How do I prevent fungal diseases?"

    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/chat/message" \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{"message": "What pests should I watch for?"}'
    ```
    """
    # Check for quick response patterns
    quick_response = get_quick_response(request.message)
    if quick_response:
        return ChatMessageResponse(
            message=quick_response,
            session_id=request.session_id,
            context_used=ChatContextUsed(
                crop_type=current_user.crop_type,
                location=current_user.farm_location_name,
                weather_available=False,
                weather_summary=None
            ),
            ai_available=is_ai_available(),
            timestamp=__import__("datetime").datetime.utcnow().isoformat()
        )

    # Process message through AI service
    response = await process_chat_message(
        message=request.message,
        user=current_user,
        session_id=request.session_id,
        include_weather=request.include_weather
    )

    return ChatMessageResponse(
        message=response["message"],
        session_id=response.get("session_id"),
        context_used=ChatContextUsed(
            crop_type=response["context_used"]["crop_type"],
            location=response["context_used"]["location"],
            weather_available=response["context_used"]["weather_available"],
            weather_summary=response["context_used"].get("weather_summary")
        ),
        ai_available=response["ai_available"],
        timestamp=response["timestamp"]
    )


@router.post("/image", response_model=ChatImageResponse)
async def send_image_message(
    request: ChatImageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send an image to the chatbot for pest identification guidance.

    **Image Chat Feature** 📸

    When you send an image through chat, the system:
    1. Receives the image reference
    2. Provides guidance on pest detection
    3. Suggests using the full detection feature

    **Note:** For full pest detection with ML analysis, use:
    - `POST /api/v1/pest/detect/enhanced` endpoint
    - This chat endpoint provides guidance only

    **Request Body:**
    - `image_url`: Path to the uploaded image
    - `message`: Optional description of what you're seeing

    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/chat/image" \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{
        "image_url": "/uploads/pest_images/abc123.jpg",
        "message": "What is this bug on my rice?"
      }'
    ```
    """
    response = await process_image_chat(
        image_url=request.image_url,
        message=request.message,
        user=current_user,
        db=db
    )

    return ChatImageResponse(
        message=response["message"],
        action_suggested=response["action_suggested"],
        pest_detection_url=response["pest_detection_url"],
        image_url=response["image_url"],
        context_used=response["context_used"],
        timestamp=response["timestamp"]
    )


@router.get("/status")
async def get_chat_status(
    current_user: User = Depends(get_current_user)
):
    """
    Check chatbot service status.

    Returns whether AI service is available and user context.

    **Example:**
    ```bash
    curl "http://localhost:8000/api/v1/chat/status" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    return {
        "status": "available",
        "ai_service_available": is_ai_available(),
        "user_context": {
            "crop_type": current_user.crop_type,
            "location": current_user.farm_location_name,
            "username": current_user.username
        },
        "capabilities": [
            "Agricultural Q&A",
            "Weather-aware advice",
            "Pest management guidance",
            "Crop-specific recommendations"
        ]
    }


# ============================================================================
# LEARNING NOTES: Chat Endpoints
# ============================================================================

"""
1. Chat Message Flow:
   - User sends message via POST /chat/message
   - Service builds context (crop, location, weather)
   - AI service generates response with context
   - Response returned with context_used info

2. Image Message Flow:
   - User sends image via POST /chat/image
   - System acknowledges receipt
   - Guides user to pest detection feature
   - Returns known pests for crop type

3. Context Injection:
   - Automatic: crop_type, location from user profile
   - Optional: weather (if include_weather=true)
   - AI receives context in system prompt

4. Session Management:
   - session_id allows conversation continuity
   - History managed by client (pass previous messages)
   - Currently stateless (no server-side session storage)

5. Quick Responses:
   - Common queries handled without AI
   - Reduces latency and API costs
   - Pattern matching for known queries
"""
