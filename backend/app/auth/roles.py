from fastapi import HTTPException


def admin_required(user):

    if user["role"] != "Admin":

        raise HTTPException(
            status_code=403,
            detail="Admin Access Required"
        )

    return True


def receptionist_required(user):

    if user["role"] not in ["Admin", "Receptionist"]:

        raise HTTPException(
            status_code=403,
            detail="Permission Denied"
        )

    return True