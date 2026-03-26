"""
Auth Service - Authentication Router
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Body, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.models.models import User, RefreshToken
from auth_service.schemas.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
    VerifyTokenResponse,
)
from auth_service.services.jwt_service import (
    hash_password, verify_password, create_access_token,
    create_refresh_token, decode_token, get_token_expiry,
)
from auth_service.utils.dependencies import get_db, _jwt_from_cookie_or_bearer
from shared.config import get_settings
import structlog

logger = structlog.get_logger()
settings = get_settings()
router = APIRouter()


class RefreshTokenOptionalBody(BaseModel):
    """Body for refresh when not using HttpOnly cookie."""

    refresh_token: str | None = None


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user"""
    # Check if email exists
    result = await db.execute(select(User).where(User.email == request.email))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create user
    user = User(
        email=request.email,
        password_hash=hash_password(request.password),
        full_name=request.full_name,
        phone=request.phone,
        role="patient",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    logger.info("user_registered", user_id=str(user.id), email=user.email)

    # Create tokens
    access_token = create_access_token(str(user.id), user.email, user.role)
    refresh_token, refresh_hash = create_refresh_token()

    # Store refresh token
    token_record = RefreshToken(
        user_id=user.id,
        token_hash=refresh_hash,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(token_record)
    await db.commit()

    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    response = JSONResponse(status_code=status.HTTP_201_CREATED, content=payload)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return response


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Login with email and password"""
    # Get user
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Check if locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Account locked until {user.locked_until}",
        )

    # Check if active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    # Update login info
    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(
            failed_login_attempts=0,
            locked_until=None,
            last_login_at=datetime.utcnow(),
        )
    )

    # Create tokens
    access_token = create_access_token(str(user.id), user.email, user.role)
    refresh_token, refresh_hash = create_refresh_token()

    # Store refresh token
    token_record = RefreshToken(
        user_id=user.id,
        token_hash=refresh_hash,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(token_record)
    await db.commit()

    logger.info("user_logged_in", user_id=str(user.id))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    response: Response,
    db: AsyncSession = Depends(get_db),
    body: RefreshTokenOptionalBody = Body(default_factory=lambda: RefreshTokenOptionalBody()),
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token"),
):
    """Refresh access token using refresh token from body or HttpOnly cookie."""
    import hashlib

    raw_refresh = (body.refresh_token or "").strip() or refresh_token_cookie
    if not raw_refresh:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required",
        )

    token_hash = hashlib.sha256(raw_refresh.encode()).hexdigest()

    result = await db.execute(
        select(RefreshToken)
        .where(RefreshToken.token_hash == token_hash)
        .where(RefreshToken.is_revoked == False)
    )
    stored_token = result.scalar_one_or_none()

    if not stored_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if stored_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    # Get user
    result = await db.execute(select(User).where(User.id == stored_token.user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    # Revoke old token (rotation)
    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.id == stored_token.id)
        .values(is_revoked=True)
    )

    # Create new tokens
    access_token = create_access_token(str(user.id), user.email, user.role)
    new_refresh_token, new_refresh_hash = create_refresh_token()

    # Store new refresh token
    new_token_record = RefreshToken(
        user_id=user.id,
        token_hash=new_refresh_hash,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(new_token_record)
    await db.commit()

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/logout")
async def logout(
    response: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
):
    """Logout and revoke refresh token"""
    if refresh_token:
        import hashlib
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        await db.execute(
            update(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .values(is_revoked=True)
        )
        await db.commit()

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "Logged out successfully"}


@router.api_route("/verify", methods=["GET", "POST"])
async def verify_token(
    db: AsyncSession = Depends(get_db),
    access_token: Optional[str] = Cookie(None),
    authorization: Optional[str] = Header(None),
) -> VerifyTokenResponse:
    """Verify JWT from access_token cookie or Authorization: Bearer (service-to-service)."""
    token = _jwt_from_cookie_or_bearer(access_token, authorization)
    if not token:
        return VerifyTokenResponse(valid=False)

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        return VerifyTokenResponse(valid=False)

    # Verify user exists
    result = await db.execute(select(User).where(User.id == payload["sub"]))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        return VerifyTokenResponse(valid=False)

    return VerifyTokenResponse(
        valid=True,
        user_id=payload["sub"],
        email=payload["email"],
        role=payload["role"],
    )


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Send password reset email (stub - needs email service)"""
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    # Always return success to prevent email enumeration
    return {"message": "If email exists, reset instructions have been sent"}


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Reset password with token (stub)"""
    return {"message": "Password reset successful"}


@router.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth-service", "version": "1.0.0"}


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change password for logged in user"""
    if not verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password incorrect")

    await db.execute(
        update(User)
        .where(User.id == current_user.id)
        .values(password_hash=hash_password(request.new_password))
    )
    await db.commit()

    logger.info("password_changed", user_id=str(current_user.id))

    return {"message": "Password changed successfully"}
