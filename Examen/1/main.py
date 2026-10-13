from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

# Partea 1: apeluri pentru build_url și is_https
print("\nPartea 1: build_url")
print("build_url 1:", build_url("example.com", "login"))
print("build_url 2:", build_url("example.com", "/login"))

print("\nPartea 1: is_https")
print("is_https 1:", is_https("https://example.com"))
print("is_https 2:", is_https("http://example.com"))


# Partea 2: apeluri pentru show_response
print("\nPartea 2: show_response")
print("Test 1:")
show_response("https://example.com")

print("Test 2:")
show_response("https://httpbin.org/status/404")


# Partea 3: apeluri pentru check_site
print("\nPartea 3: check_site")
print("Site funcțional:", check_site("https://example.com"))
print(
    "Site inexistent:",
    check_site("http://this-site-does-not-exist.invalid"),
)


# Partea 4: apelul scan_sites()
print("\nPartea 4: scan_sites")
scan_sites()


# Partea 5: apeluri pentru check_headers
print("\nPartea 5: check_headers")
print("Site HTTPS:", check_headers("https://example.com"))
print(
    "Site inexistent:",
    check_headers("http://this-site-does-not-exist.invalid"),
)


# Partea 6: apeluri pentru retry_check
print("\nPartea 6: retry_check")
print(
    "Status 200:",
    retry_check("https://httpbin.org/status/200"),
)
print(
    "Status 404:",
    retry_check("https://httpbin.org/status/404"),
)
print(
    "Status 500:",
    retry_check("https://httpbin.org/status/500"),
)
print(
    "Site inexistent:",
    retry_check("http://this-site-does-not-exist.invalid"),
)