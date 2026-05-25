from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.schemas.intelligence_schema import FirePredictionRequest, FireDataResponse
from app.controllers.intelligence_controller import query_intelligence_controller
from app.core.database import get_db
from app.core.security import get_current_user_from_cookie

intelligence_router = APIRouter()

@intelligence_router.post(
    "/predict", 
    status_code=status.HTTP_200_OK, 
    response_model=FireDataResponse  
)
def get_wildfire_prediction(
    prediction_request: FirePredictionRequest, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_cookie)
):
    return query_intelligence_controller(
        user_id=current_user.id, 
        prediction_request=prediction_request, 
        db=db
    )