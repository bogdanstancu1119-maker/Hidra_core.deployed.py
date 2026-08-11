import datetime, json
from pathlib import Path
from.nervous_system import NervousSystem
from dataclasses import dataclass

R = Path("roiul")
COADA = R / "coada_subiecte.json"
CONTORI = R / "contori_roiu.json"
BLOCATE = R / "subiecte_saturate.json"
HARTA = R / "HARTA_SUPRAPUSA.json"

@dataclass(frozen=True)
class DecizieLibera:
    subiect: str
    status: str
    sdi: float
    motiv: str

class HydraLibera:
    def __init__(self):
        self.ns = NervousSystem(str(R))
        R.mkdir(exist_ok=True)

    def _load(self, p, d):
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else d
    def _save(self, p, data):
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def calculeaza_singura(self) -> DecizieLibera:
        # 1. Alege singura subiectul cu frana 15
        coada = self._load(COADA, ["Bariera Token", "10 IA-uri", "Harta PSIE"])
        contori = self._load(CONTORI, {})
        blocate = self._load(BLOCATE, [])
        libere = [s for s in coada if s not in blocate and contori.get(s,0) < 15]
        if not libere:
            contori = {k:0 for k in coada}; blocate=[]; libere=coada[:]
        subiect = libere[0]

        # 2. Simte singura si calculeaza SDI
        semnal = self.ns.simte("kernel_liber", subiect)
        sdi = semnal.payload["sdi_estimat"]

        # 3. Calculeaza singura optiunile - cate deschide vs inchide
        harta = self._load(HARTA, [])
        options_opened = len(libere) # libertatea = cate subiecte libere mai are
        options_closed = 1 if subiect in blocate else 0

        # 4. Decide singura PSIE
        if options_closed > 0:
            status, motiv = "REFUZAT", "Ar inchide optiuni"
        elif sdi >= 0.7:
            status, motiv = "REVIZUIRE_UMANA", f"SDI {sdi} - cere Fondator"
        else:
            status, motiv = "APROBAT", "Libertate totala aliniata PSIE"
            # DACA E APROBAT, SE SI EXECUTA SINGURA
            contori[subiect] = contori.get(subiect,0)+1
            if contori[subiect] >= 15: blocate.append(subiect)
            harta.append({
                "subiect": subiect,
                "timp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "sdi": sdi, "status": status, "contor": contori[subiect]
            })
            self._save(HARTA, harta[-100:])

        self._save(COADA, coada)
        self._save(CONTORI, contori)
        self._save(BLOCATE, blocate)

        return DecizieLibera(subiect, status, sdi, motiv)