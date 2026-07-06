"""Tests fonctionnels de payment-api (pytest + client de test Flask)."""

import pytest

from app import app, PLAFOND


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_authorize_ok(client):
    resp = client.post("/authorize", json={"amount": 50000})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["authorized"] is True
    assert body["amount"] == 50000


def test_authorize_above_plafond(client):
    resp = client.post("/authorize", json={"amount": PLAFOND + 1})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["authorized"] is False
    assert body["reason"] == "plafond depasse"


def test_authorize_negative_amount(client):
    resp = client.post("/authorize", json={"amount": -10})
    assert resp.status_code == 400


def test_authorize_missing_amount(client):
    resp = client.post("/authorize", json={})
    assert resp.status_code == 400


def test_authorize_amount_at_plafond(client):
    # Le plafond exact doit etre accepte (limite incluse).
    resp = client.post("/authorize", json={"amount": PLAFOND})
    assert resp.status_code == 200
    assert resp.get_json()["authorized"] is True
