#!/usr/bin/env python3
"""Simple server for TheDirectory: serves static files + notes API."""

import http.server
import json
import os

NOTES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.json")


def load_notes():
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"content": ""}


def save_notes(data):
    with open(NOTES_FILE, "w") as f:
        json.dump(data, f)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/notes":
            notes = load_notes()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(notes).encode())
        else:
            super().do_GET()

    def do_PUT(self):
        if self.path == "/api/notes":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                save_notes({"content": data.get("content", "")})
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"invalid json"}')
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", 8080), Handler)
    print("Serving on http://0.0.0.0:8080")
    server.serve_forever()
