from fastapi import FastAPI

from app.features.cities.router import router as cities_router

app = FastAPI(title="Weizhi API")
app.include_router(cities_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
