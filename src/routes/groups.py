"""HTTP routes for groups."""
from fastapi import APIRouter, Depends

from src.routes.deps import get_store, require_user
from src.services import groups

router = APIRouter(prefix="/api/groups")


@router.get("")
def my_groups(user=Depends(require_user), store=Depends(get_store)):
    return {"groups": groups.list_my_groups(store, user)}
