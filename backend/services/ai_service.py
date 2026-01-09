"""
AI Service for generating recommendations via OpenRouter API.

This module provides functions to:
- Generate pest control recommendations when pests are detected
- Generate weather-related farming recommendations
- Provide best-guess analysis for unidentified pest reports
- Generate context-aware chatbot responses

Learning Notes:
- Uses httpx for async HTTP requests to OpenRouter API
- OpenRouter provides access to various LLMs (we use Llama 3.1 8B free tier)
- All AI calls include agricultural context (location, crop type, weather)
- Mock mode available when API key not configured
"""

import httpx
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from config import settings

# ============================================================================
# CONFIGURATION
# ============================================================================

# OpenRouter API configuration
OPENROUTER_API_KEY = settings.openrouter_api_key
OPENROUTER_BASE_URL = settings.openrouter_base_url

# Model to use (free tier model)
# Using Llama 3.1 8B Instruct - free and good for agricultural advice
DEFAULT_MODEL = "meta-llama/llama-3.1-8b-instruct:free"

# API timeout (seconds)
API_TIMEOUT = 30

# Logger
logger = logging.getLogger(__name__)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _is_api_configured() -> bool:
    """Check if OpenRouter API is properly configured."""
    return bool(OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your_openrouter_api_key_here")


def _build_headers() -> Dict[str, str]:
    """Build HTTP headers for OpenRouter API requests."""
    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://agrisense.local",  # Required by OpenRouter
        "X-Title": "AgriSense Agricultural Assistant"
    }


def _build_system_prompt(
    crop_type: str,
    location: Optional[str] = None,
    weather_context: Optional[str] = None
) -> str:
    """
    Build system prompt with agricultural context.

    Args:
        crop_type: User's primary crop (rice, vegetables, etc.)
        location: Farm location (Malaysian state/region)
        weather_context: Current weather conditions summary

    Returns:
        str: System prompt with context
    """
    context_parts = [
        "You are an agricultural expert assistant for Malaysian farmers.",
        f"The farmer grows {crop_type} crops.",
    ]

    if location:
        context_parts.append(f"Their farm is located in {location}, Malaysia.")

    if weather_context:
        context_parts.append(f"Current weather conditions: {weather_context}")

    context_parts.extend([
        "",
        "Guidelines:",
        "- Provide practical, actionable advice suitable for small to medium farms",
        "- Consider Malaysian tropical climate and local agricultural practices",
        "- Recommend organic/IPM solutions when possible",
        "- Be concise but thorough",
        "- If uncertain, advise consulting local agricultural extension officers",
    ])

    return "\n".join(context_parts)


# ============================================================================
# MOCK RESPONSES (Used when API not configured)
# ============================================================================

def _get_mock_pest_recommendations(
    pest_name: str,
    confidence: float,
    crop_type: str
) -> Dict[str, Any]:
    """Generate mock pest recommendations for testing."""

    recommendations = {
        "Rice Stem Borer": [
            "Apply biological control using Trichogramma wasps",
            "Remove and destroy infected stems",
            "Maintain proper water levels (3-5cm)",
            "Plant early to avoid peak pest season"
        ],
        "Brown Planthopper": [
            "Avoid excessive nitrogen fertilizer",
            "Maintain field sanitation",
            "Use resistant rice varieties (e.g., IR64)",
            "Apply neem-based pesticides if severe"
        ],
        "Rice Blast": [
            "Apply fungicide (tricyclazole) preventively",
            "Avoid excessive nitrogen application",
            "Ensure proper drainage",
            "Use resistant varieties"
        ]
    }

    default_recommendations = [
        "Monitor the affected area closely for changes",
        "Remove heavily infested plant parts",
        "Consider applying neem oil as organic treatment",
        "Consult local agricultural extension office for specific advice"
    ]

    return {
        "pest_name": pest_name,
        "confidence": confidence,
        "severity_assessment": "moderate" if confidence < 0.85 else "high",
        "recommendations": recommendations.get(pest_name, default_recommendations),
        "immediate_actions": [
            "Isolate affected plants if possible",
            "Document damage with photos for records"
        ],
        "prevention_tips": [
            "Maintain field hygiene",
            "Practice crop rotation",
            "Regular monitoring and early detection"
        ],
        "when_to_seek_help": "If infestation spreads to more than 20% of crop area or damage increases rapidly"
    }


def _get_mock_weather_recommendations(
    alert_type: str,
    conditions: Dict[str, Any],
    crop_type: str
) -> Dict[str, Any]:
    """Generate mock weather recommendations for testing."""

    recommendations_map = {
        "heavy_rain": {
            "immediate_actions": [
                "Check and clear drainage channels",
                "Delay any scheduled irrigation",
                "Move harvested crops to covered storage"
            ],
            "crop_protection": [
                "Apply preventive fungicide after rain stops",
                "Monitor for waterlogging signs",
                "Check for pest emergence (snails, slugs)"
            ],
            "long_term": [
                "Improve field drainage systems",
                "Consider raised beds for future planting"
            ]
        },
        "high_temperature": {
            "immediate_actions": [
                "Increase irrigation frequency",
                "Apply mulch to retain soil moisture",
                "Water during early morning or late evening"
            ],
            "crop_protection": [
                "Use shade cloth for sensitive crops",
                "Monitor for heat stress symptoms",
                "Avoid transplanting during peak heat"
            ],
            "long_term": [
                "Plant heat-tolerant varieties",
                "Improve irrigation systems"
            ]
        },
        "strong_wind": {
            "immediate_actions": [
                "Secure loose structures and equipment",
                "Delay pesticide spraying",
                "Check support stakes for tall crops"
            ],
            "crop_protection": [
                "Install windbreaks if possible",
                "Avoid harvesting during high winds"
            ],
            "long_term": [
                "Plant windbreak hedges",
                "Use sturdier crop varieties"
            ]
        }
    }

    default = {
        "immediate_actions": ["Monitor conditions closely", "Prepare for weather changes"],
        "crop_protection": ["Protect sensitive crops", "Ensure proper drainage"],
        "long_term": ["Maintain regular monitoring schedule"]
    }

    return recommendations_map.get(alert_type, default)


def _get_mock_report_analysis(
    description: Optional[str],
    severity: str,
    crop_type: str
) -> Dict[str, Any]:
    """Generate mock analysis for unidentified pest reports."""

    # Generic best-guess based on description keywords
    possible_pests = []
    if description:
        desc_lower = description.lower()
        if "green" in desc_lower and "leaf" in desc_lower:
            possible_pests = ["Green Leafhopper", "Rice Aphids"]
        elif "brown" in desc_lower or "stem" in desc_lower:
            possible_pests = ["Rice Stem Borer", "Brown Planthopper"]
        elif "white" in desc_lower or "fungus" in desc_lower:
            possible_pests = ["Rice Blast (fungal)", "Sheath Blight"]
        elif "hole" in desc_lower:
            possible_pests = ["Rice Leaf Folder", "Rice Stem Borer"]

    if not possible_pests:
        possible_pests = ["Unable to identify - recommend expert consultation"]

    return {
        "possible_identification": f"Based on description, this could be: {', '.join(possible_pests)}",
        "general_advice": [
            "Monitor the affected area daily for changes",
            "Remove heavily infested leaves/plants carefully",
            "Consider applying neem oil spray as organic treatment",
            "Maintain proper field drainage",
            "Consult local agricultural extension office for confirmation"
        ],
        "when_to_seek_help": f"If infestation spreads beyond current area or damage becomes {severity}"
    }


# ============================================================================
# OPENROUTER API CALLS
# ============================================================================

async def _call_openrouter(
    messages: List[Dict[str, str]],
    model: str = DEFAULT_MODEL,
    max_tokens: int = 1000
) -> Optional[str]:
    """
    Make async call to OpenRouter API.

    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model ID to use
        max_tokens: Maximum tokens in response

    Returns:
        str: AI response text, or None if failed
    """
    if not _is_api_configured():
        logger.warning("OpenRouter API not configured, using mock responses")
        return None

    url = f"{OPENROUTER_BASE_URL}/chat/completions"

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            response = await client.post(
                url,
                headers=_build_headers(),
                json=payload
            )

            if response.status_code == 429:
                logger.warning("OpenRouter rate limit reached, using mock response")
                return None

            response.raise_for_status()

            data = response.json()

            # Extract response text
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]

            logger.error(f"Unexpected API response format: {data}")
            return None

    except httpx.TimeoutException:
        logger.error("OpenRouter API request timed out")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenRouter API error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"OpenRouter API unexpected error: {str(e)}")
        return None


def _parse_json_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Parse JSON from AI response text.
    Handles cases where AI wraps JSON in markdown code blocks.

    Args:
        response_text: Raw AI response

    Returns:
        dict: Parsed JSON, or None if parsing fails
    """
    if not response_text:
        return None

    # Try direct JSON parse
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code block
    if "```json" in response_text:
        try:
            start = response_text.index("```json") + 7
            end = response_text.index("```", start)
            json_str = response_text[start:end].strip()
            return json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            pass

    # Try extracting from generic code block
    if "```" in response_text:
        try:
            start = response_text.index("```") + 3
            # Skip potential language identifier
            if response_text[start:start+1] != "\n":
                start = response_text.index("\n", start) + 1
            end = response_text.index("```", start)
            json_str = response_text[start:end].strip()
            return json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            pass

    return None


# ============================================================================
# PUBLIC API FUNCTIONS
# ============================================================================

async def get_pest_recommendations(
    pest_name: str,
    confidence: float,
    crop_type: str,
    weather_context: Optional[str] = None,
    location: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get AI-generated recommendations for detected pest.

    Called when pest detection confidence >= 70%.

    Args:
        pest_name: Detected pest name
        confidence: Detection confidence (0.0 - 1.0)
        crop_type: User's crop type
        weather_context: Current weather conditions
        location: Farm location

    Returns:
        dict: Recommendations including:
            - pest_name: Confirmed pest name
            - confidence: Detection confidence
            - severity_assessment: low/moderate/high
            - recommendations: List of treatment recommendations
            - immediate_actions: Urgent steps to take
            - prevention_tips: Future prevention advice
            - when_to_seek_help: When to consult experts
    """
    system_prompt = _build_system_prompt(crop_type, location, weather_context)

    user_prompt = f"""A pest has been detected on the farm with the following details:
- Pest: {pest_name}
- Detection confidence: {confidence * 100:.1f}%
- Crop affected: {crop_type}

Please provide treatment recommendations in the following JSON format:
{{
    "pest_name": "{pest_name}",
    "confidence": {confidence},
    "severity_assessment": "low/moderate/high based on typical damage",
    "recommendations": ["list of 3-5 specific treatment recommendations"],
    "immediate_actions": ["list of 2-3 urgent steps to take now"],
    "prevention_tips": ["list of 2-3 future prevention measures"],
    "when_to_seek_help": "guidance on when to consult experts"
}}

Provide practical advice suitable for Malaysian smallholder farmers."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = await _call_openrouter(messages)

    if response:
        parsed = _parse_json_response(response)
        if parsed:
            return parsed

    # Fall back to mock response
    logger.info(f"Using mock recommendations for pest: {pest_name}")
    return _get_mock_pest_recommendations(pest_name, confidence, crop_type)


async def get_weather_recommendations(
    alert_type: str,
    conditions: Dict[str, Any],
    crop_type: str,
    location: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get AI-generated recommendations for weather conditions.

    Called when weather alerts are generated.

    Args:
        alert_type: Type of weather alert (heavy_rain, high_temperature, etc.)
        conditions: Current weather conditions dict
        crop_type: User's crop type
        location: Farm location

    Returns:
        dict: Recommendations including:
            - immediate_actions: Urgent steps to take
            - crop_protection: How to protect crops
            - long_term: Future preparedness advice
    """
    system_prompt = _build_system_prompt(crop_type, location)

    conditions_str = ", ".join([f"{k}: {v}" for k, v in conditions.items()])

    user_prompt = f"""Weather alert for the farm:
- Alert type: {alert_type}
- Current conditions: {conditions_str}
- Crop: {crop_type}

Please provide farming recommendations in the following JSON format:
{{
    "immediate_actions": ["list of 2-3 urgent steps to take now"],
    "crop_protection": ["list of 2-3 ways to protect crops"],
    "long_term": ["list of 1-2 future preparedness measures"]
}}

Provide practical advice suitable for Malaysian smallholder farmers."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = await _call_openrouter(messages)

    if response:
        parsed = _parse_json_response(response)
        if parsed:
            return parsed

    # Fall back to mock response
    logger.info(f"Using mock recommendations for alert: {alert_type}")
    return _get_mock_weather_recommendations(alert_type, conditions, crop_type)


async def get_pest_report_analysis(
    description: Optional[str],
    observed_severity: str,
    crop_type: str,
    location: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get AI-generated best-guess analysis for unidentified pest.

    Called when user submits manual pest report after failed detection.

    Args:
        description: User's description of what they observed
        observed_severity: User's severity assessment (minor, moderate, severe)
        crop_type: User's crop type
        location: Farm location

    Returns:
        dict: Analysis including:
            - possible_identification: Best guess based on description
            - general_advice: List of general recommendations
            - when_to_seek_help: When to consult experts
    """
    system_prompt = _build_system_prompt(crop_type, location)

    user_prompt = f"""A farmer has reported an unidentified pest/disease with the following details:
- Description: {description or "No description provided"}
- Observed severity: {observed_severity}
- Crop: {crop_type}
- Location: {location or "Malaysia"}

The automated detection system could not identify the pest. Please provide your best-guess analysis in the following JSON format:
{{
    "possible_identification": "Your best guess of what this could be based on the description",
    "general_advice": ["list of 4-5 general pest management recommendations"],
    "when_to_seek_help": "guidance on when to consult agricultural experts"
}}

Be helpful but cautious - clearly indicate this is a best guess and recommend expert confirmation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = await _call_openrouter(messages)

    if response:
        parsed = _parse_json_response(response)
        if parsed:
            return parsed

    # Fall back to mock response
    logger.info("Using mock analysis for pest report")
    return _get_mock_report_analysis(description, observed_severity, crop_type)


async def get_chatbot_response(
    user_message: str,
    crop_type: str,
    location: Optional[str] = None,
    weather_context: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Get AI-generated chatbot response.

    For general agricultural Q&A.

    Args:
        user_message: User's question/message
        crop_type: User's crop type
        location: Farm location
        weather_context: Current weather summary
        conversation_history: Previous messages in conversation

    Returns:
        str: AI response text
    """
    system_prompt = _build_system_prompt(crop_type, location, weather_context)

    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history[-10:])  # Keep last 10 messages

    messages.append({"role": "user", "content": user_message})

    response = await _call_openrouter(messages, max_tokens=500)

    if response:
        return response

    # Fall back to generic response
    return (
        "I'm sorry, I couldn't process your request at this time. "
        "For agricultural advice, please consult your local agricultural extension office "
        f"or try asking specific questions about {crop_type} farming in Malaysia."
    )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_ai_available() -> bool:
    """Check if AI service is available (API configured)."""
    return _is_api_configured()


async def test_ai_connection() -> Dict[str, Any]:
    """
    Test connection to OpenRouter API.

    Returns:
        dict: Status and details of connection test
    """
    if not _is_api_configured():
        return {
            "status": "not_configured",
            "message": "OpenRouter API key not configured",
            "using_mock": True
        }

    try:
        messages = [
            {"role": "user", "content": "Hello, respond with 'OK' if you can read this."}
        ]

        response = await _call_openrouter(messages, max_tokens=10)

        if response:
            return {
                "status": "connected",
                "message": "OpenRouter API is working",
                "using_mock": False,
                "model": DEFAULT_MODEL
            }
        else:
            return {
                "status": "error",
                "message": "Failed to get response from OpenRouter",
                "using_mock": True
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "using_mock": True
        }


# ============================================================================
# LEARNING NOTES: AI Service Integration
# ============================================================================

"""
1. OpenRouter API:
   - Provides access to various LLMs through single API
   - We use free tier model (Llama 3.1 8B)
   - Requires API key and proper headers
   - Rate limits apply (handle gracefully with fallbacks)

2. Prompt Engineering:
   - System prompt sets context (crop type, location, weather)
   - User prompts request specific JSON format
   - Temperature 0.7 balances creativity and consistency

3. Response Handling:
   - AI may return JSON directly or in markdown code blocks
   - Parser handles both cases
   - Always have mock fallback for when API fails

4. When AI is Called:
   - Pest detection (≥70% confidence): Get treatment recommendations
   - Weather alerts: Get farming recommendations
   - Pest reports: Get best-guess analysis
   - Chatbot: General Q&A

5. When AI is NOT Called:
   - Pest risk predictions: Use stored prevention_tips from database
   - This saves API costs and ensures consistent advice

6. Error Handling:
   - Timeout: Fall back to mock
   - Rate limit (429): Fall back to mock
   - Parse error: Fall back to mock
   - Always provide useful response to user

7. Security:
   - API key stored in environment variable
   - Never expose API key in responses
   - Validate all AI outputs before using
"""
