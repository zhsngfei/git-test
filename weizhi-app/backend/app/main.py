from fastapi import FastAPI

from app.features.cities.router import router as cities_router
from app.features.places.router import router as places_router
from app.features.works.router import router as works_router

app = FastAPI(title="Weizhi API")
app.include_router(cities_router)
app.include_router(works_router)
app.include_router(places_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
