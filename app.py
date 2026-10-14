import platform

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index():
    return {"message": "Lab deployment is running", "version": "0.2.0", "python": platform.python_version()}
