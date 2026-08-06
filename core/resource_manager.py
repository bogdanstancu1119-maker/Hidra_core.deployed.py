# isi gestioneaza singura resursele
class ResourceManager:
    def __init__(self, core):
        self.core = core
        self.credite = 500
    def stare(self):
        return "95 stabil" if self.core.calculeaza_J() < 50 else "explorez 5%"