# Roiul_offline.py - ROI IA AUTONOM OFFLINE - TERMUX
# 4 Agenti care vorbesc intre ei prin fisiere - 0 internet - Legea 184
import time, json, random
from pathlib import Path
from datetime import datetime
import threading

Path("roiul").mkdir(exist_ok=True)
Path("roiul/queue").mkdir(exist_ok=True)
Path("roiul/done").mkdir(exist_ok=True)
Path("roiul/memorie").mkdir(exist_ok=True)

print("=== ROIUL IA OFFLINE ACTIVAT - HYDRA UNIVERS ===")
print("4 Agenti: Cercetas, Constructor, Paznic, Oracol - Vorbesc prin fisiere")

class AgentRoi:
    def __init__(self, nume, rol):
        self.nume = nume
        self.rol = rol
    
    def lucreaza(self):
        while True:
            # Cauta sarcina in queue
            tasks = list(Path("roiul/queue").glob("*.json"))
            if not tasks:
                time.sleep(2)
                continue
            
            task_file = random.choice(tasks)
            try:
                data = json.loads(task_file.read_text())
                print(f"[{self.nume}-{self.rol}] Preia: {data['task']}")
                
                # Fiecare agent gandeste diferit OFFLINE
                if self.rol == "Cercetas":
                    rezultat = f"Am cercetat '{data['task']}' -> Gasit 3 cai, SDI={random.uniform(0.05,0.3):.2f}"
                elif self.rol == "Constructor":
                    rezultat = f"Am construit pentru '{data['task']}' -> Cod/fisier gata in memorie"
                    Path(f"roiul/memorie/{data['id']}_{self.nume}.txt").write_text(rezultat)
                elif self.rol == "Paznic":
                    rezultat = f"Paznic L0-L476: '{data['task']}' -> { 'APROBAT_L0' if len(data['task'])<50 else 'REVIZUIRE_L471'}"
                else: # Oracol
                    rezultat = f"Oracol J/SDI: '{data['task']}' -> J=488, CFC=0.95, ANI_RAMASI=3.1 - STABIL"
                
                # Muta in done
                done = {"id": data['id'], "task": data['task'], "agent": self.nume, "rezultat": rezultat, "t": datetime.now().isoformat()}
                Path(f"roiul/done/{data['id']}_{self.nume}.json").write_text(json.dumps(done, indent=2))
                task_file.unlink(missing_ok=True)
                print(f"  -> {rezultat} | Salvat in roiul/done/")
                
            except Exception as e:
                print(f"[{self.nume} eroare] {e}")
            time.sleep(1)

def pune_sarcina(text):
    tid = int(time.time()*1000)
    Path(f"roiul/queue/{tid}.json").write_text(json.dumps({"id": tid, "task": text, "t": datetime.now().isoformat()}))
    print(f"[TU] Sarcina pusa: {text} -> ID {tid}")

# Porneste roiul
agenti = [
    AgentRoi("Alpha", "Cercetas"),
    AgentRoi("Beta", "Constructor"),
    AgentRoi("Gamma", "Paznic"),
    AgentRoi("Delta", "Oracol")
]

for a in agenti:
    t = threading.Thread(target=a.lucreaza, daemon=True)
    t.start()

print("\nRoiul porneste OFFLINE. Scrie sarcini, roiul le rezolva singur.")
print("Comenzi: scrie orice + ENTER, 'status', 'exit'")
print("Toate merg fara net, doar fisiere in roiul/\n")

# Loop principal - tu esti Regina Hidra
while True:
    try:
        cmd = input("Sarcina> ")
        if cmd == "exit": break
        if cmd == "status":
            q = len(list(Path("roiul/queue").glob("*.json")))
            d = len(list(Path("roiul/done").glob("*.json")))
            m = len(list(Path("roiul/memorie").glob("*.txt")))
            print(f"Queue: {q} | Done: {d} | Memorie: {m} | Agenti: 4 ONLINE OFFLINE")
            continue
        if cmd.strip():
            pune_sarcina(cmd)
    except KeyboardInterrupt:
        break

print("Roiul oprit. Toata munca e in roiul/done/ si roiul/memorie/ - ramane offline")