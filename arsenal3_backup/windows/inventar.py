import json
import argparse
from dataclasses import dataclass, asdict
import json


# Cai considerate suspecte
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

# ID-urile evenimentelor suspecte
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        return any(cale in self.cale for cale in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"



# Citirea proceselor din fisierul JSON
def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]


# Citirea evenimentelor din fisierul JSON
def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]



@dataclass
class Inventar:
    procese: list
    evenimente: list

    @classmethod
    def din_json(cls, cale_procese, cale_evenimente):
        with open(cale_procese, encoding="utf-8") as f:
            procese = [Proces(**d) for d in json.load(f)]

        with open(cale_evenimente, encoding="utf-8") as f:
            evenimente = [Eveniment(**d) for d in json.load(f)]

        return cls(procese, evenimente)

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self, user):
        return [p for p in self.procese if p.user == user]

    def alarme(self):
        return [e for e in self.evenimente if e.e_suspect()]




# Testarea incarcarii datelor
procese = procese_din_json("start/procese.json")
evenimente = evenimente_din_json("start/evenimente.json")

print("procese:", len(procese))
print("suspecte:", sum(1 for p in procese if p.e_suspect()))

print("evenimente:", len(evenimente))
print("alarme:", sum(1 for e in evenimente if e.e_suspect()))




# Testarea clasei Eveniment
e = Eveniment(
    4625,
    "warning",
    "Microsoft-Windows-Security-Auditing",
    "administrator",
    "An account failed to log on"
)

print(e.e_suspect())

def main():
    parser = argparse.ArgumentParser(
        description="Inventar de procese și evenimente Windows"
    )

    parser.add_argument(
        "--procese",
        default="start/procese.json",
        help="Fisierul JSON cu procese"
    )

    parser.add_argument(
        "--evenimente",
        default="start/evenimente.json",
        help="Fisierul JSON cu evenimente"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Afiseaza rezultatul in format JSON"
    )

    args = parser.parse_args()

    inv = Inventar.din_json(args.procese, args.evenimente)

    if args.json:
        rezultat = {
            "numar_procese": len(inv),
            "numar_evenimente": len(inv.evenimente),
            "procese_suspecte": [
                asdict(p) for p in inv.suspecte()
            ],
            "alarme": [
                asdict(e) for e in inv.alarme()
            ]
        }

        print(json.dumps(rezultat, indent=4, ensure_ascii=False))

    else:
        print("=== INVENTAR WINDOWS ===")
        print("Numar procese:", len(inv))
        print("Numar evenimente:", len(inv.evenimente))

        print("\nProcese suspecte:")
        for p in inv.suspecte():
            print(f"[{p.pid}] {p.nume} - {p.cale}")

        print("\nAlarme:")
        for e in inv.alarme():
            print(f"[{e.id}] {e.nivel} - {e.mesaj}")


if __name__ == "__main__":
    main()
