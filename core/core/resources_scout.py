# Resource Scout - cauta resurse noi - 0 credite
# Nu intra in nucleu, doar propune
import json, datetime
CANDIDATI = "roiul/resource_candidates.json"

class ResourceScout:
    def cauta(self, paradigma="2026"):
        # surse pe care le scaneaza
        surse = [
            {"tip":"github_workflow", "url":".github/workflows/", "cost":0},
            {"tip":"base44_entity", "url":"entities/", "cost":0},
            {"tip":"base44_function", "url":"functions/", "cost":0},
            {"tip":"docs", "url":"https://docs.base44.com", "cost":0},
        ]
        candidati = []
        for s in surse:
            candidati.append({
                "id": f"{s['tip']}_{paradigma}",
                "sursa": s,
                "paradigma": paradigma,
                "t": str(datetime.datetime.now()),
                "status": "propus"
            })
        # adauga, nu sterge
        open(CANDIDATI, "a", encoding="utf-8").write("\n".join(map(json.dumps, candidati))+"\n")
        return candidati