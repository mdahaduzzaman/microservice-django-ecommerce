import requests
from django.conf import settings


class VendorServiceClient:
    def __init__(self):
        self.BASE_URL = settings.VENDOR_SERVICE_URL

    def get_vendor(self, user_id: str):
        url = f"{self.BASE_URL}/vendors/me/"
        headers = {"X-User-ID": user_id}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        return response.json()


class InventoryServiceClient:
    def __init__(self):
        self.base_url = settings.INVENTORY_SERVICE_URL

    def create_product_inventory(self, product_id, quantity):
        url = f"{self.base_url}/inventory/"
        data = {"product_id": product_id, "quantity": quantity}
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            response.raise_for_status()

    def get_product_inventory(self, product_id):
        url = f"{self.base_url}/inventory/{product_id}/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def update_product_inventory(self, product_id, quantity):
        url = f"{self.base_url}/inventory/{product_id}/"
        data = {"quantity": quantity}
        response = requests.put(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def delete_product_inventory(self, product_id):
        url = f"{self.base_url}/inventory/{product_id}/"
        response = requests.delete(url)
        if response.status_code == 204:
            return True
        else:
            response.raise_for_status()
