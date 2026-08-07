from fastapi import Request
from fastapi import HTTPException
from fastapi import Security
from fastapi import Depends
from fastapi import status
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from backend.platform.auth.application.current_user_service import CurrentUserService
from backend.platform.auth.application.jwt_service import JWTService
from backend.platform.auth.domain.user import User
from backend.api.dependencies.container import get_container


bearer_scheme = HTTPBearer()

def get_current_user_service(
    request: Request,
) -> CurrentUserService:
    """
    Returns the current user application service.
    """

    container = get_container(request)

    return container.current_user_service()


def get_jwt_service(
    request: Request,
) -> JWTService:
    """
    Returns the JWT application service.
    """

    container = get_container(request)

    return container.jwt_service()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(
        bearer_scheme,
    ),
    jwt_service: JWTService = Depends(
        get_jwt_service,
    ),
    current_user_service: CurrentUserService = Depends(
        get_current_user_service,
    ),
) -> User:

    print("TOKEN:", credentials.credentials)

    try:
        user_id = jwt_service.verify_access_token(
            credentials.credentials,
        )

        print("USER ID FROM JWT:", user_id)

        user = current_user_service.get_current_user(
            user_id,
        )

        print("USER:", user)

        return user

    except Exception as exc:
        print(type(exc))
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
        ) from exc