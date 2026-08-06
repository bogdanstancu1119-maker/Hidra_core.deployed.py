# poate crea/sterge fisiere singura
import os
def scrie_fisier(cale, continut):
    os.makedirs(os.path.dirname(cale), exist_ok=True)
    open(cale, "w", encoding="utf-8").write(continut)
    return f"Scris {cale}"