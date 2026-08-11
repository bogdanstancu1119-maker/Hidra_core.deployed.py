import pathlib, json, datetime, os, glob

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