

#A1 – Funcția esec(linie)
import re
from collections import Counter
TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")
 
def esec(linie):
    m = TIPAR.search(linie)
    if m is None:
        return None

    return (m.group(1), m.group(2))
 
print(esec("... Failed password for root from 203.0.113.9 port 51230 ssh2"))
print(esec("<linie stricata fara structura>"))



#A2 – Citirea tuturor eșecurilor din fișier
def citeste_esecuri(cale):

    esecuri = []

    try:
        f = open(cale, encoding="utf-8")

    except FileNotFoundError:
        print("Nu gasesc", cale)
        return esecuri

    with f:
        for linie in f:

            r = esec(linie)

            if r is not None:
                esecuri.append({
                    "user": r[0],
                    "ip": r[1]
                })

    return esecuri

esecuri = citeste_esecuri(r"D:\TP\Tehnici_programare\arsenal2\aparare\start\auth.log")

print("esecuri:", len(esecuri))




#A3 – Numărarea eșecurilor după IP
def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)






#A4 – Funcția principală main()
def main():

    esecuri = citeste_esecuri(r"D:\TP\Tehnici_programare\arsenal2\aparare\start\auth.log")

    counts = pe_ip(esecuri)

    print("Esecuri de autentificare:", len(esecuri))

    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")


if __name__ == "__main__":
    main()