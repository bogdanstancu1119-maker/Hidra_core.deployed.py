from pathlib import Path
import json
from .signal import Signal

class NervousSystem:
    def __init__(self, root="roiul"):
        self.root = Path(root)
        self.root.mkdir(exist_ok=True)

    def simte(self, sursa: str, topic: str) -> Signal:
        # simte coada si cat e de saturat
        coada_path = self.root / "coada_subiecte.json"
        contori_path = self.root / "contori_roiu.json"
        
        coada = json.loads(coada_path.read_text(encoding="utf-8")) if coada_path.exists() else []
        contori = json.loads(contori_path.read_text(encoding="utf-8")) if contori_path.exists() else {}
        
        # calculeaza SDI singur - cu cat contorul e mai mare, cu atat SDI mai mare
        contor = contori.get(topic, 0)
        sdi = 0.2 + (contor * 0.05) # dupa 10 repetari -> 0.7 -> cere omul
        
        return Signal(
            sursa=sursa,
            topic=topic,
            payload={
                "sdi_estimat": min(sdi, 0.9),
                "contor": contor,
                "libere_ramase": len(coada)
            }
        )