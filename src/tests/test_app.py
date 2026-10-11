from app import app


def test_home_page_loads():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Greenhill Food Co-op" in response.data


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert data["application"] == "Greenhill Food Co-op"


def test_closed_round_message_displays(monkeypatch):
    from app import app

    monkeypatch.setattr(
        "app.get_available_products",
        lambda products, current_round, is_open: "No open round"
    )

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"No open round" in response.data
    
def test_historical_order_displays_original_price():
    client = app.test_client()
    response = client.get("/history")

    assert response.status_code == 200
    assert b"Historical Order" in response.data
    assert b"Original Price: $3.40" in response.data
    assert b"Order Total: $6.80" in response.data

