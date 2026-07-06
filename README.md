# payment-api

Mini API REST d'autorisation de paiement, servant de **projet fil rouge** au cours
_« DevOps et Automatisation pour les Systèmes d'Information Bancaire »_ (Master SIB — Option MMP).

Ce dépôt est prêt à l'emploi : dès le premier `git push` sur `main`, un pipeline
**GitHub Actions** s'exécute automatiquement (tests → build de l'image Docker →
déploiement soumis à **validation manuelle**).

---

## 1. L'application

Une API Flask volontairement minimaliste (l'objectif du TP est le CI/CD, pas la
richesse fonctionnelle) :

| Méthode | Route         | Rôle                                                         |
|--------:|---------------|--------------------------------------------------------------|
| `GET`   | `/health`     | Sonde de disponibilité → `{"status": "ok"}`                  |
| `POST`  | `/authorize`  | Autorise une transaction si le montant est valide et ≤ plafond |

Le plafond d'autorisation est fixé à **1 000 000 XAF** dans `app.py`.

---

## 2. Lancer et tester en local

```bash
# 1) Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate

# 2) Installer les dépendances
pip install -r requirements.txt

# 3) Lancer les tests
pytest -q

# 4) Démarrer l'API
python app.py
# puis, dans un autre terminal :
curl http://localhost:8000/health
curl -X POST http://localhost:8000/authorize \
     -H "Content-Type: application/json" \
     -d '{"amount": 50000}'
```

### Avec Docker

```bash
docker build -t payment-api:1.0 .
docker run -d --name pay -p 8000:8000 payment-api:1.0
curl http://localhost:8000/health
docker stop pay && docker rm pay
```

---

## 3. Le pipeline CI/CD (GitHub Actions)

Défini dans `.github/workflows/ci.yml`, en trois étapes :

1. **`test`** — installe les dépendances et lance `pytest`. S'exécute sur **toutes** les branches.
2. **`build`** — construit l'image Docker et la publie sur **GHCR** (`ghcr.io`).
   Ne s'exécute que sur `main`, et seulement si les tests passent (`needs: test`).
3. **`deploy`** — déploiement en production, **bloqué par une validation manuelle**
   (`needs: build` + `environment: production`).

Pour déclencher le pipeline :

```bash
git add .
git commit -m "ci: pipeline CI/CD"
git push origin main
```

Suivi de l'exécution : onglet **Actions** du dépôt GitHub.

---

## 4. ⚠️ Activer la validation manuelle (étape à ne pas oublier)

Le job `deploy` référence `environment: production`. Mais **le blocage manuel
n'existe que si l'environnement est configuré avec des reviewers.** Sans cette
configuration, le déploiement partirait automatiquement.

À faire une seule fois, côté GitHub :

1. **Settings → Environments → New environment** → nommez-le exactement **`production`**.
2. Cochez **Required reviewers** et ajoutez au moins une personne (l'enseignant, par exemple).
3. Enregistrez.

Désormais, à chaque exécution sur `main`, le job `deploy` reste **en attente**
jusqu'à ce qu'un reviewer clique sur **Review deployments → Approve and deploy**.
C'est exactement le « contrôle avant la prod » demandé dans le TP.

---

## 5. Note sur GHCR (publication de l'image)

- Le workflow utilise le jeton intégré `GITHUB_TOKEN` : **aucun secret à créer**.
- Après le premier build, l'image apparaît dans l'onglet **Packages** du dépôt.
  Si vous voulez la rendre publique : **Package settings → Change visibility**.
- Le nom d'image est forcé en minuscules (`${GITHUB_REPOSITORY,,}`) car GHCR
  refuse les majuscules — piège classique déjà géré ici.

---

## 6. Structure du dépôt

```
payment-api/
├─ app.py                     # API Flask
├─ requirements.txt           # Flask, gunicorn, pytest
├─ Dockerfile                 # image Python slim, user non-root
├─ .dockerignore
├─ .gitignore
├─ README.md
├─ tests/
│  ├─ __init__.py
│  └─ test_app.py             # 6 tests pytest
└─ .github/
   └─ workflows/
      └─ ci.yml               # pipeline test → build → deploy (manuel)
```
