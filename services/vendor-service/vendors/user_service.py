from uuid import UUID
import requests
from decouple import config


def assign_vendor_role(user_id: UUID) -> None:
    """
    Assigns the vendor role to a user based on their user ID.
    This function is typically called when a new vendor is created.
    """
    USER_SERVICE_URL = config("USER_SERVICE_URL", default="http://localhost:4000")
    url = f"{USER_SERVICE_URL}/users/{user_id}/roles"
    data = {"roles": ["vendor"]}
    res = requests.post(url, json=data)
    if res.status_code != 200:
        raise ValueError("Failed to assign vendor role.")
    print(f"Vendor role assigned to user {user_id}.")
