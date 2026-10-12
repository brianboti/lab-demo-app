import definitely_missing_module  # deliberate startup failure for the Lab Deploy failure exercise
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index():
    return {"message": "Lab deployment is running", "version": "0.1.0"}

