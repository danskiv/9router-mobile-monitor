#!/usr/bin/env python3
"""
9Router Mobile Monitor Micro-Server
Serves the mobile-first dashboard and proxies API requests (including SSE stream) to 9Router on port 20128.
Standard library only - zero external dependencies.
"""

import sys
import os
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get("PORT", 20130))
HOST = os.environ.get("HOST", "0.0.0.0")
NINE_ROUTER_BASE = os.environ.get("NINE_ROUTER_URL", "http://127.0.0.1:20128")
DOC_ROOT = os.path.dirname(os.path.abspath(__file__))

class ProxyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOC_ROOT, **kwargs)

    def do_GET(self):
        # 1. Real-time SSE Stream proxying
        if self.path.startswith("/api/usage/stream"):
            target_url = f"{NINE_ROUTER_BASE}{self.path}"
            try:
                req = urllib.request.Request(target_url)
                for header in ["Accept", "User-Agent"]:
                    if header in self.headers:
                        req.add_header(header, self.headers[header])
                
                with urllib.request.urlopen(req, timeout=3600) as resp:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.send_header("Cache-Control", "no-cache")
                    self.send_header("Connection", "keep-alive")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    while True:
                        line = resp.readline()
                        if not line:
                            break
                        self.wfile.write(line)
                        self.wfile.flush()
            except Exception:
                pass
            return

        # 2. General /api/* REST proxying (e.g. /api/usage/stats, /api/providers, /api/provider-nodes)
        if self.path.startswith("/api/"):
            target_url = f"{NINE_ROUTER_BASE}{self.path}"
            try:
                req = urllib.request.Request(target_url)
                for header in ["Accept", "User-Agent"]:
                    if header in self.headers:
                        req.add_header(header, self.headers[header])
                
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()
                    self.send_response(resp.status)
                    self.send_header("Content-Type", resp.headers.get("Content-Type", "application/json"))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(f'{{"error":"Gateway proxy error","detail":"{str(e)}"}}'.encode())
            return

        # 3. Default static file serving
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
            
        super().do_GET()

    def end_headers(self):
        # Cache control for fresh live metrics
        if self.path.endswith(".html") or self.path.startswith("/api/"):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

def run():
    server_address = (HOST, PORT)
    httpd = ThreadingHTTPServer(server_address, ProxyHandler)
    print(f"⚔️ 9Router Mobile Monitor Server listening on http://{HOST}:{PORT}")
    print(f"⚔️ Proxying 9Router API & SSE from {NINE_ROUTER_BASE}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⚔️ Server stopped by user.")
        httpd.server_close()

if __name__ == "__main__":
    run()
