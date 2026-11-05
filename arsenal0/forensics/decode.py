
import re
import base64
from urllib.parse import unquote
import hashlib
import json
import argparse
from pathlib import Path


# A1 – Text si octeti (str si bytes)

def exemplu_a1():
    s = "Salut"

    b = s.encode("utf-8")

    print("Text initial:", s)
    print("Reprezentare bytes:", b)
    print("Primul octet:", b[0])

    hex_text = b.hex()
    print("Reprezentare HEX:", hex_text)

    b_refacut = bytes.fromhex(hex_text)
    print("Octeti refacuti:", b_refacut)

    text_final = b_refacut.decode("utf-8")
    print("Text final:", text_final)


# A2 – Recunoasterea automata a codarilor

def recunoaste_format(text):

    if re.search(r'%[0-9A-Fa-f]{2}', text):
        return "URL"

    if re.fullmatch(r'(?:[0-9A-Fa-f]{2})+', text):
        return "HEX"

    try:
        base64.b64decode(text, validate=True)
        return "Base64"
    except Exception:
        pass

    return "Necunoscut"


# A3 – Decodificarea formatelor URL, HEX si Base64

def decodeaza(text, format):

    if format == "URL":
        return unquote(text)

    elif format == "HEX":
        octeti = bytes.fromhex(text)
        return octeti.decode("utf-8")

    elif format == "Base64":
        octeti = base64.b64decode(text, validate=True)
        return octeti.decode("utf-8")

    else:
        return text


# A4 – Decodificarea mesajelor cu mai multe straturi

def decodeaza_straturi(text, maxim=10):

    rezultat = text

    for i in range(maxim):

        format = recunoaste_format(rezultat)

        if format == "Necunoscut":
            break

        try:
            rezultat_nou = decodeaza(rezultat, format)

            if rezultat_nou == rezultat:
                break

            rezultat = rezultat_nou

        except Exception:
            break

    return rezultat


# A5 – Identificarea mesajelor codificate prin XOR

def xor_un_octet(date):

    rezultate = []

    for cheie in range(256):

        rezultat = bytes(
            octet ^ cheie for octet in date
        )

        if all(32 <= b <= 126 for b in rezultat):
            rezultate.append((cheie, rezultat))

    return rezultate


# A6 – Spargerea unui hash prin dictionar

def sparge_hash(cale_hash, cale_wordlist):

    with open(cale_hash, "r", encoding="utf-8") as f:
        tinta = f.readline().strip().lower()

    if len(tinta) == 32:
        algoritm = "md5"

    elif len(tinta) == 40:
        algoritm = "sha1"

    elif len(tinta) == 64:
        algoritm = "sha256"

    else:
        print("Lungime de hash necunoscuta!")
        return None

    print("Lungimea hashului:", len(tinta))
    print("Algoritmul identificat:", algoritm)

    with open(cale_wordlist, "r", encoding="latin1") as f:

        for cuv in f:
            cuv = cuv.strip()

            hash_calculat = hashlib.new(
                algoritm, cuv.encode()
            ).hexdigest()

            if hash_calculat == tinta:
                print("Parola gasita:", cuv)
                return cuv

    print("Parola nu a fost gasita in dictionar.")
    return None


# A7 – Identificarea si decodificarea automata

def ghici_strat(text):
    format = recunoaste_format(text)

    if format == "URL":
        return "url"

    elif format == "HEX":
        return "hex"

    elif format == "Base64":
        return "base64"

    return "necunoscut"


def desfa(text):

    strat = ghici_strat(text)

    # Folosim functia de la A3
    rezultat = decodeaza(text, recunoaste_format(text))

    # Returnam rezultatul in bytes
    rezultat_bytes = rezultat.encode("utf-8")

    return strat, rezultat_bytes


# A7 – Program principal cu argparse si salvare JSON

def main():

    p = argparse.ArgumentParser(
        description="Decoder universal"
    )

    p.add_argument(
        "intrare",
        help="Sir de caractere sau cale catre fisier"
    )

    p.add_argument(
        "--fisier",
        action="store_true",
        help="Citeste intrarea dintr-un fisier"
    )

    a = p.parse_args()

    # Citirea intrarii
    if a.fisier:
        cale = Path(a.intrare)
        text_intrare = cale.read_text(encoding="utf-8")

    else:
        text_intrare = a.intrare

    # Apelarea functiei de decodificare
    strat, rezultat = desfa(text_intrare)

    # Transformarea octetilor in text
    try:
        rezultat_text = rezultat.decode("utf-8")

    except UnicodeDecodeError:
        rezultat_text = rezultat.hex()

    # Crearea fisei JSON
    fisa = {
        "strat": strat,
        "rezultat": rezultat_text
    }

    # Salvarea fisei in acelasi director cu decode.py
    cale_fisa = Path(__file__).parent / "fisa.json"

    with open(cale_fisa, "w", encoding="utf-8") as f:
        json.dump(
            fisa,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("Strat identificat:", strat)
    print("Rezultat:", rezultat_text)
    print("Fisa salvata:", cale_fisa)


# Programul principal se executa doar la rularea directa
if __name__ == "__main__":
    main()
