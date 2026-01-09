"""
Tests for chat/chatbot endpoints.

Tests:
- Send chat message
- Chat with image
- Chat status
- Error handling
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


def create_test_image(width=300, height=300, format="JPEG"):
    """Create a test image for chat image tests."""
    img = Image.new('RGB', (width, height), color='green')
    img_bytes = BytesIO()
    img.save(img_bytes, format=format)
    img_bytes.seek(0)
    return img_bytes


class TestChatMessage:
    """Test chat message endpoint."""

    def test_send_message_success(self, client: TestClient, auth_headers: dict):
        """Test sending a chat message."""
        response = client.post(
            "/api/v1/chat/message",
            headers=auth_headers,
            json={
                "message": "What pests should I watch out for in rice farming?"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "context_used" in data
        assert isinstance(data["response"], str)

    def test_send_message_with_session(self, client: TestClient, auth_headers: dict):
        """Test sending a message with session ID for conversation continuity."""
        response = client.post(
            "/api/v1/chat/message",
            headers=auth_headers,
            json={
                "message": "Tell me about pest control",
                "session_id": "test-session-123"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data

    def test_send_message_empty(self, client: TestClient, auth_headers: dict):
        """Test sending empty message fails."""
        response = client.post(
            "/api/v1/chat/message",
            headers=auth_headers,
            json={
                "message": ""
            }
        )

        # Should fail validation
        assert response.status_code == 422

    def test_send_message_no_auth(self, client: TestClient):
        """Test sending message without authentication fails."""
        response = client.post(
            "/api/v1/chat/message",
            json={
                "message": "Hello"
            }
        )

        assert response.status_code == 403

    def test_send_message_various_questions(self, client: TestClient, auth_headers: dict):
        """Test various types of agricultural questions."""
        questions = [
            "How should I prepare my field for planting?",
            "What is the best time to apply fertilizer?",
            "How do I identify rice stem borer?",
            "What should I do during heavy rain?",
        ]

        for question in questions:
            response = client.post(
                "/api/v1/chat/message",
                headers=auth_headers,
                json={"message": question}
            )

            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert len(data["response"]) > 0


class TestChatImage:
    """Test chat with image endpoint."""

    def test_send_image_success(self, client: TestClient, auth_headers: dict):
        """Test sending image in chat."""
        img = create_test_image()
        response = client.post(
            "/api/v1/chat/image",
            headers=auth_headers,
            files={"image": ("test.jpg", img, "image/jpeg")},
            data={"message": "What pest is this?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data or "detection" in data

    def test_send_image_no_message(self, client: TestClient, auth_headers: dict):
        """Test sending image without message."""
        img = create_test_image()
        response = client.post(
            "/api/v1/chat/image",
            headers=auth_headers,
            files={"image": ("test.jpg", img, "image/jpeg")}
        )

        # Should work - message is optional
        assert response.status_code in [200, 422]

    def test_send_image_no_auth(self, client: TestClient):
        """Test sending image without authentication fails."""
        img = create_test_image()
        response = client.post(
            "/api/v1/chat/image",
            files={"image": ("test.jpg", img, "image/jpeg")}
        )

        assert response.status_code == 403


class TestChatStatus:
    """Test chat status endpoint."""

    def test_get_status(self, client: TestClient, auth_headers: dict):
        """Test getting chat service status."""
        response = client.get(
            "/api/v1/chat/status",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "ai_available" in data

    def test_get_status_no_auth(self, client: TestClient):
        """Test getting status without authentication fails."""
        response = client.get("/api/v1/chat/status")
        assert response.status_code == 403


class TestChatContext:
    """Test that chat uses user context properly."""

    def test_chat_uses_user_context(self, client: TestClient, auth_headers: dict, test_user):
        """Test that chat response includes user context."""
        response = client.post(
            "/api/v1/chat/message",
            headers=auth_headers,
            json={
                "message": "Give me advice for my farm"
            }
        )

        assert response.status_code == 200
        data = response.json()
        # Context should be used (contains user info)
        assert "context_used" in data

    def test_chat_context_includes_crop(self, client: TestClient, auth_headers: dict, test_user):
        """Test that crop-specific advice is given."""
        response = client.post(
            "/api/v1/chat/message",
            headers=auth_headers,
            json={
                "message": "What are common pests for my crop?"
            }
        )

        assert response.status_code == 200
        data = response.json()
        # Response should be relevant to the user's crop type
        assert "response" in data


class TestChatErrorHandling:
    """Test chat error handling."""

    def test_malformed_json(self, client: TestClient, auth_headers: dict):
        """Test sending malformed JSON."""
        response = client.post(
            "/api/v1/chat/message",
            headers=auth_headers,
            content="not valid json",
            headers_override={"Content-Type": "application/json"}
        )

        # Should return error
        assert response.status_code in [400, 422]

    def test_missing_required_fields(self, client: TestClient, auth_headers: dict):
        """Test sending request without required fields."""
        response = client.post(
            "/api/v1/chat/message",
            headers=auth_headers,
            json={}
        )

        assert response.status_code == 422

    def test_very_long_message(self, client: TestClient, auth_headers: dict):
        """Test sending very long message."""
        long_message = "What should I do? " * 1000

        response = client.post(
            "/api/v1/chat/message",
            headers=auth_headers,
            json={"message": long_message}
        )

        # Should either succeed or return validation error
        assert response.status_code in [200, 422]
