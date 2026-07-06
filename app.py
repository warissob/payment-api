"""payment-api — mini API REST d'autorisation de paiement.

Projet fil rouge du cours « DevOps et Automatisation pour les Systemes
d'Information Bancaire » (Master SIB). Volontairement minimaliste :
l'objectif du TP est le pipeline CI/CD, pas la richesse fonctionnelle.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# Plafond d'autorisation par transaction, en francs CFA (XAF).
PLAFOND = 1_000_000


@app.get("/health")
def health():
    """Sonde de disponibilite utilisee par les tests et l'orchestrateur."""
    return jsonify(status="ok"), 200


@app.post("/authorize")
def authorize():
    """Autorise une transaction si le montant est valide et sous le plafond."""
    data = request.get_json(silent=True) or {}
    amount = data.get("amount")

    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        return jsonify(error="montant invalide"), 400

    if amount > PLAFOND:
        return jsonify(authorized=False, reason="plafond depasse", plafond=PLAFOND), 200

    return jsonify(authorized=True, amount=amount), 200


if __name__ == "__main__":
    # Lancement local en developpement : python app.py
    app.run(host="0.0.0.0", port=8000)
