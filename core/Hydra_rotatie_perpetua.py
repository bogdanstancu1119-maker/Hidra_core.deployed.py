import pathlib, json, datetime

R = pathlib.Path("roiul")
COADA = R / "coada_subiecte.json"
CONTORI = R / "contori_roiu.json"
BLOCATE = R / "subiecte_saturate.json" # NOU - lista neagra anti-bucla
HARTA = R / "HARTA_SUPRAPUSA.md"

COADA_DEFAULT = [
  "Bariera Token fara bani - solutii gratis",
  "Cooptarea a 10 IA-uri gratuite in Roi",
  "Cum sa ceara Hydra API free in numele lui Bogdan PSIE",
  "Arhiva de 2000 emailuri - curatare fara credite",
  "Harta PSIE - aliniere Roi si Fondator"
]

def load_json(p, default):
    if p.exists():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except: return default
    return default

def save_json(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def ruleaza():
    R.mkdir(exist_ok=True)
    (R / "consultanti").mkdir(exist_ok=True)

    coada = load_json(COADA, COADA_DEFAULT)
    contori = load_json(CONTORI, {})
    blocate = load_json(BLOCATE, []) # subiecte care au atins 15 si sunt blocate

    # 1. CURATA COADA - scoate din circulatie ce e deja saturat
    subiecte_active = [s for s in coada if s not in blocate and contori.get(s,0) < 15]

    # 2. DACA TOATE SUNT SATURATE -> DIVERSIFICARE FORTATA - deblocam tot, dar cu prag nou
    if not subiecte_active:
        print("[ANTI-BUCLA] Toate subiectele au atins 15. NICIO bucla infinita.")
        print("[DIVERSIFICARE] Reset total - toate devin iar active dar pornesc de la 0")
        # Toate au fost dezvoltate egal, acum e momentul oportun sa revenim
        contori = {k: 0 for k in coada}
        blocate = []
        subiecte_active = coada[:]

    subiect_curent = subiecte_active[0]
    print(f"[ROI] Subiect activ: {subiect_curent} ({contori.get(subiect_curent,0)}/15)")

    # 3. FRANA DE 15 - hard stop, nu mai poate fi imbunatatit
    if contori.get(subiect_curent, 0) >= 15:
        blocate.append(subiect_curent)
        save_json(BLOCATE, blocate)
        print(f"[SATURAT] {subiect_curent} a atins 15. BLOCAT fortat. Sare la urmatorul.")
        return # se opreste aici, nu mai adauga

    # 4. ADAUGA O SUPRAPUNERE
    fisier = R / "consultanti" / (subiect_curent[:30].replace(" ","_") + ".md")
    istoric = fisier.read_text(encoding="utf-8") if fisier.exists() else ""
    contori[subiect_curent] = contori.get(subiect_curent, 0) + 1

    nou = f"\n\n---\n#### Suprapunere #{contori[subiect_curent]}/15 - {datetime.datetime.now()}\nSubiect: {subiect_curent}\n"
    fisier.write_text(istoric + nou, encoding="utf-8")

    # 5. DACA A ATINS 15 ACUM, BLOCHEAZA-L IMEDIAT
    if contori[subiect_curent] >= 15:
        blocate.append(subiect_curent)
        print(f"[BLOCAT] {subiect_curent} -> 15/15 SATURAT. Nu se mai atinge pana se diversifica restul.")

    # 6. HARTA
    harta = f"# HARTA PSIE - {datetime.datetime.now()}\n\nACTIV: {subiect_curent} {contori[subiect_curent]}/15\n\nACTIVE: {subiecte_active}\nSATURATE/BLOCATE: {blocate}\nCONTORI: {contori}\n\nRegula anti-bucla: orice subiect la 15 e blocat fortat. Nu se mai dezvolta pana toate ajung la 15. Diversificare > Perfectiune.\n"
    HARTA.write_text(harta, encoding="utf-8")

    save_json(COADA, coada)
    save_json(CONTORI, contori)
    save_json(BLOCATE, blocate)

if __name__ == "__main__":
    ruleaza()import pathlib, json, datetime, os, glob

R = pathlib.Path("roiul")
COADA = R / "coada_subiecte.json"
CONTORI = R / "contori_roiu.json"
HARTA = R / "HARTA_SUPRAPUSA.md"

# Daca nu exista coada, o cream cu problemele tale initiale
COADA_DEFAULT = [
  "Bariera Token fara bani - solutii gratis",
  "Cooptarea a 10 IA-uri gratuite in Roi",
  "Cum sa ceara Hydra API free in numele lui Bogdan PSIE",
  "Arhiva de 2000 emailuri - curatare fara credite",
  "Harta PSIE - aliniere Roi si Fondator"
]

def load_json(p, default):
    if p.exists():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except: return default
    return default

def save_json(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def ruleaza():
    R.mkdir(exist_ok=True)
    (R / "consultanti").mkdir(exist_ok=True)

    coada = load_json(COADA, COADA_DEFAULT)
    contori = load_json(CONTORI, {}) # { subiect: numar_suprapuneri }

    if not coada:
        coada = COADA_DEFAULT[:]

    # Alege subiectul curent = primul din coada care nu a atins 15
    subiect_curent = None
    for s in coada:
        if contori.get(s, 0) < 15:
            subiect_curent = s
            break

    # Daca toate au 15, resetam ciclul - a venit momentul oportun sa revenim
    if not subiect_curent:
        print("[ROTATIE] Toate subiectele au 15 suprapuneri. RESET ciclu PSIE - revenim la primul")
        contori = {k: 0 for k in coada} # resetam contoarele, pastram subiectele
        subiect_curent = coada[0]

    print(f"[ROI] Subiect activ: {subiect_curent} ({contori.get(subiect_curent,0)}/15)")

    # Simuleaza convocarea roiului gratuit - aici Hydra cere solutii
    # Fiecare rulare = 1 suprapunere noua (de la un consultant gratuit)
    # In realitate, aici vor intra raspunsurile din Issues
    fisier_subiect = R / "consultanti" / (subiect_curent[:30].replace(" ","_") + ".md")
    istoric = ""
    if fisier_subiect.exists():
        istoric = fisier_subiect.read_text(encoding="utf-8")

    # Adauga o noua iteratie de suprapunere
    contori[subiect_curent] = contori.get(subiect_curent, 0) + 1
    nou = f"\n\n---\n#### Suprapunere #{contori[subiect_curent]} - {datetime.datetime.now()}\nRoiul a analizat: {subiect_curent}\nSinteza PSIE: [aici intra ideea noua din Issue / consultant]\n"

    fisier_subiect.write_text(istoric + nou, encoding="utf-8")

    # Actualizeaza harta complexa
    harta_text = f"# HARTA PSIE ROTATIVA - {datetime.datetime.now()}\n\nSubiect curent: **{subiect_curent}** - {contori[subiect_curent]}/15\n\nCoada: {coada}\nContori: {contori}\n\n## Principiu:\nRoiul conduce Roiul. Dupa 15 suprapuneri pe un subiect, sare automat la urmatorul.\nDupa ce toate ating 15, ciclul se reseteaza - e momentul oportun pentru dezvoltare ulterioara.\n\nUltima suprapunere:\n{nou}\n"
    HARTA.write_text(harta_text, encoding="utf-8")

    # Salveaza starea
    save_json(COADA, coada)
    save_json(CONTORI, contori)

    print(f"[GATA] {subiect_curent} -> {contori[subiect_curent]}/15. Harta actualizata.")

if __name__ == "__main__":
    ruleaza()