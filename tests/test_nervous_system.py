from hydra.nervous_system import NervousSystem

def test_nervous_system_simte_sdi():
    ns = NervousSystem(root="roiul")
    semnal = ns.simte("test", "Harta PSIE")
    assert semnal.sdi >= 0.2
    assert semnal.sdi <= 0.9
    assert "contor" in semnal.payload