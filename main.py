import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from core import settings
from core import init_city, get_city
from core import SmartCityException
from data.supabase_client import init_supabase

from apis.routes import auth, nodes, edges, paths, analysis, projects, fleet, parking, search

app = FastAPI(
    title="Darb SmartCity API",
    version="1.0.0",
    description="Smart City API - Darb AI Powered System"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler
@app.exception_handler(SmartCityException)
async def smart_city_exception_handler(request: Request, exc: SmartCityException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.message, "code": exc.code}
    )

# Routers
for router in [auth.router, nodes.router, edges.router, paths.router,
               analysis.router, projects.router, fleet.router, parking.router, search.router]:
    app.include_router(router)

# Startup
@app.on_event("startup")
async def startup():
    settings.ensure_directories()
    init_city()
    try:
        init_supabase()
    except Exception as e:
        print(f"⚠️ Supabase warning: {e}")

# Endpoints
@app.get("/")
async def root():
    return {"message": "Darb SmartCity API 🚀", "docs": "/docs", "health": "/health"}

@app.get("/health")
async def health():
    city = get_city()
    return {"status": "ok", "nodes": len(city.nodes), "edges": len(city.edges)}

@app.get("/api/info")
async def info():
    city = get_city()
    return {"app": "Darb SmartCity API", "version": "1.0.0", "nodes": len(city.nodes), "edges": len(city.edges)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=False)
