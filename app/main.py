from fastapi import FastAPI
from app.api.routers.external import router as external_router
from app.api.routers.leads import router as leads_router



app = FastAPI(title="Tech Test API", version="0.1.0")

@app.get("/")
def health():
    return {"status": "ok"}


app.include_router(external_router)
app.include_router(leads_router)
