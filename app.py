from flask import Flask

app = Flask(__name__)

@app.route("/")
def accueil():
    return "Bienvenue sur Payment API"

@app.route("/paiement")
def paiement():
    return "Paiement accepté"

@app.route("/solde")
def solde():
    return "Solde disponible"

    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)