"""Indexation de la documentation (Markdown) et recherche des passages pertinents.

Chaque document est découpé en sections (titres « ## »). La recherche utilise
TF-IDF + similarité cosinus ; sous un seuil, aucun passage n'est renvoyé
(filtrage : l'assistant préfère dire qu'il ne sait pas plutôt qu'inventer).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOSSIER_DOCS = Path(__file__).resolve().parent.parent / "docs"
SEUIL = 0.15

MOTS_VIDES = (
    "le la les l un une des de du d et ou a au aux en dans par pour sur avec ce cette ces "
    "est sont quel quelle comment combien pourquoi je il nous vous mon ma mes son sa ses "
    "ne pas plus se s y on faut"
).split()


@dataclass
class Section:
    document: str
    titre: str
    texte: str

    @property
    def source(self) -> str:
        return f"{self.document} › {self.titre}"


def decouper(chemin: Path) -> list[Section]:
    """Découpe un fichier Markdown en sections à partir des titres « ## »."""
    sections, titre, lignes = [], None, []
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        trouve = re.match(r"^##\s+(.*)", ligne)
        if trouve:
            if titre and lignes:
                sections.append(Section(chemin.name, titre, " ".join(lignes)))
            titre, lignes = trouve.group(1).strip(), []
        elif titre and ligne.strip():
            lignes.append(ligne.strip())
    if titre and lignes:
        sections.append(Section(chemin.name, titre, " ".join(lignes)))
    return sections


class Index:
    def __init__(self, dossier: Path = DOSSIER_DOCS):
        self.sections = [s for f in sorted(dossier.glob("*.md")) for s in decouper(f)]
        if not self.sections:
            raise ValueError(f"Aucune section trouvée dans {dossier}")
        self.vectoriseur = TfidfVectorizer(strip_accents="unicode", stop_words=MOTS_VIDES)
        self.matrice = self.vectoriseur.fit_transform(f"{s.titre} {s.texte}" for s in self.sections)

    def rechercher(self, question: str, k: int = 2) -> list[dict]:
        scores = cosine_similarity(self.vectoriseur.transform([question]), self.matrice)[0]
        meilleurs = scores.argsort()[::-1][:k]
        return [
            {"source": self.sections[i].source, "score": round(float(scores[i]), 3), "texte": self.sections[i].texte}
            for i in meilleurs
            if scores[i] >= SEUIL
        ]
