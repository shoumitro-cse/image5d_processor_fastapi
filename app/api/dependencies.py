from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
# from app.services.user_service import UserService
# from app.services.item_service import ItemService


# Database dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # User service dependency
# def get_user_service(db: Session = Depends(get_db)) -> UserService:
#     return UserService(db)
#
#
# # Item service dependency
# def get_item_service(db: Session = Depends(get_db)) -> ItemService:
#     return ItemService(db)


# example for endpoints
# router = APIRouter()
# @router.post("/", response_model=ItemResponse)
# async def create_item(item: ItemCreate, service: ItemService = Depends(get_item_service)):
#     return await service.create_item(item)
