import re

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS



#B1 – Magic bytes: identificarea tipului real al fișierului

def tip_real(cale):
    # Deschidem fisierul in mod binar
    with open(cale, "rb") as f:
        cap = f.read(8)

    # Verificam semnatura fisierului
    if cap.startswith(b"%PDF"):
        return "PDF"

    elif cap.startswith(b"\x89PNG"):
        return "PNG"

    elif cap.startswith(b"\xff\xd8"):
        return "JPEG"

    elif cap.startswith(b"PK\x03\x04"):
        return "ZIP / DOCX"

    else:
        return "Format necunoscut: " + cap.hex()


# Testam functia
print("Tipul real al fisierului:")
print(tip_real("probe/foto.jpg"))





#B2 – strings: extragerea textului citibil dintr-un fișier binar.
def extrage_text(cale):
    # Citim fisierul in format binar
    with open(cale, "rb") as f:
        date = f.read()

    # Cautam secvente de minimum 4 caractere imprimabile
    texte = re.findall(rb"[ -~]{4,}", date)

    # Afisam textele gasite
    for m in texte:
        print(m.decode("ascii"))


# Testam functia
print("\nTexte gasite in fisier:")
extrage_text("probe/ascuns.png")



#B3 – Metadate EXIF și GPS din fotografie.
def extrage_exif(cale):
    # Deschidem fotografia
    img = Image.open(cale)

    # Citim metadatele EXIF
    exif = img.getexif()

    print("Metadatele fotografiei:")

    # Afisam toate metadatele
    for id, val in exif.items():
        nume = TAGS.get(id, id)

        if id != 34853:
            print(nume, "=", val)

    # Extragem informatiile GPS
    gps = exif.get_ifd(34853)

    print("\nInformatii GPS:")

    if not gps:
        print("Fotografia nu contine coordonate GPS.")
        return

    # Transformam identificatorii in denumiri
    gps_date = {}

    for id, val in gps.items():
        nume = GPSTAGS.get(id, id)
        gps_date[nume] = val

    # Convertim grade, minute si secunde in grade zecimale
    def conversie(coord):
        grade, minute, secunde = coord

        return float(grade) + float(minute) / 60 + float(secunde) / 3600

    # Extragem latitudinea si longitudinea
    lat = conversie(gps_date["GPSLatitude"])
    lon = conversie(gps_date["GPSLongitude"])

    # Verificam emisfera
    if gps_date["GPSLatitudeRef"] == "S":
        lat = -lat

    if gps_date["GPSLongitudeRef"] == "W":
        lon = -lon

    print("Latitudine:", lat)
    print("Longitudine:", lon)


# Testam functia
extrage_exif("probe/foto.jpg")






#B4 – File carving: extragerea unui fișier ascuns dintr-o imagine.

def extrage_arhiva(cale):
    # Citim continutul imaginii in format binar
    with open(cale, "rb") as f:
        date = f.read()

    # Cautam semnatura arhivei ZIP
    i = date.find(b"PK\x03\x04")

    # Verificam daca arhiva a fost gasita
    if i != -1:
        # Salvam arhiva intr-un fisier separat
        with open("gasit.zip", "wb") as f:
            f.write(date[i:])

        print("Arhiva extrasa de la octetul:", i)
        print("Fisierul gasit.zip a fost creat.")

    else:
        print("Nu a fost gasita nicio arhiva ZIP.")


# Testam functia
extrage_arhiva("probe/ascuns.png")




#B5 – Ascunderea unui mesaj prin steganografie LSB.
def ascunde_mesaj(cale):
    # Deschidem fotografia si o convertim in RGB
    img = Image.open(cale).convert("RGB")

    # Extragem pixelii imaginii
    px = list(img.getdata())

    # Mesajul pe care vrem sa-l ascundem
    mesaj = b"FLAG{ascuns_in_pixeli}"

    # Adaugam un octet 0 pentru a marca sfarsitul mesajului
    mesaj = mesaj + b"\x00"

    # Transformam mesajul in biti
    biti = "".join(f"{x:08b}" for x in mesaj)

    # Transformam pixelii in valori RGB individuale
    canale = [valoare for pixel in px for valoare in pixel]

    # Verificam daca imaginea are suficienta capacitate
    if len(biti) > len(canale):
        print("Imaginea nu are suficient spatiu!")
        return

    # Ascundem bitii in ultimii biti ai canalelor RGB
    for i, bit in enumerate(biti):
        canale[i] = (canale[i] & ~1) | int(bit)

    # Refacem pixelii RGB
    px_nou = [
        tuple(canale[i:i + 3])
        for i in range(0, len(canale), 3)
    ]

    # Introducem pixelii modificati in imagine
    img.putdata(px_nou)

    # Salvam imaginea rezultata in format PNG
    img.save("stego.png")

    print("Mesajul a fost ascuns cu succes!")
    print("Imaginea rezultata: stego.png")


# Testam functia
ascunde_mesaj("probe/foto.jpg")






#B6 – Extragerea mesajului ascuns în biții LSB
def dezvaluie_mesaj(cale):
    img = Image.open(cale).convert("RGB")
    px = list(img.getdata())

    biti = ""

    # Extragem ultimul bit din fiecare canal RGB
    for r, g, b in px:
        biti += str(r & 1)
        biti += str(g & 1)
        biti += str(b & 1)

    octeti = []

    # Grupam bitii cate 8
    for i in range(0, len(biti) - 7, 8):
        octet = biti[i:i + 8]
        valoare = int(octet, 2)

        # Ne oprim la octetul 0
        if valoare == 0:
            break

        octeti.append(valoare)

    # Transformam octetii in text
    mesaj = bytes(octeti).decode("utf-8")

    print("Mesajul ascuns este:", mesaj)


dezvaluie_mesaj("stego.png")