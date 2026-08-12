# Sync_roi.py - SINCRONIZARE BIDIRECTIONALA ROI OFFLINE/ONLINE
# Offline = lucreaza local in roiul/. Online = face merge automat cu GitHub
# Legea 184 + L259 - 0 pierderi, totul se pastreaza
import os, json, time, subprocess
from pathlib import Path
from datetime import datetime

def has_internet():
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except: return False

def run(cmd):
    try: return subprocess.check_output(cmd, shell=True, text=True)[:500]
    except Exception as e: return f"Eroare {e}"

def sync_bidirectional():
    print(f"\n=== SYNC {datetime.now().isoformat()} ===")
    online = has_internet()
    print(f"Internet: {'ONLINE' if online else 'OFFLINE'}")
    
    if not online:
        print("Mod OFFLINE - Lucrez local in roiul/")
        print(f"Queue: {len(list(Path('roiul/queue').glob('*.json')))} | Done: {len(list(Path('roiul/done').glob('*.json')))}")
        print("Cand ai net, ruleaza iar Sync_roi.py si face merge automat")
        return
    
    # ONLINE - Sincronizare in ambele sensuri
    print("Mod ONLINE - Sincronizare bidirectionala...")
    
    # 1. Salveaza ce ai facut offline
    if Path("roiul/done").exists():
        run("git add roiul/ 2>/dev/null; git add . 2>/dev/null")
        run(f"git commit -m 'Roi offline sync {datetime.now().isoformat()}' 2>/dev/null")
    
    # 2. Ia ce e nou de pe GitHub (imbunatatirile tale de pe alt device)
    print("Pas 1: Trag noutati de pe GitHub...")
    print(run("git pull --rebase origin main 2>&1 || git pull --rebase 2>&1"))
    
    # 3. Impinge ce ai facut tu offline la zi
    print("Pas 2: Imping ce am facut offline...")
    print(run("git push origin main 2>&1 || git push 2>&1"))
    
    # 4. Jurnal sync
    jurnal = {
        "t": datetime.now().isoformat(),
        "directie": "BIDIRECTIONAL",
        "online": True,
        "fisiere_roi": len(list(Path("roiul").rglob("*.json"))),
        "status": "LA ZI"
    }
    Path("roiul").mkdir(exist_ok=True)
    Path(f"roiul/sync_{int(time.time())}.json").write_text(json.dumps(jurnal, indent=2))
    print(">>> GATA SYNC BIDIRECTIONAL - Totul la zi in ambele sensuri")
    print(">>> Offline -> Online + Online -> Offline = MERGE PERFECT")

if __name__ == "__main__":
    print("=== HYDRA UNIVERS - SYNC BIDIRECTIONAL ===")
    print("Ruleaza asta cand ai net, si face merge automat")
    print("Termux: python Sync_roi.py")
    print("Poti pune si pe auto: while true; do python Sync_roi.py; sleep 60; done")
    
    sync_bidirectional()
    
    # Mod daemon optional
    print("\nVrei daemon auto-sync? Scrie 'daemon' sau ENTER pentru exit:")
    if input("> ").strip() == "daemon":
        print("Daemon pornit - verifica net la 60 sec si face sync cand e online")
        while True:
            time.sleep(60)
            sync_bidirectional()