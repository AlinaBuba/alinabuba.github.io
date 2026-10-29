#!/usr/bin/env python3
"""Screenshots (desktop 1280, phone 390; light and dark) into shots/. Uses CHROME env or google-chrome."""
import functools, http.server, os, pathlib, shutil, subprocess, threading

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME") or shutil.which("google-chrome") or shutil.which("chromium")
PAGES = ["", "about/", "specializations/", "services/", "faq/", "contacts/", "privacy/", "en/", "en/about/"]
SIZES = {"desktop": (1280, 2600), "phone": (390, 4200)}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve(extra=None):
    """Start a local server on a free port; `extra` maps virtual paths to HTML strings."""
    extra = extra or {}

    class H(Quiet):
        def do_GET(self):
            if self.path in extra:
                body = extra[self.path].encode()
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
            else:
                super().do_GET()

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(H, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def chrome(*args):
    return subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", *args],
                          capture_output=True, text=True, check=True)


if __name__ == "__main__":
    out = ROOT / "shots"
    out.mkdir(exist_ok=True)
    srv, base = serve()
    for page in PAGES:
        for size, (w, h) in SIZES.items():
            for theme in ("light", "dark"):
                name = (page.strip("/").replace("/", "-") or "home") + f"-{size}-{theme}.png"
                chrome(f"--screenshot={out / name}", f"--window-size={w},{h}", "--force-device-scale-factor=1",
                       f"--blink-settings=preferredColorScheme={0 if theme == 'dark' else 1}", "--virtual-time-budget=2000", f"{base}/{page}")
    print("screenshots in", out)
    srv.shutdown()
