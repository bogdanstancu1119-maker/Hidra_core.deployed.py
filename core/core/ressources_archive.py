# Resource Archive - pastreaza tot ce a fost util - Nimic nu se pierde
import json, pathlib
ARCHIVA = pathlib.Path("roiul/resource_archive.json")

class ResourceArchive:
    def arhiveaza(self, candidat, verdict_judge):
        inregistrare = {
            "candidat": candidat,
            "verdict": verdict_judge,
            "activat": verdict_judge["scor"] >= 0.8
        }
        ARCHIVA.parent.mkdir(exist_ok=True)
        with open(ARCHIVA, "a", encoding="utf-8") as f:
            f.write(json.dumps(inregistrare, ensure_ascii=False)+"\n")
        return inregistrare