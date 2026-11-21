"""Запустити локальний CGI-сервер із каталогу лабораторної роботи."""

import argparse
from functools import partial
from http.server import CGIHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Локальний CGI-сервер")
    parser.add_argument("--port", type=int, default=8000)
    options = parser.parse_args()
    handler = partial(CGIHTTPRequestHandler, directory=Path(__file__).resolve().parent)
    with ThreadingHTTPServer(("127.0.0.1", options.port), handler) as server:
        print(f"http://127.0.0.1:{server.server_port}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
