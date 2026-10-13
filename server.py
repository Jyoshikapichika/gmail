#!/usr/bin/env python3
"""
Gmail-Style NPTEL Email Demo — Local Backend Server (Educational UI Project)

Provides:
- Static file serving for index.html, styles.css, app.js, and NOC26CS93S370700875.pdf
- GET /api/download-hallticket : Serves the unmodified uploaded PDF with Content-Disposition attachment header
- GET /api/health              : Verifies that NOC26CS93S370700875.pdf is present and returns file metadata
"""

import json
import os
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FILENAME = "NOC26CS93S370700875.pdf"
PDF_FILEPATH = os.path.join(PROJECT_DIR, PDF_FILENAME)
PORT = int(os.environ.get("PORT", "8000"))


class DemoEmailRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_DIR, **kwargs)

    def handle(self):
        try:
            super().handle()
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass

    def do_HEAD(self):
        parsed_path = urlparse(self.path).path
        if parsed_path == "/favicon.ico":
            self.path = "/gmail-icon-192.png"
        elif parsed_path == "/api/download-hallticket":
            if not os.path.isfile(PDF_FILEPATH):
                self.send_response(404)
                self.end_headers()
                return
            file_size = os.path.getsize(PDF_FILEPATH)
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header(
                "Content-Disposition", f'attachment; filename="{PDF_FILENAME}"'
            )
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            return
        return super().do_HEAD()

    def do_GET(self):
        parsed_path = urlparse(self.path).path

        if parsed_path == "/favicon.ico":
            self.path = "/gmail-icon-192.png"
            return super().do_GET()

        if parsed_path == "/api/health":
            exists = os.path.isfile(PDF_FILEPATH)
            size = os.path.getsize(PDF_FILEPATH) if exists else 0
            payload = {
                "status": "ok",
                "demoMode": True,
                "pdfFilename": PDF_FILENAME,
                "pdfExists": exists,
                "pdfSizeBytes": size,
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                self.wfile.write(body)
            except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                pass
            return

        if parsed_path == "/api/download-hallticket":
            if not os.path.isfile(PDF_FILEPATH):
                err = json.dumps({
                    "error": f"Hall Ticket PDF ({PDF_FILENAME}) not found in {PROJECT_DIR}"
                }).encode("utf-8")
                self.send_response(404)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(err)))
                self.end_headers()
                try:
                    self.wfile.write(err)
                except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                    pass
                return

            file_size = os.path.getsize(PDF_FILEPATH)
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header(
                "Content-Disposition", f'attachment; filename="{PDF_FILENAME}"'
            )
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            try:
                with open(PDF_FILEPATH, "rb") as f:
                    while chunk := f.read(65536):
                        self.wfile.write(chunk)
            except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                pass
            return

        try:
            return super().do_GET()
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass


def get_lan_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    lan_ip = get_lan_ip()
    server = ThreadingHTTPServer(("0.0.0.0", PORT), DemoEmailRequestHandler)
    print("=" * 68)
    print(" Gmail-Style NPTEL Email Demo Server (Educational UI Project)")
    print("=" * 68)
    print(f" Local Desktop URL : http://localhost:{PORT}")
    print(f" Android / LAN URL : http://{lan_ip}:{PORT}")
    print(f" Hall Ticket PDF   : {PDF_FILEPATH} (Exists: {os.path.isfile(PDF_FILEPATH)})")
    print("=" * 68)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down demo server...")
        server.server_close()
