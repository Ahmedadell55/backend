# api/routes/analysis.py
from fastapi import APIRouter, HTTPException
from business.services.analysis_service import AnalysisService
from core.city_instance import get_city as get_city_instance

router = APIRouter(prefix="/analysis", tags=["Analysis"])

def get_analysis_service():
    try:
        city = get_city_instance()
        return AnalysisService(city)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/city")
async def city_analysis():
    try:
        service = get_analysis_service()
        return await service.analyze_full_city()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/simple")
async def simple_analysis():
    try:
        service = get_analysis_service()
        return await service.get_simple_stats()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
