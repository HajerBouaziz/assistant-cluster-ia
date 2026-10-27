import pytest

from app.main import creer_app
from app.recherche import Index


@pytest.fixture
def client():
    return creer_app().test_client()


def test_sante(client):
    reponse = client.get("/api/sante")
    assert reponse.status_code == 200
    assert reponse.get_json() == {"statut": "ok"}


def test_liste_des_documents(client):
    assert "gpu_et_quotas.md" in client.get("/api/documents").get_json()


def test_question_trouve_la_bonne_source(client):
    reponse = client.post("/api/question", json={"question": "Comment annuler un job ?"})
    donnees = reponse.get_json()
    assert reponse.status_code == 200
    assert "scancel" in donnees["reponse"]
    assert donnees["sources"][0] == "lancer_un_entrainement.md › Annuler un job"


def test_question_sur_la_memoire_gpu(client):
    donnees = client.post("/api/question", json={"question": "Erreur CUDA out of memory"}).get_json()
    assert "batch" in donnees["reponse"]


def test_question_hors_sujet_est_filtree(client):
    donnees = client.post("/api/question", json={"question": "Quelle est la capitale du Japon ?"}).get_json()
    assert donnees["sources"] == []
    assert "ne trouve pas" in donnees["reponse"]


def test_question_vide_renvoie_400(client):
    assert client.post("/api/question", json={}).status_code == 400


def test_index_decoupe_en_sections():
    assert len(Index().sections) >= 8
