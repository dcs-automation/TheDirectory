#!/usr/bin/env python3
"""Simple server for TheDirectory: serves static files + notes/bookmarks API."""

import http.server
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_FILE = os.path.join(BASE_DIR, "notes.json")
BOOKMARKS_FILE = os.path.join(BASE_DIR, "bookmarks.json")

DEFAULT_BOOKMARKS = [
    {
        "name": "Frequently Visited",
        "links": [
            {"label": "Google", "url": "https://www.google.com"},
            {"label": "YouTube", "url": "https://www.youtube.com"},
            {"label": "GitHub", "url": "https://github.com"},
            {"label": "Reddit", "url": "https://www.reddit.com"},
            {"label": "Wikipedia", "url": "https://en.wikipedia.org"},
            {"label": "Twitter / X", "url": "https://x.com"},
        ]
    },
    {
        "name": "Productivity",
        "links": [
            {"label": "Gmail", "url": "https://mail.google.com"},
            {"label": "Google Drive", "url": "https://drive.google.com"},
            {"label": "Calendar", "url": "https://calendar.google.com"},
            {"label": "Notion", "url": "https://www.notion.so"},
        ]
    },
    {
        "name": "Entertainment",
        "links": [
            {"label": "Netflix", "url": "https://www.netflix.com"},
            {"label": "Spotify", "url": "https://open.spotify.com"},
            {"label": "Twitch", "url": "https://www.twitch.tv"},
        ]
    }
]


def load_json(filepath, default):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/notes":
            self._json_response(load_json(NOTES_FILE, {"content": ""}))
        elif self.path == "/api/bookmarks":
            self._json_response(load_json(BOOKMARKS_FILE, DEFAULT_BOOKMARKS))
        else:
            super().do_GET()

    def do_PUT(self):
        body = self._read_body()
        if body is None:
            return
        if self.path == "/api/notes":
            save_json(NOTES_FILE, {"content": body.get("content", "")})
            self._json_response({"ok": True})
        elif self.path == "/api/bookmarks":
            if not isinstance(body, list):
                self._error_response(400, "expected array")
                return
            save_json(BOOKMARKS_FILE, body)
            self._json_response({"ok": True})
        else:
            self._error_response(404, "not found")

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            self._error_response(400, "invalid json")
            return None

    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _error_response(self, status, message):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())


if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", 8080), Handler)
    print("Serving on http://0.0.0.0:8080")
    server.serve_forever()
