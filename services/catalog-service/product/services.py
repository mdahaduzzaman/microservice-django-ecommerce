import requests
from django.conf import settings


class VendorService:
    BASE_URL = settings.VENDOR_SERVICE_URL

    @staticmethod
    def get_vendor_by_user_id(user_id: str):
        try:
            response = requests.get(
                f"{VendorService.BASE_URL}/vendors/me/", timeout=3,
                headers={"X-User-ID": user_id}
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
