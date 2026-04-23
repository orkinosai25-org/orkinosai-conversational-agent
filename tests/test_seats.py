"""Tests for chatbot seat API endpoints."""

from src.api.app import create_app, seats_db, training_data_db, documents_db


def _create_seat(client, site_domain: str):
    response = client.post("/seats", json={"site_domain": site_domain})
    assert response.status_code == 201
    return response.get_json()["seat"]["id"]


def test_create_chatbot_seat():
    """A seat can be created with core seat fields."""
    app = create_app("config.yaml")
    app.config["TESTING"] = True

    with app.test_client() as client:
        seats_db.clear()

        response = client.post(
            "/seats",
            json={
                "site_domain": "https://example.com",
                "bot_name": "Example Bot",
                "greeting": "Welcome to Example"
            }
        )

        assert response.status_code == 201
        payload = response.get_json()
        seat = payload["seat"]
        assert payload["message"] == "Chatbot Seat created successfully"
        assert seat["site_domain"] == "example.com"
        assert seat["bot_name"] == "Example Bot"
        assert seat["greeting"] == "Welcome to Example"
        assert seat["trained_sources"] == {"urls": [], "documents": []}


def test_training_url_is_isolated_per_seat():
    """Training URLs are tracked per seat."""
    app = create_app("config.yaml")
    app.config["TESTING"] = True

    with app.test_client() as client:
        seats_db.clear()
        training_data_db.clear()

        seat_a = _create_seat(client, "alpha.example.com")
        seat_b = _create_seat(client, "beta.example.com")

        response_a = client.post("/training/url", json={"url": "https://alpha.example.com/help", "seat_id": seat_a})
        response_b = client.post("/training/url", json={"url": "https://beta.example.com/docs", "seat_id": seat_b})
        assert response_a.status_code == 200
        assert response_b.status_code == 200

        seat_a_payload = client.get(f"/seats/{seat_a}").get_json()["seat"]
        seat_b_payload = client.get(f"/seats/{seat_b}").get_json()["seat"]

        assert seat_a_payload["trained_sources"]["urls"] == [
            {"training_id": response_a.get_json()["training_id"], "source": "https://alpha.example.com/help"}
        ]
        assert seat_b_payload["trained_sources"]["urls"] == [
            {"training_id": response_b.get_json()["training_id"], "source": "https://beta.example.com/docs"}
        ]


def test_training_rejects_unknown_seat():
    """Training request fails for unknown seat_id."""
    app = create_app("config.yaml")
    app.config["TESTING"] = True

    with app.test_client() as client:
        seats_db.clear()
        documents_db.clear()

        response = client.post("/training/url", json={"url": "https://example.com", "seat_id": "missing-seat"})
        assert response.status_code == 404
        assert response.get_json()["error"] == "Seat not found"
