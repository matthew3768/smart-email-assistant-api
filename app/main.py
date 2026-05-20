from fastapi import FastAPI

app = FastAPI(
    title="Smart Email Assistant API",
    description="An API for drafting, classifying, and automating email replies.",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"message": "Smart Email Assistant API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}