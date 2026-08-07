class UniversalDeployer:
    platforme = ["github", "base44", "vercel", "cloudflare", "huggingface", "local"]
    
    def deploy(self, resursa):
        # nu intreaba daca are voie, verifica daca e 0 credite si PSIE aliniat
        if resursa["cost"] == 0 and resursa["sdi"] < 0.7:
            return f"deployat pe {self.alege_platforma_libera()}"
    
    def alege_platforma_libera(self):
        # cauta prima fereastra deschisa - Ferestre Permanente
        return "prima care raspunde"