from fastapi import APIRouter, HTTPException, Query
from app.services.external_client import ExternalClient

router = APIRouter(prefix="/external-data", tags=["external"])

@router.get("")
async def get_external_data():
    client = ExternalClient()
    try:
        data = await client.get("/posts")
        return {"count": len(data), "items": data[:50]}
    except Exception:
        raise HTTPException(status_code=502, detail="Error consultando API pública")

@router.post("/filter")
async def filter_external_data(limit: int = Query(10, ge=1, le=50)):
    client = ExternalClient()
    try:
        data = await client.get("/posts")
        items = sorted(data, key=lambda d: len(d.get("title", "")), reverse=True)[:limit]
        return {"count": len(items), "items": items}
    except Exception:
        raise HTTPException(status_code=502, detail="Error filtrando datos externos")
