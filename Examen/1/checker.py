import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    return f"https://{host.rstrip('/')}/{path.lstrip('/')}"



def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")



def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    except requests.RequestException as error:
        print(f"Error: {str(error)[:150]}")


def check_site(url):
    try:
        response = requests.get(url, timeout=5)

        return {
            "status": response.status_code,
            "content_type": response.headers,
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }

    except requests.RequestException as error:
        return {
            "status": None,
            "error": "A aparut o problema",
        }



def scan_sites():
    
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    """Verifică site-urile, afișează răspunsurile 200 și un rezumat."""
    results = []

    for url in SITES:
        result = check_site(url)
        results.append((url, result))

    successful = [
        (url, result)
        for url, result in results
        if result.get("status") == 200
    ]

    successful.sort(
        key=lambda item: item[1].get("length", 0),
        reverse=True,
    )

    for url, result in successful:
        print(
            f"{url} -> {result['status']}, "
            f"{result['length']} octeți"
        )

    failed_count = len(results) - len(successful)
    print(f"Reușite: {len(successful)} | Eșuate: {failed_count}")
    


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)

        # Antetele HTTP nu țin cont de majuscule/minuscule.
        response_headers = {
            name.lower(): value
            for name, value in response.headers.items()
        }

        present = [
            header
            for header in SECURITY_HEADERS
            if header.lower() in response_headers
        ]

        missing = [
            header
            for header in SECURITY_HEADERS
            if header.lower() not in response_headers
        ]

        score = (
            round(len(present) / len(SECURITY_HEADERS) * 100)
            if SECURITY_HEADERS
            else 100
        )

        return {
            "present": present,
            "missing": missing,
            "score": score,
        }

    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error)[:150],
        }

def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    attempts = max(0, int(attempts))
    last_status = None
    last_error = None
    actual_attempts = 0

    for _ in range(attempts):
        actual_attempts += 1

        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            last_error = None

            # Orice status sub 500 oprește reîncercările.
            if last_status < 500:
                return {
                    "status": last_status,
                    "attempts": actual_attempts,
                }

        except requests.RequestException as error:
            last_status = None
            last_error = str(error)[:150]

    result = {
        "status": last_status,
        "attempts": actual_attempts,
    }

    if last_error is not None:
        result["error"] = last_error

    return result