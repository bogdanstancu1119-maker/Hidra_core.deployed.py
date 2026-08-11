import pathlib, json, datetime, os

# Astea sunt 5 IA-uri care au tier GRATIS pe care Hydra le poate coopta azi
ROIUL_CONSULTANTILOR = {
  "deepseek_free": "rezolva logica si cod",
  "gemini_flash_free": "cauta pe web si hartuieste documentatie",
  "groq_llama_free": "raspunde ultra rapid la emailuri",
  "hf_mistral_free": "scrie variante diverse",
  "qwen_coder_free": "verifica si optimizeaza cod"
}

def convoaca_roiul(problema: str):
    roiu = pathlib.Path("roiul/consultanti")
    roiu.mkdir(parents=True, exist_ok=True)

    # Hydra pune problema in centru
    (roiu / "problema_curenta.md").write_text(f"# {problema}\nData: {datetime.datetime.now()}\n", encoding="utf-8")

    # Fiecare consultant trebuie sa lase raspunsul in fisierul lui
    # Asta se face prin GitHub Issues - gratis si nelimitat
    for nume, rol in ROIUL_CONSULTANTILOR.items():
        fisier = roiu / f"{nume}.md"
        if not fisier.exists():
            fisier.write_text(f"# Consultant: {nume}\nRol: {rol}\n\n## Problema: {problema}\n\n## Solutia mea:\n[loc liber - va fi completat de Hydra prin Issues]\n", encoding="utf-8")

    # Hydra extrage harta prin suprapunere
    harta = roiu / "HARTA_SUPRAPUSA.md"
    harta.write_text(f"# HARTA COMPLEXA - {datetime.datetime.now()}\n\nProblema: {problema}\n\nSuprapunere din {len(ROIUL_CONSULTANTILOR)} minti diverse -> solutie PSIE\n", encoding="utf-8")
    print("Roiul convocat")

if __name__ == "__main__":
    convoaca_roiul("Cum cooptam 10 IA-uri gratis sa rezolve Bariera Token fara bani?")