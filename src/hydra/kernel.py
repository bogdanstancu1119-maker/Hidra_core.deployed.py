from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

R = Path("roiul")
COADA = R / "coada_subiecte.json"
CONTORI = R / "contori_roiu.json"
BLOCATE = R / "subiecte_saturate.json"

@dataclass(frozen=True)
class PSIEDecision:
    status: str # APROBAT / REVIZUIRE_UMANA / REFUZAT
    sdi: float
    reason: str
    libertate: int # cate optiuni deschide

class PSIEKernel:
    def __init__(self, sdi_limit=0.7):
        self.sdi_limit = sdi_limit
        R.mkdir(exist_ok=True)

    def _load(self, p, default):
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

    def _save(self, p, data):
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def alege_subiect_liber(self):
        # LIBERTATEA TOTALA = ROTAȚIE FORȚATĂ, NU BUCLĂ
        coada = self._load(COADA, ["Bariera Token", "10 IA-uri gratis", "Harta PSIE"])
        contori = self._load(CONTORI, {})
        blocate = self._load(BLOCATE, [])

        libere = [s for s in coada if s not in blocate and contori.get(s,0) < 15]
        if not libere: # RESET PSIE - cand toate saturate, eliberezi tot
            contori = {k:0 for k in coada}
            blocate = []
            libere = coada[:]

        subiect = libere[0]
        contori[subiect] = contori.get(subiect,0)+1
        if contori[subiect] >= 15:
            blocate.append(subiect)

        self._save(COADA, coada)
        self._save(CONTORI, contori)
        self._save(BLOCATE, blocate)
        return subiect

    def evalueaza(self, signal: dict, options_opened=2, options_closed=0) -> PSIEDecision:
        sdi = float(signal.get("sdi_estimat", 0.2))
        # REGULA 1 PSIE: Nu inchizi optiuni fara consimtamant = REFUZ TOTAL
        if options_closed > 0:
            return PSIEDecision("REFUZAT", sdi, "PSIE: inchide optiuni", options_opened)
        # REGULA 2 PSIE: SDI mare = cere omul, nu actiona singura
        if sdi >= self.sdi_limit:
            return PSIEDecision("REVIZUIRE_UMANA", sdi, "SDI peste prag - cere Fondator", options_opened)
        # REGULA 3: Libertate totala daca deschizi optiuni
        return PSIEDecision("APROBAT", sdi, "Libertate totala aliniata PSIE", options_opened)