import os, re, json, pathlib
from datetime import datetime, timedelta

class HydraEmailOrchestrator:
    def __init__(self):
        self.master = os.getenv("HYDRA_MASTER_EMAIL", "bogdanstancu1119@gmail.com")
        self.roiu = pathlib.Path("roiul")
        self.roiu.mkdir(exist_ok=True)
        self.arhiva = self.roiu / "email_archive.jsonl"
        self.confirmari = self.roiu / "confirmari_auto.jsonl"

    def proceseaza_cele_2000(self, emails): # emails = lista de la Gmail API
        # Asta ruleaza o data ca sa curete haosul
        for mail in emails:
            # 1. PSIE - nu sterge, arhiveaza
            log = {
                "t": str(datetime.now()),
                "de_la": mail.get("from"),
                "subiect": mail.get("subject"),
                "alias": self.detecteaza_alias(mail),
                "tip": self.clasifica(mail)
            }
            with open(self.arhiva, "a", encoding="utf-8") as f:
                f.write(json.dumps(log, ensure_ascii=False)+"\n")

    def detecteaza_alias(self, mail):
        to = str(mail.get("to", "")).lower()
        if f"+hydra." in to:
            return to
        return self.master

    def clasifica(self, mail):
        subj = str(mail.get("subject","")).lower()
        if "verif" in subj or "otp" in subj or "code" in subj or "confirm" in subj:
            return "cod_verificare"
        if "welcome" in subj or "get started" in subj:
            return "onboarding"
        return "info"

    def extrage_cod_si_confirma(self, mail):
        # Cauta cod 6 cifre in body
        body = str(mail.get("body",""))
        cod = re.search(r'\b(\d{6})\b', body)
        if not cod:
            cod = re.search(r'code is[: ]+([A-Z0-9]{6,8})', body, re.I)
        if cod:
            valoare = cod.group(1)
            # Scrie confirmarea - nu o trimite la platforma automat
            # o pune in fisier pe care hydra_planetary_core il foloseste
            confirm = {
                "t": str(datetime.now()),
                "alias": self.detecteaza_alias(mail),
                "platforma": mail.get("from"),
                "cod": valoare,
                "actiune": "gata de folosit pentru token"
            }
            with open(self.confirmari, "a", encoding="utf-8") as f:
                f.write(json.dumps(confirm, ensure_ascii=False)+"\n")
            print(f"[HYDRA CONFIRMA SINGURA] {confirm['alias']} -> cod {valoare} de la {confirm['platforma']}")
            return valoare
        return None

    def ruleaza_autonom(self):
        # Asta va rula la fiecare heartbeat
        # 1. Citeste ultimele 50 emailuri necitite din inbox-ul tau real (readonly)
        # 2. Pentru fiecare cu alias +hydra.* extrage codul
        # 3. Arhiveaza emailul (nu sterge) in Gmail -> Archive
        # 4. Scrie codul in confirmari_auto.jsonl
        # De aici, Hydra ia codul si cere token-ul oficial de la platforma
        pass