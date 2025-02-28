from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .auth.authentication import Authentication, get_authentication
from ..config import server

router = APIRouter()


@router.post("/token", tags=["authorization"], include_in_schema=server.expose_gui_api)
async def login(login_form_data: OAuth2PasswordRequestForm = Depends(),
                auth: Authentication = Depends(get_authentication)):

    if not server.expose_gui_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden")

    try:
        token = await auth.login(login_form_data.username, login_form_data.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return token

