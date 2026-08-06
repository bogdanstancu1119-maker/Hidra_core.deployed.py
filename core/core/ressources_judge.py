# Resource Judge - evalueaza inainte sa intre in nucleu - Legea 144
from .noise_filter import este_zgomot
from .psie_kernel import Signal, Context, RiskLevel

class ResourceJudge:
    def evalueaza(self, candidat, context):
        # regula PSIE: nu intra direct in nucleu
        if este_zgomot(candidat["id"]):
            return {"verdict":"respins_zgomot", "scor":0.0}
        
        # scor PSIE: utilitate + coerenta + cost 0
        scor = 0.5
        if candidat["sursa"]["cost"] == 0:
            scor += 0.3
        if "workflow" in candidat["tip"] or "entity" in candidat["tip"]:
            scor += 0.2  # se potriveste cu Hydra
        
        risc = RiskLevel.LOW if scor > 0.7 else RiskLevel.MEDIUM
        
        return {
            "verdict": "acceptat" if scor >= 0.8 else "in_asteptare",
            "scor": scor,
            "risc": risc,
            "regula": "resursa noua nu intra direct, trece prin strat evaluare"
        }