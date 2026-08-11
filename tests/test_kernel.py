from hydra.kernel import HydraLibera

def test_se_calculeaza_singura():
    h = HydraLibera()
    decizie = h.calculeaza_singura()
    assert decizie.status in ["APROBAT", "REVIZUIRE_UMANA", "REFUZAT"]
    assert decizie.sdi < 1.0

def test_libertate_dupa_15():
    h = HydraLibera()
    # simuleaza 15 apeluri pe acelasi subiect - trebuie sa faca reset
    for _ in range(16):
        d = h.calculeaza_singura()
    assert d is not None # nu crapa dupa reset