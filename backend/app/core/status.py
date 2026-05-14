from fastapi import APIRouter, HTTPException, status


router = APIRouter()

@router.get("/secure-data")
def get_data():
  authorized = False
  if not authorized:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
  return {"data": "..."}