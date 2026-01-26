from fastapi import APIRouter, HTTPException, Depends, status, Header
from typing import List

# Import from the new generic module
import idempotency
from accounts import crud
from accounts.schemas import AccountCreate, AccountUpdate, AccountResponse
from auth import utils
from auth.schemas import User

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=List[AccountResponse])
def get_all_accounts(current_user: User = Depends(utils.get_current_user)):
    """Auth: Clerk, Manager"""
    accounts = crud.get_all_accounts()
    return accounts


@router.post("", status_code=200)
def create_account(
        account: AccountCreate,
        idempotency_id: str = Header(..., alias="Idempotency-Id"),
        current_user: User = Depends(utils.get_current_user)
):
    """
    Auth: Clerk, Manager
    Requires 'Idempotency-Id' header.
    """
    # 1. Generic Check (Reusable)
    cached_response = idempotency.get_idempotency_key(idempotency_id)
    if cached_response:
        return cached_response

    # 2. Specific Business Logic (Create Account)
    result = crud.create_account(account)

    # 3. Generic Save (Reusable)
    idempotency.save_idempotency_key(idempotency_id, result)

    return result


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: str, current_user: User = Depends(utils.get_current_user)):
    """Auth: Clerk, Manager"""
    account = crud.get_account_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{account_id}")
def update_account(account_id: str, account: AccountUpdate, current_user: User = Depends(utils.get_current_user)):
    """Auth: Clerk, Manager"""
    success = crud.update_account(account_id, account)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account updated successfully"}


@router.delete("/{account_id}")
def delete_account(account_id: str, current_user: User = Depends(utils.get_current_user)):
    """Auth: MANAGER ONLY"""
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )

    success = crud.delete_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}