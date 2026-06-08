from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import indicators, health

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Economic Indicators API",
    description="REST API for macroeconomic data — inflation, interest rates, employment, and GDP.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(indicators.router, prefix="/api/v1", tags=["Indicators"])
