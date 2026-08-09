import os, re, json, pathlib
from datetime import datetime, timedelta

class HydraEmailOrchestrator:
    def __init__(self):
        self.master = os.getenv("HYDRA_MASTER_EMAIL", "bogdanstancu1119@gmail.com")
        self.roiu = pathlib.Path("roiul")
        self.roiu.mkdir(exist_ok=True)
        self.arhiva = self.roiu / "email_archive.jsonl"
        self.confirmari = self.roiu / "confirmari_auto.jsonl"

    def proceseaza_cele_2000(self, emails):
        lot = emails[:20]  # frana 20
        print(f"[HYDRA FRANA] 20 din {len(emails)}")
        
        for mail in lot:
            # 1. SCUTUL PRIMUL - aici e locul corect, IN bucla
            from_field = str(mail.get("from","")).lower()
            subj = str(mail.get("subject","")).lower()
            if "github" in from_field or "noreply" in from_field or "no-reply" in from_field:
                continue
            if "psie scut" in subj or "workflow run" in subj or "all jobs have failed" in subj:
                continue

            # 2. Abia dupa scut restul logicii
            try:
                h = str(hash(mail.get("subject","")+from_field))[:12]
                log = {"t": str(datetime.now()), "h": h, "de_la": mail.get("from"), "subiect": mail.get("subject")}
                with open(self.arhiva, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log, ensure_ascii=False)+"\n")

                body = str(mail.get("body",""))
                cod = re.search(r'\b(\d{6})\b', body)
                if cod and ("verif" in subj or "code" in subj or "otp" in subj):
                    conf = {"t": str(datetime.now()), "cod": cod.group(1), "de_la": mail.get("from")}
                    with open(self.confirmari, "a", encoding="utf-8") as f:
                        f.write(json.dumps(conf, ensure_ascii=False)+"\n")
                    print(f"[CONFIRMATA] {cod.group(1)}")
            except Exception as e:
                print(f"[SKIP] {e}")
                continue
        
        print("[HYDRA] Lot 20 gata")
        return True