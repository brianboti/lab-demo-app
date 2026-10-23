import html
import itertools
import os
import platform
import threading

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

# The sentence the page shows in large letters. Change it, merge, release: the page shows the new one as soon as the new
# version serves visitors. The tests read it from here, so any wording passes them.
MESSAGE = "Lab deployment is running"
VERSION = "0.2.0"

app = FastAPI()
# The bake trial's switch (platform 1.9.0 live exercise): with FAULT_EVERY=N in platform.yaml, every Nth request to "/"
# answers 500, so a release that passes its health checks can still fail its bake. Unset in normal operation.
FAULT_EVERY = int(os.environ.get("FAULT_EVERY") or 0)
_requests = itertools.count(1)
_lock = threading.Lock()

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fast Deploy demo</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; background: #f4f7f8; color: #10242f;
         font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
  main {{ text-align: center; padding: 48px 24px; max-width: 1100px; }}
  .eyebrow {{ font-size: 15px; letter-spacing: .14em; text-transform: uppercase; font-weight: 700; color: #087f78; margin: 0 0 24px; }}
  h1 {{ font-size: clamp(44px, 8vw, 104px); line-height: 1.05; letter-spacing: -.03em; margin: 0 0 32px; }}
  .meta {{ font-size: 16px; color: #5b6f7b; margin: 0; }}
  .meta code {{ background: #e3ecef; padding: 3px 8px; border-radius: 6px; font-size: 15px; }}
</style>
</head>
<body>
<main>
  <p class="eyebrow">Fast Deploy &middot; live demo</p>
  <h1>{message}</h1>
  <p class="meta">Served by <code>{revision}</code> &middot; version {version} &middot; Python {python}</p>
</main>
</body>
</html>
"""


def planted_fault():
    if FAULT_EVERY:
        with _lock:
            number = next(_requests)
        if number % FAULT_EVERY == 0:
            raise HTTPException(status_code=500, detail="planted fault for the bake trial")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index():
    planted_fault()
    # K_REVISION is the Cloud Run revision serving this request; a new release has a new one, so the page shows which
    # version answered.
    return PAGE.format(message=html.escape(MESSAGE), revision=html.escape(os.environ.get("K_REVISION", "this computer")),
                       version=VERSION, python=platform.python_version())


@app.get("/api")
def api():
    return {"message": MESSAGE, "version": VERSION, "python": platform.python_version(), "revision": os.environ.get("K_REVISION")}
