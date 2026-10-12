import os

if os.environ.get("K_SERVICE"):  # only inside Cloud Run, so unit tests pass and the candidate dies at startup
    raise RuntimeError("deliberate startup crash for the Lab Deploy failure exercise")

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index():
    return {"message": "Lab deployment is running", "version": "0.1.0"}

