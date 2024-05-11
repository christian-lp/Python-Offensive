#!/usr/bin/env python3

from mitmproxy import http

def response(packet):

    content_type = packet.response.headers.get("content_type", "")

    try:
        if "image" in content_type:
            url = packet.reqest.url
            estension = content_type.split("/")[-1]

            if etension == "jpeg":
                extension = "jpg"

            file_name = f"images/{url.replace('/', '_')}.extension"
            image_data = packet.response.content 

            with open(file_name, "wb") as f:
                f.write(image_data)

            print(f"[+] Imagen guardada: {file_name}")
    except:
        pass
