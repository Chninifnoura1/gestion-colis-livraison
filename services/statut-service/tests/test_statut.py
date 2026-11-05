import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import statut_service

client = TestClient(app)


def new_colis_id() -> str:
    # A brand new parcel id for each test: tests never disturb each other
    return str(uuid.uuid4())


def post_statut(colis_id, libelle, **extra):
    return client.post(
        "/api/v1/statuts/",
        json={"colis_id": colis_id, "libelle": libelle, **extra},
    )


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_statut_ok():
    colis_id = new_colis_id()
    response = post_statut(
        colis_id, "expédié",
        localisation="Casablanca", commentaire="Pris en charge",
    )
    assert response.status_code == 201
    body = response.json()
    assert body["colis_id"] == colis_id
    assert body["libelle"] == "expédié"
    assert body["localisation"] == "Casablanca"


def test_create_statut_libelle_invalide():
    response = post_statut(new_colis_id(), "inconnu")
    assert response.status_code == 422


def test_create_statut_sans_colis_id():
    response = client.post("/api/v1/statuts/", json={"libelle": "livré"})
    assert response.status_code == 422


def test_create_statut_colis_introuvable(monkeypatch):
    monkeypatch.setattr(statut_service, "colis_exists", lambda colis_id: False)
    response = post_statut(new_colis_id(), "livré")
    assert response.status_code == 404


def test_create_statut_service_colis_indisponible(monkeypatch):
    monkeypatch.setattr(statut_service, "colis_exists", lambda colis_id: None)
    response = post_statut(new_colis_id(), "livré")
    assert response.status_code == 503


def test_statut_actuel_est_le_dernier():
    colis_id = new_colis_id()
    post_statut(colis_id, "en préparation")
    post_statut(colis_id, "expédié")
    post_statut(colis_id, "en cours de livraison")

    response = client.get(f"/api/v1/statuts/colis/{colis_id}/actuel")
    assert response.status_code == 200
    assert response.json()["libelle"] == "en cours de livraison"


def test_statut_actuel_colis_sans_statut():
    response = client.get(f"/api/v1/statuts/colis/{new_colis_id()}/actuel")
    assert response.status_code == 404


def test_historique_dans_l_ordre():
    colis_id = new_colis_id()
    etapes = ["en préparation", "expédié", "livré"]
    for etape in etapes:
        post_statut(colis_id, etape)

    response = client.get(f"/api/v1/statuts/colis/{colis_id}/historique")
    assert response.status_code == 200
    assert [s["libelle"] for s in response.json()] == etapes


def test_historique_colis_sans_statut():
    response = client.get(f"/api/v1/statuts/colis/{new_colis_id()}/historique")
    assert response.status_code == 200
    assert response.json() == []


def test_colis_id_invalide():
    response = client.get("/api/v1/statuts/colis/abc/actuel")
    assert response.status_code == 422
