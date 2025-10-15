from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import devices, batteries, links
from .models import Base
from .database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Battery Monitor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(devices.router)
app.include_router(batteries.router)
app.include_router(links.router)

app.mount("/ui", StaticFiles(directory="app/static", html=True), name="ui")

@app.get("/")
def root():
    return {"service": "battery-monitor", "status": "ok"}
