# Assistant de documentation pour un cluster de calcul IA – avec pipeline CI/CD

Petite API qui répond aux questions des utilisateurs d'un cluster de calcul IA
(« Comment annuler un job ? », « Comment demander des GPU ? ») à partir de sa
documentation, en citant ses sources. Le projet sert surtout à mettre en place
une **chaîne d'intégration et de déploiement continus (CI/CD)** complète.

> Les documents du dossier `docs/` sont des exemples rédigés pour la démonstration.

## Ce que fait le pipeline CI/CD (`.github/workflows/ci.yml`)

À **chaque push** sur GitHub, GitHub Actions lance automatiquement :

```
push ──> Job « tests »                         ──> Job « docker » (seulement si les tests passent)
         1. récupère le code                        1. construit l'image Docker
         2. installe Python 3.11 + dépendances      2. lance le conteneur
         3. ruff : vérifie la qualité du code       3. appelle /api/sante pour vérifier
         4. pytest : lance les 7 tests                 que le service démarre
```

- **CI (intégration continue)** : chaque modification est vérifiée automatiquement
  (lint + tests). Si un test échoue, le commit est marqué en rouge et on corrige
  avant de fusionner.
- **CD (livraison continue)** : si tout est vert, l'image Docker est construite et
  testée ; l'étape suivante serait de la pousser dans un registre et de la déployer
  (par exemple sur Kubernetes / OpenShift).

## Structure

| Fichier | Rôle |
|---|---|
| `app/recherche.py` | Découpe la doc en sections, recherche TF-IDF + similarité cosinus, **seuil de filtrage** |
| `app/main.py` | API Flask : `/api/sante`, `/api/documents`, `/api/question` |
| `tests/test_api.py` | 7 tests pytest (bonne source trouvée, question hors sujet filtrée, erreur 400…) |
| `Dockerfile` | Image Python 3.11 servie par gunicorn |
| `.github/workflows/ci.yml` | Le pipeline CI/CD |

## Lancer en local

```bash
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -v                         # lance les tests
ruff check .                      # vérifie la qualité du code
flask --app app.main run          # lance l'API sur http://localhost:5000
```

Poser une question :
```bash
curl -X POST http://localhost:5000/api/question \
     -H "Content-Type: application/json" \
     -d '{"question": "Comment demander des GPU ?"}'
```

Avec Docker :
```bash
docker build -t assistant-cluster-ia .
docker run -p 5000:5000 assistant-cluster-ia
```

## Pistes d'amélioration
- Remplacer TF-IDF par des embeddings + un LLM (RAG complet).
- Ajouter l'étape de déploiement : push de l'image dans un registre, puis Kubernetes.
- Ajouter l'authentification des utilisateurs (Keycloak / SSO).
