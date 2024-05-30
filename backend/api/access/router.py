from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from . import schemas
from .service import AccessService, get_access_service


router = APIRouter(
    prefix="/access",
    tags=["access"],
)


@router.post("/signup", response_model=schemas.SignupResponse)
async def signup(
    signup_schema: schemas.SignupRequest,
    service: AccessService = Depends(get_access_service),
):
    user_schema = schemas.User(**signup_schema.model_dump())

    user = await service.create_user(
        schema=user_schema,
    )

    return user


@router.post("/login", response_model=schemas.LoginResponse)
async def login(
    schema: schemas.LoginRequest,
    Authorize: AuthJWT = Depends(),
    service: AccessService = Depends(get_access_service),
) -> tuple[str, str]:
    user = await service.login(
        email=schema.email,
        password=schema.password,
    )

    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_access_token(subject=user.email)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return schemas.LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=schemas.RefreshResponse)
async def refresh(
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_refresh_token_required()

    user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=user)

    Authorize.set_access_cookies(access_token)

    return schemas.RefreshResponse(
        access_token=access_token,
    )


@router.get("/logout")
async def logout(
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
