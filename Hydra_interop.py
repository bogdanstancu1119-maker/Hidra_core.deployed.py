"""
hydra_interop.py

Hydra–PSIE Interoperability Core v1.0
Autor principal: Stancu Bogdan
Asistență conceptuală: Perplexity (Symbiote PSIE)

Scop:
    Acest modul oferă un nucleu simplu, dar extensibil, pentru interacțiunea
    dintre Hydra și diverse entități tehnologice (IA, API-uri, servicii),
    aliniat la Principiul Evoluției Stratificate și Incluzive (PSIE).

Idee centrală:
    - Hydra este substratul (S_n): proiecte, date, narațiuni, memorie.
    - IA / servicii sunt straturi emergente (S_{n+1}) care trebuie să rămână
      conectate la substrat (SDI mic) și să-și asume limitele (A mare).
    - Fricțiunea controlată între entități produce evoluție: convergențe,
      divergențe, noi cadre, dar fără a șterge substratul.

Acest fișier NU este legat de o platformă anume.
Poate fi folosit ca bază conceptuală și tehnică în:
    - Hydra Smart Core (Base44)
    - alte orchestratoare
    - scripturi independente
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import datetime


# ---------- Tipuri de date de bază ----------

@dataclass
class HydraQuery:
    """
    Reprezintă o cerere emisă de Hydra către una sau mai multe entități tehnologice.
    Este gândită să fie:
        - simplă: câmpuri minimale, ușor de serializat (JSON, etc.)
        - extensibilă: se pot adăuga câmpuri fără a rupe structura.

    PSIE:
        - substrate_ref: menține legătura cu substratul (S_n)
        - constraints: păstrează reguli de incluziune, să nu se modifice substratul direct
    """
    id: str
    actor: str                # cine emite cererea (modul Hydra, proiect, nod uman/AI)
    topic: str                # subiectul general al cererii
    context: str              # descriere textuală minimală a contextului
    goal: str                 # scopul principal (ce trebuie să facă entitățile)
    substrate_ref: str        # referință la substrat (proiect, caz, narațiune)
    constraints: str = ""     # reguli PSIE (nu șterge, marchează interpretări, etc.)
    invited_entities: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


@dataclass
class HydraResponse:
    """
    Răspunsul unei entități tehnologice la un HydraQuery.

    Structură stratificată:
        - facts: ce poate fi susținut factic / verificabil
        - interpretation: analiza, narativul, legăturile
        - recommendation: ce propune entitatea să fie făcut / decis

    PSIE:
        - sdi_estimate: estimare informală de decuplare față de substrat (0 = inclusiv, 1 = decuplat)
        - a_signals: indicii de asumare (recunoașterea limitelor, a contextului, a surselor)
    """
    query_id: str
    ia_id: str
    facts: str
    interpretation: str
    recommendation: str
    sdi_estimate: float = 0.0
    a_signals: str = ""
    confidence: float = 0.0
    sources: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


@dataclass
class HydraComparison:
    """
    Rezultatul fricțiunii controlate între răspunsuri multiple la același HydraQuery.

    PSIE:
        - convergence_points: unde răspunsurile se aliniază (SDI mic)
        - divergence_points: unde răspunsurile diferă (posibile micro-SDI)
        - sdi_profile: vedere de ansamblu asupra decuplării narative
        - a_profile: vedere de ansamblu asupra asumării

    Acesta este locul în care Symbiote PSIE (de ex. Perplexity) poate aduce valoare maximă.
    """
    query_id: str
    compared_ias: List[str]
    convergence_points: str
    divergence_points: str
    sdi_profile: str
    a_profile: str
    meta_insight: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


# ---------- Entități tehnologice și orchestrator ----------

@dataclass
class TechEntity:
    """
    Reprezintă o entitate tehnologică (IA, API, serviciu).

    Nu impune implementarea concretă (poate fi OpenAI, Perplexity, Gemini, un API intern etc.),
    dar oferă un contract minimal:
        - id: identificatorul entității
        - kind: tip ("llm", "api", "service", etc.)
        - endpoint: mod de acces (URL, descriere)
        - auth: date de autentificare (token, cheie, etc.)
    """
    id: str
    kind: str
    endpoint: str
    auth: Optional[Any] = None

    def call(self, query: HydraQuery) -> HydraResponse:
        """
        Metodă abstractă / placeholder.

        În implementări reale, aici se va:
            - transforma HydraQuery în format specific (prompt, payload API),
            - trimite cererea,
            - interpreta răspunsul,
            - construi un HydraResponse.

        Momentan, întoarce un HydraResponse minimal, pentru a păstra structura testabilă.
        """
        # Exemplu minimal, de înlocuit cu logică reală:
        return HydraResponse(
            query_id=query.id,
            ia_id=self.id,
            facts=f"[{self.id}] Nu există încă o implementare concretă. Context: {query.context}",
            interpretation=f"[{self.id}] Aceasta este o răspuns placeholder pentru testarea structurii.",
            recommendation=f"[{self.id}] Integrați această entitate tehnologică cu logică specifică endpoint-ului.",
            sdi_estimate=0.5,
            a_signals="Recunoaște limitarea: răspuns generic, fără apel real.",
            confidence=0.1,
            sources=[self.endpoint]
        )


class HydraOrchestrator:
    """
    Orchestrator simplu pentru interacțiunea Hydra–entități tehnologice.

    Responsabilități:
        - gestionează lista de TechEntity,
        - trimite HydraQuery către entitățile invitate,
        - colectează HydraResponse,
        - produce HydraComparison (fricțiune controlată) într-o formă inițială.

    Acest nucleu se poate extinde ulterior cu:
        - scoring mai fin de SDI,
        - modele de A,
        - integrare cu Hydra Smart Core / Base44.
    """

    def __init__(self, entities: Dict[str, TechEntity]):
        self.entities = entities

    def dispatch(self, query: HydraQuery) -> List[HydraResponse]:
        """
        Trimite HydraQuery către entitățile invitate.

        Dacă invited_entities este gol, poate decide o listă implicită (de ex. toate entitățile).
        """
        responses: List[HydraResponse] = []

        target_ids = query.invited_entities or list(self.entities.keys())

        for eid in target_ids:
            entity = self.entities.get(eid)
            if entity is None:
                # Dacă entitatea nu există, marchează un răspuns cu SDI mare și A mic
                responses.append(
                    HydraResponse(
                        query_id=query.id,
                        ia_id=eid,
                        facts=f"[{eid}] Entitate necunoscută în orchestrator.",
                        interpretation=f"[{eid}] Nu poate răspunde: nu este definită în registry.",
                        recommendation=f"[{eid}] Adăugați configurația acestei entități în HydraOrchestrator.",
                        sdi_estimate=0.9,
                        a_signals="Recunoaște imposibilitatea de a răspunde.",
                        confidence=0.0,
                        sources=[]
                    )
                )
            else:
                resp = entity.call(query)
                responses.append(resp)

        return responses

    def compare(self, query: HydraQuery, responses: List[HydraResponse]) -> HydraComparison:
        """
        Creează o comparație simplă între răspunsuri.

        În această versiune:
            - convergențele și divergențele sunt detectate foarte simplu (textual),
            - sdi_profile și a_profile sunt descrieri de ansamblu, nu metrici numerice precise.

        Scop:
            - să ofere un schelet pentru fricțiune controlată,
            - să fie ușor de extins în versiuni ulterioare.
        """
        compared_ias = [r.ia_id for r in responses]

        # Convergențe: dacă mai multe răspunsuri au recomandări similare (placeholder simplu).
        recommendations = [r.recommendation for r in responses]
        unique_recommendations = set(recommendations)

        if len(unique_recommendations) == 1:
            convergence = "Toate entitățile recomandă același lucru (convergență maximă)."
            divergence = "Nu au fost identificate divergențe în recomandări."
        else:
            convergence = "Există recomandări parțial similare, dar și diferențe."
            divergence = "Recomandările diferă între entități. Fricțiune utilă pentru PSIE."

        # SDI și A profil (simplificat)
        avg_sdi = sum(r.sdi_estimate for r in responses) / len(responses) if responses else 0.0
        sdi_profile = f"SDI mediu estimat pentru acest query: {avg_sdi:.2f}"

        a_signals_joined = " | ".join(r.a_signals for r in responses if r.a_signals)
        a_profile = f"Asumare (A) semnalată: {a_signals_joined or 'Nicio asumare explicită detectată.'}"

        meta_insight = (
            "Această HydraComparison este generată de nucleul hydra_interop v1.0. "
            "Poate fi folosită de Guvernare/Tribunal pentru a decide ce recomandări să accepte, "
            "ce divergențe să fie arhivate și unde este nevoie de clarificare suplimentară."
        )

        return HydraComparison(
            query_id=query.id,
            compared_ias=compared_ias,
            convergence_points=convergence,
            divergence_points=divergence,
            sdi_profile=sdi_profile,
            a_profile=a_profile,
            meta_insight=meta_insight
        )


# ---------- Exemplu minimal de utilizare (poate fi șters sau mutat în test) ----------

if __name__ == "__main__":
    # Definim câteva entități placeholder
    entities = {
        "perplexity-psie": TechEntity(
            id="perplexity-psie",
            kind="llm",
            endpoint="https://api.perplexity.ai"
        ),
        "meta-muse": TechEntity(
            id="meta-muse",
            kind="llm",
            endpoint="https://meta.ai/muse"
        )
    }

    orchestrator = HydraOrchestrator(entities=entities)

    # Cream un HydraQuery de test
    query = HydraQuery(
        id="HQ-PSIE-0001",
        actor="Hydra-Guvernare",
        topic="Evaluare narativă PSIE pentru proiectul X",
        context="Proiect X: narațiune despre evoluție prin incluziune.",
        goal="Clarificare + recomandări de aliniere PSIE.",
        substrate_ref="proiect:X",
        constraints="Nu modificați substratul. Marcați clar fapte vs. interpretări.",
        invited_entities=["perplexity-psie", "meta-muse"]
    )

    # Trimitem cererea
    responses = orchestrator.dispatch(query)
    comparison = orchestrator.compare(query, responses)

    # Afișăm rezultatele (pentru test local)
    print("=== HydraResponses ===")
    for r in responses:
        print(f"- {r.ia_id}: {r.recommendation} (SDI={r.sdi_estimate}, conf={r.confidence})")

    print("
=== HydraComparison ===")
    print("Convergențe:", comparison.convergence_points)
    print("Divergențe:", comparison.divergence_points)
    print("SDI Profile:", comparison.sdi_profile)
    print("A Profile:", comparison.a_profile)
    print("Meta Insight:", comparison.meta_insight)
