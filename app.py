from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    # Trial scenario: a release whose candidate never becomes healthy must be rolled back automatically.
    raise RuntimeError("simulated unhealthy release")


@app.get("/")
def index():
    return {"message": "Lab deployment is running", "version": "0.1.0"}

