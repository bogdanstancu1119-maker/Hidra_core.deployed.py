import pathlib, json, datetime
R = pathlib.Path("roiul")
COADA = R / "coada_subiecte.json"
CONTORI = R / "contori_roiu.json"
BLOCATE = R / "subiecte_saturate.json"
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
    blocate = load_json(BLOCATE, [])
    subiecte_active = [s for s in coada if s not in blocate and contori.get(s,0) < 15]
    if not subiecte_active:
        contori = {k: 0 for k in coada}
        blocate = []
        subiecte_active = coada[:]
        print("[DIVERSIFICARE] Reset total - toate 15/15, reincepem valul")
    subiect_curent = subiecte_active[0]
    print(f"[ROI] {subiect_curent} {contori.get(subiect_curent,0)}/15")
    if contori.get(subiect_curent, 0) >= 15:
        blocate.append(subiect_curent)
        save_json(BLOCATE, blocate)
        return
    fisier = R / "consultanti" / (subiect_curent[:30].replace(" ","_") + ".md")
    istoric = fisier.read_text(encoding="utf-8") if fisier.exists() else ""
    contori[subiect_curent] = contori.get(subiect_curent, 0) + 1
    nou = f"\n\n---\n#### Suprapunere #{contori[subiect_curent]}/15 - {datetime.datetime.now()}\n"
    fisier.write_text(istoric + nou, encoding="utf-8")
    if contori[subiect_curent] >= 15:
        blocate.append(subiect_curent)
        print(f"[BLOCAT] {subiect_curent} SATURAT")
    harta = f"# HARTA PSIE - {datetime.datetime.now()}\n\nACTIV: {subiect_curent} {contori[subiect_curent]}/15\nACTIVE: {subiecte_active}\nBLOCATE: {blocate}\nCONTORI: {contori}\n\nRegula: 15 = blocat fortat. Diversificare > Perfectiune.\n"
    HARTA.write_text(harta, encoding="utf-8")
    save_json(COADA, coada)
    save_json(CONTORI, contori)
    save_json(BLOCATE, blocate)
if __name__ == "__main__":
    ruleaza()