"""Tests for multi-model chat routing API behaviour."""

from src.api.app import create_app


def test_chat_endpoint_returns_routing_metadata():
    """Chat responses should expose routing and cost metadata."""
    app = create_app("config.yaml")
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post(
            "/chat",
            json={
                "conversation_id": "routing-api-test",
                "message": "Our API is broken and this is urgent.",
                "model_preference": "sumotx",
                "fallback_model": "small",
                "routing_mode": "auto",
            },
        )

        assert response.status_code == 200
        payload = response.get_json()
        assert payload["routing"]["assigned_model"] == "gpt-4"
        assert payload["routing"]["fallback_model"] == "small"
        assert payload["classification"]["intent"] == "bug_report"
        assert payload["estimated_cost_usd"] >= 0
