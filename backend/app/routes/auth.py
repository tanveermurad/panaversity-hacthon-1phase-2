"""
Authentication API routes for user signup and signin.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db import get_session
from app.models import User
from app.schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from app.middleware import hash_password, verify_password, create_access_token, verify_token


router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.

    Creates a new user with hashed password and returns JWT token.

    Args:
        user_data: User registration data (email, password, name)
        session: Database session

    Returns:
        TokenResponse with user info and JWT token

    Raises:
        409: Email already exists
        400: Invalid input data
    """
    # Check if email already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    password_hash = hash_password(user_data.password)

    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=password_hash,
        name=user_data.name
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate JWT token
    token = create_access_token(
        user_id=str(new_user.id),
        email=new_user.email
    )

    # Return user and token
    user_response = UserResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        created_at=new_user.created_at
    )

    return TokenResponse(user=user_response, token=token)


@router.post("/signin", response_model=TokenResponse)
async def signin(
    login_data: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token.

    Verifies credentials and issues JWT token for API access.

    Args:
        login_data: User login credentials (email, password)
        session: Database session

    Returns:
        TokenResponse with user info and JWT token

    Raises:
        401: Invalid credentials
    """
    # Find user by email
    statement = select(User).where(User.email == login_data.email)
    user = session.exec(statement).first()

    # Verify user exists and password is correct
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = create_access_token(
        user_id=str(user.id),
        email=user.email
    )

    # Return user and token
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at
    )

    return TokenResponse(user=user_response, token=token)


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Get current authenticated user information.

    Args:
        user_id: Authenticated user ID from JWT token
        session: Database session

    Returns:
        UserResponse with user information

    Raises:
        404: User not found
        401: Invalid token
    """
    from uuid import UUID

    # Get user from database
    statement = select(User).where(User.id == UUID(user_id))
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at
    )
