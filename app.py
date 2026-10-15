import itertools
import os
import platform
import threading

from fastapi import FastAPI, HTTPException

app = FastAPI()
# The bake trial's switch (platform 1.9.0 live exercise): with FAULT_EVERY=N in platform.yaml, every Nth request to "/"
# answers 500, so a release that passes its health checks can still fail its bake. Unset in normal operation.
FAULT_EVERY = int(os.environ.get("FAULT_EVERY") or 0)
_requests = itertools.count(1)
_lock = threading.Lock()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index():
    if FAULT_EVERY:
        with _lock:
            number = next(_requests)
        if number % FAULT_EVERY == 0:
            raise HTTPException(status_code=500, detail="planted fault for the bake trial")
    return {"message": "Lab deployment is running", "version": "0.2.0", "python": platform.python_version()}
