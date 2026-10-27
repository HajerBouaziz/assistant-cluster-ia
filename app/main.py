"""API Flask de l'assistant.

Routes :
  GET  /api/sante       -> vérifie que le service fonctionne
  GET  /api/documents   -> liste des documents indexés
  POST /api/question    -> {"question": "..."} -> réponse + sources
"""

from flask import Flask, jsonify, request

from app.recherche import Index


def creer_app() -> Flask:
    app = Flask(__name__)
    app.json.ensure_ascii = False  # écrit les accents tels quels dans le JSON
    app.json.mimetype = "application/json; charset=utf-8"  # précise l'encodage UTF-8 au client
    index = Index()

    @app.get("/api/sante")
    def sante():
        return jsonify(statut="ok")

    @app.get("/api/documents")
    def documents():
        return jsonify(sorted({s.document for s in index.sections}))

    @app.post("/api/question")
    def question():
        donnees = request.get_json(silent=True) or {}
        texte = str(donnees.get("question", "")).strip()
        if not texte:
            return jsonify(erreur="Le champ 'question' est obligatoire."), 400
        passages = index.rechercher(texte)
        if not passages:
            return jsonify(reponse="Je ne trouve pas cette information dans la documentation.", sources=[])
        return jsonify(reponse=passages[0]["texte"], sources=[p["source"] for p in passages])

    return app


app = creer_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)