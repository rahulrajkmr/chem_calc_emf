"""Start a local website so the browser can load the Python files.

Run:
    python3 run.py

Then open:
    http://localhost:8000
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 8000

print("Galvanic Cell calculator")
print("Open this address in your browser:")
print(f"http://localhost:{PORT}")
print("Press Ctrl+C to stop.")

server = ThreadingHTTPServer(("127.0.0.1", PORT), SimpleHTTPRequestHandler)
server.serve_forever()
