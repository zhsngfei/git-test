from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.features.auth.router import router as auth_router
from app.features.cities.router import router as cities_router
from app.features.collections.router import router as collections_router
from app.features.places.router import router as places_router
from app.features.recommendations.router import router as recommendations_router
from app.features.works.router import router as works_router

app = FastAPI(title="Weizhi API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cities_router)
app.include_router(works_router)
app.include_router(places_router)
app.include_router(collections_router)
app.include_router(recommendations_router)
app.include_router(auth_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "appEnv": settings.app_env}


@app.get("/health/readiness")
def readiness() -> dict[str, object]:
    return {
        "status": "ok",
        "appEnv": settings.app_env,
        "services": {
            "supabaseAuth": settings.supabase_auth_status(),
            "supabaseCollections": settings.supabase_collections_storage(),
            "mimoai": settings.mimoai_status(),
        },
    }
