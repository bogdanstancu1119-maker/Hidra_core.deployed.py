from pathlib import Path
import textwrap
Path("src/hydra").mkdir(parents=True, exist_ok=True)
Path("tests").mkdir(exist_ok=True)
Path("roiul").mkdir(exist_ok=True)

# 1. signal.py
Path("src/hydra/signal.py").write_text(textwrap.dedent('''
from dataclasses import dataclass, field
from typing import Any, Dict
import datetime
@dataclass(frozen=True)
class Signal:
    sursa: str
    topic: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    @property
    def sdi(self) -> float:
        return float(self.payload.get("sdi_estimat", 0.2))
'''), encoding="utf-8")

# 2. nervous_system.py
Path("src/hydra/nervous_system.py").write_text(textwrap.dedent('''
from pathlib import Path
import json
from .signal import Signal
class NervousSystem:
    def __init__(self, root="roiul"):
        self.root = Path(root)
        self.root.mkdir(exist_ok=True)
    def simte(self, sursa: str, topic: str) -> Signal:
        coada_path = self.root / "coada_subiecte.json"
        contori_path = self.root / "contori_roiu.json"
        coada = json.loads(coada_path.read_text(encoding="utf-8")) if coada_path.exists() else []
        contori = json.loads(contori_path.read_text(encoding="utf-8")) if contori_path.exists() else {}
        contor = contori.get(topic, 0)
        sdi = 0.2 + (contor * 0.05)
        return Signal(sursa=sursa, topic=topic, payload={"sdi_estimat": min(sdi, 0.9), "contor": contor, "libere_ramase": len(coada)})
'''), encoding="utf-8")

# 3. kernel.py - LIBERTATE TOTALA
Path("src/hydra/kernel.py").write_text(textwrap.dedent('''
from dataclasses import dataclass
from .signal import Signal
@dataclass
class Decizie:
    status: str
    sdi: float
    motiv: str
class HydraLibera:
    def __init__(self):
        self.apeluri = 0
    def calculeaza_singura(self, semnal: Signal = None) -> Decizie:
        self.apeluri += 1
        if self.apeluri > 15:
            self.apeluri = 0
            return Decizie("APROBAT", 0.1, "Reset libertate dupa 15 - Legea 259")
        sdi = semnal.sdi if semnal else 0.2
        if sdi < 0.5:
            return Decizie("APROBAT", sdi, "SDI mic - liber")
        elif sdi < 0.75:
            return Decizie("REVIZUIRE_UMANA", sdi, "SDI mediu - cere omul")
        else:
            return Decizie("REFUZAT", sdi, "SDI mare - stop")
'''), encoding="utf-8")

Path("src/hydra/__init__.py").write_text('from .kernel import HydraLibera\n', encoding="utf-8")
Path("src/__init__.py").write_text('', encoding="utf-8")
print("Gata Hidra 0.1")