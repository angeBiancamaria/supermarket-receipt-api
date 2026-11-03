from fastapi.testclient import TestClient

from supermarket_receipt_api.main import app

client = TestClient(app)


def test_panier_accepte():
    # Le client commande 2 briques de lait
    panier = {
        "items": [
            {"product_id": "milk", "quantity": 2}
        ]
    }

    response = client.post("/checkout", json=panier)

    # Vérifier que la requête est acceptée
    assert response.status_code == 200

    # Vérifier le ticket reçu
    ticket = response.json()

    assert ticket == {
        "lines": [
            {
                "product_id": "milk",
                "name": "Brique de lait",
                "quantity": 2,
                "unit": "piece",
                "unit_price_cents": 100,
                "subtotal_cents": 200,
                "discount_cents": 0,
                "total_cents": 200,
            }
        ],
        "subtotal_cents": 200,
        "discount_cents": 0,
        "total_cents": 200,
    }


def test_requete_refusee():
    # Le client commande une quantité invalide
    panier = {
        "items": [
            {"product_id": "milk", "quantity": 2.5}  # Quantité invalide (non entière)
        ]
    }

    response = client.post("/checkout", json=panier)

    # Vérifier que l'API refuse la requête
    assert response.status_code == 422

    # Vérifier qu'une explication est fournie
    erreur = response.json()

    assert "detail" in erreur
    assert erreur["detail"]
