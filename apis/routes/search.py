from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from apis.dependencies.auth import optional_user
from business.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])

class SearchQuery(BaseModel):
    text: str
    context: Optional[str] = None

search_service = SearchService()

@router.post("/query")
async def search_query(
    query: SearchQuery,
    user_id: Optional[str] = Depends(optional_user)
):
    try:
        return await search_service.process_query(text=query.text, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/commands")
async def get_search_commands():
    return {"commands": search_service.get_supported_commands()}
