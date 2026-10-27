
import base64
import hashlib
import hmac
import json
import struct
import time
import urllib.error
import urllib.request

API_URL = (
    "https://api.challenge.hennge.com/"
    "challenges/backend-recursion/004"
)


def generate_totp(email):
    secret = (email + "HENNGECHALLENGE004").encode("ascii")
    counter = int(time.time()) // 30

    digest = hmac.new(
        secret,
        struct.pack(">Q", counter),
        hashlib.sha512
    ).digest()

    offset = digest[-1] & 0x0F
    code = struct.unpack(
        ">I", digest[offset:offset + 4]
    )[0] & 0x7FFFFFFF

    return f"{code % 10**10:010d}"


def main():
    with open("answer.json", encoding="utf-8") as file:
        payload = json.load(file)

    email = payload["contact_email"]

    if payload.get("solution_language") != "python":
        raise ValueError("solution_language must be python")

    credentials = f"{email}:{generate_totp(email)}"
    auth = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("ascii")

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print("Status:", response.status)
            print(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        print("Status:", error.code)
        print(error.read().decode("utf-8"))

    except urllib.error.URLError as error:
        print("Connection error:", error.reason)


if __name__ == "__main__":
    main()
