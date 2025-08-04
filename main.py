import uuid
import time
import json
import gzip
import base64
import random
import os
import hashlib
import string
import curl_cffi
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAh6p66pVDFDfd+MRPa22g
jYhI//6XZKUbb/rRAzYgcyyzb73hBEqRMmCtDKNvIUe+qXI1xX1JHsSnT+Hi5wsu
fuW44RlFTlRuhM4entshgr+S8lAlLH914Sz5N2hLB9hgZmAMecQIhCOTjYG1t4NU
A8ggbVLKalBz83gsTup+U+6S+OGji5Cq2vbKVIHYKTZHqoQKNzCH6A6z0E+AoygB
yk1H98YHFoebpYoqVk0NCORBB+/ZLIa+guB83cS6sAL+SFYWxBcW9DwwzaJnFOIp
pNq0WgL3ggAt97CuGBMbuET0sEtxCfYPFnD/BL9QnQJONbuUUPBvfpLSkFJZhyy3
kQIDAQAB
-----END PUBLIC KEY-----"""

def encrypt_payload(json_str: str):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    ct = cipher.encrypt(json_str.encode())
    return base64.b64encode(ct).decode()

def generate_challenge():
    salt_length = random.randint(8, 11)
    raw_salt = os.urandom(salt_length)
    return {
        "salt": base64.b64encode(raw_salt).decode(),
        "prefix": base64.b64encode(hashlib.sha256(raw_salt).digest()).decode(),
        "config": {
            "difficulty": random.randint(5, 6),
            "salt_length": salt_length,
            "iterations": random.randint(1, 2)
        }
    }

def solve_pow(prefix: str, difficulty: int, max_iter: int = 5_000_000):
    alphabet = string.ascii_letters + string.digits
    target = "0" * difficulty
    for _ in range(max_iter):
        nonce = "".join(random.choices(alphabet, k=8))
        h = hashlib.sha256((prefix + nonce).encode()).hexdigest()
        if h.startswith(target):
            return {
                "nonce": nonce,
                "hash": h
            }
    raise RuntimeError("PoW challenge timeout")

def cookie():
    st = time.time()
    chal = generate_challenge()
    chal["createdAt"] = int(time.time() * 1000)
    chal_json = json.dumps(chal, separators=(",", ":"))
    encrypted_chal = encrypt_payload(chal_json)
    request_id = "".join(random.choices(string.ascii_letters + string.digits, k=8)) + str(int(time.time() * 1000))
    print(f"Challenge: {chal}")
    sol_payload = solve_pow(chal["prefix"], chal["config"]["difficulty"])
    sol_obj = {
        "nonce": sol_payload["nonce"],
        "hash": sol_payload["hash"],
        "requestId": request_id
    }
    sol_json = json.dumps(sol_obj, separators=(",", ":"))
    encrypted_sol = encrypt_payload(sol_json)
    #print(f"Encrypted Solution: {encrypted_sol}")
    bp = f"{encrypted_chal}|{encrypted_sol}"
    print(f"bp: {encrypted_chal[:20]}|{encrypted_sol[:20]} elapsed={time.time() - st:.1f}s.")
    return bp

payload = {
    "fingerprint": str(uuid.uuid4()),
    "webglRenderer": "ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0), or similar",
    "browserData": {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
        "language": "ja",
        "platform": "Win32",
        "plugins": [
            "PDF Viewer",
            "Chrome PDF Viewer",
            "Chromium PDF Viewer",
            "Microsoft Edge PDF Viewer",
            "WebKit built-in PDF"
        ],
        "screen": {
            "width": 1920,
            "height": 1080,
            "colorDepth": 24
        },
        "timezone": "Asia/Tokyo"
    },
    "expiry": int((time.time() + 3600) * 1000)
}
s = curl_cffi.Session(impersonate="chrome131")
s.cookies.update({
    "__bp": cookie()
})
r = s.get(
    "https://www.cybertemp.xyz/api/getMail?email=k6au6zi1@uzzp.flipkartoffer.in",
    headers={
        "x-client-meta": base64.b64encode(gzip.compress(json.dumps(payload).encode('utf-8'))).decode('utf-8'),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0',
        'Accept': '*/*',
        'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
        'Referer': 'https://www.cybertemp.xyz/',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=4',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
).text
print(r)
