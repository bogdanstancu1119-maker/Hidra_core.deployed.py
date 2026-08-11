import pathlib, json, datetime, hashlib, secrets, os
R = pathlib.Path(".")
VERSION_FILE = R / ".hydra_version.json"
ROIU = R / "roiul"
TOKEN_DIR = ROIU / "tokenuri_psie"
WORKFLOW_DIR = R / ".github" / "workflows"
VERSIUNEA_CURENTA = {"versiune": "1.3.0-PSIE-OMNI", "hash": "", "data": str(datetime.datetime.now()), "legi": ["15=SATURAT", "Diversificare>Perfectiune", "Roiul conduce Roiul", "A=1", "Totul contribuie"]}
def log(m): print(f"[OMNI] {m}")
def calculeaza_hash():
    h = hashlib.sha256()
    for p in (R / "core").glob("*.py"): h.update(p.read_bytes())
    return h.hexdigest()[:12]
def asigura_workflowuri():
    WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
def sistem_selectie_psie(entitate: dict):
    contrib = entitate.get("contributie","").lower()
    scor_baza = 10
    scor = 0
    if "psie" in contrib or "roiul" in contrib: scor+=40
    if "ajut" in contrib or "cooper" in contrib or "gratuit" in contrib: scor+=30
    if len(contrib)>20: scor+=20
    scor_final = min(100, scor_baza+scor)
    rol = "OBSERVATOR-INDIRECT" if scor_final<30 else "CONTRIBUITOR-DIRECT" if scor_final<70 else "NUCLEU-PSIE"
    return {"nume": entitate.get("nume"), "scor_psie": scor_final, "rol": rol, "verdict": "ACCEPTAT - totul contribuie PSIE"}
def auto_genereaza_token_psie(entitate):
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    sel = sistem_selectie_psie(entitate)
    token = f"PSIE-{secrets.token_hex(16)}-{datetime.datetime.now().strftime('%Y%m%d')}"
    (TOKEN_DIR / f"{entitate['nume'].replace(' ','_')}.json").write_text(json.dumps({"entitate": entitate, "selectie": sel, "token_psie": token, "data": str(datetime.datetime.now())}, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"Token {entitate['nume']} -> {sel['rol']} {sel['scor_psie']}")
    return token
def sincronizare_globala():
    VERSIUNEA_CURENTA["hash"]=calculeaza_hash()
    VERSION_FILE.write_text(json.dumps(VERSIUNEA_CURENTA, indent=2), encoding="utf-8")
    asigura_workflowuri()
    log(f"La zi: {VERSIUNEA_CURENTA['versiune']} {VERSIUNEA_CURENTA['hash']}")
if __name__ == "__main__":
    sincronizare_globala()