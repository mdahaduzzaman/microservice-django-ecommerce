import requests
from decouple import config

from vendors.models import Vendor, SubscriptionPlan


class PaymentServiceClient:
    def __init__(self):
        self.base_url = config("PAYMENT_SERVICE_URL", default="")

    def create_checkout_session(
        self,
        payment_method: str,
        quantity: int,
        plan: SubscriptionPlan,
        vendor: Vendor,
        success_url: str,
        cancel_url: str,
    ) -> dict:
        url = f"{self.base_url}/create-checkout-session/"
        data = {
            "payment_method": payment_method,
            "mode": "subscription",
            "line_items": [
                {
                    "name": f"{plan.name.capitalize()} Subscription",
                    "amount": (
                        plan.monthly_price if quantity == 1 else plan.yearly_price
                    ),
                    "quantity": quantity,
                }
            ],
            "currency": "usd",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "metadata": {
                "vendor_id": str(vendor.id),
                "plan_id": str(plan.id),
                "billing_cycle": "monthly" if quantity == 1 else "yearly",
            },
        }
        response = requests.post(url, json=data)
        print(f"Creating checkout session: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()
