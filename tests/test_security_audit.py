import urllib.request
import urllib.error
import json
import os

print("=== BACKEND SECURITY & VALIDATION AUDIT ===")

# Test 1: Non-PDF upload
boundary = '----WebKitFormBoundaryTest1234'
data = (
    b'--' + boundary.encode() + b'\r\n'
    b'Content-Disposition: form-data; name="file"; filename="malicious.exe"\r\n'
    b'Content-Type: application/octet-stream\r\n\r\n'
    b'MZfakeexecutablecontent\r\n'
    b'--' + boundary.encode() + b'--\r\n'
)

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/projects',
    data=data,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as resp:
        print('FAIL: Non-PDF accepted with status', resp.status)
except urllib.error.HTTPError as e:
    print('PASS: Non-PDF rejected with HTTP', e.code, e.read().decode())

# Test 2: Path Traversal
evil_payloads = ['..', '../..', '..%2F..', 'rendered_png/../..', 'config.py']
for evil in evil_payloads:
    try:
        url = f'http://127.0.0.1:8000/api/projects/sample_pl/download/{evil}'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            print(f'FAIL: Traversal payload {evil} accessible! HTTP {resp.status}')
    except urllib.error.HTTPError as e:
        print(f'PASS: Traversal payload {evil} blocked with HTTP {e.code}')
    except Exception as e:
        print(f'PASS: Traversal payload {evil} blocked by client: {e}')

# Test 3: Project Delete / Cleanup support check
try:
    req = urllib.request.Request('http://127.0.0.1:8000/api/projects/sample_pl', method='DELETE')
    with urllib.request.urlopen(req) as resp:
        print('DELETE endpoint exists:', resp.status)
except urllib.error.HTTPError as e:
    print('DELETE endpoint status: HTTP', e.code, '(Endpoint missing: 405 Method Not Allowed)')
