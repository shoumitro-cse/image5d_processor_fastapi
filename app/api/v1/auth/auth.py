from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from app.schemas.auth_schema import LoginRequest
from app.services.auth_service import auth_service  # Import AuthService

router = APIRouter(prefix="", tags=["Authentication"])

# Sample in-memory user database
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": auth_service.hash_password("testpassword")
    }
}


@router.post("/token")
async def login_access_token(form_data: LoginRequest):
    """
    Authenticates a user and returns a JWT token.

    payload:

      `
        {
          "username": "testuser",
          "password": "testpassword"
        }
      `
    """
    user = fake_users_db.get(form_data.username)
    if not user or not auth_service.verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(
        data={"sub": user["username"]}, expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}
