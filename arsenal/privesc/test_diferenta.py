
from arsenal.privesc.diferenta import cai


def test_diferenta_suid():
    baza = cai("arsenal/privesc/start/baza_suid.txt")
    acum = cai("arsenal/privesc/start/suid.txt")

    noi = acum - baza

    assert len(baza) == 9
    assert len(acum) == 13
    assert len(noi) == 4


def test_suid_noi_periculoase():
    baza = cai("arsenal/privesc/start/baza_suid.txt")
    acum = cai("arsenal/privesc/start/suid.txt")

    noi = acum - baza

    asteptate = {
        "/bin/cp",
        "/usr/bin/find",
        "/usr/bin/nmap",
        "/usr/bin/vim.basic",
    }

    assert noi == asteptate
