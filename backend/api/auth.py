from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.schema import User as UserModel
from schemas import User, UserCreate, Token, TokenData
import security
from security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
# from database import get_db  # We'll add this when database is ready

router = APIRouter()

# Temporary in-memory user storage (replace with database later)
fake_users_db = {}

@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # Check if user already exists
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and create new user
    hashed_password = get_password_hash(user.password)
    user_id = len(fake_users_db) + 1
    fake_users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_password
    }
    
    return User(id=user_id, email=user.email)

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find user by email
    user_data = fake_users_db.get(form_data.username)

    # Check if user exists and password is correct
    if not user_data or not verify_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create and return access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# This scheme will look for a Bearer token in the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function to get the current authenticated user from a JWT token.
    For now, uses the in-memory fake_users_db, but will be updated to use database later.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    # For now, use fake_users_db (will be replaced with database query later)
    user_data = fake_users_db.get(token_data.email)
    if user_data is None:
        raise credentials_exception
    
    return User(id=user_data["id"], email=user_data["email"])


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user's profile.
    This is a protected endpoint that requires a valid Bearer token.
    """
    return current_user
