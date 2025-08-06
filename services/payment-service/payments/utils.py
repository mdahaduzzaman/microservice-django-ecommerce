import stripe
from decouple import config
import logging

from payments.models import PaymentMethod

logger = logging.getLogger(__name__)

stripe.api_key = config("STRIPE_SECRET_KEY")
stripe.api_version = "2025-04-30.basil"


def get_checkout_session(payment_method: PaymentMethod, *args, **kwargs) -> dict:
    if payment_method.name == "stripe":
        return create_stripe_checkout_session(*args, **kwargs)
    else:
        raise NotImplementedError(
            f"Payment method {payment_method.name} is not implemented."
        )


def create_stripe_checkout_session(
    mode: str,
    currency: str,
    success_url: str,
    cancel_url: str,
    metadata: dict,
    line_items: list,
) -> dict:
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": currency,
                    "product_data": {
                        "name": item["name"],
                        **(
                            {"description": item["description"]}
                            if "description" in item
                            else {}
                        ),
                    },
                    "unit_amount": int(item["amount"] * 100),  # in cents
                },
                "quantity": item["quantity"],
            }
            for item in line_items
        ],
        metadata=metadata,
        mode=mode,
        success_url=f"{success_url}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=cancel_url,
        # Enable tax collection if supported
        automatic_tax={
            "enabled": False,  # Set to True if you want Stripe to calculate taxes
        },
    )

    logger.info(
        f"Stripe checkout session created: {checkout_session.id} for mode: {mode}, currency: {currency}"
    )

    return {
        "session_id": checkout_session.id,
        "checkout_url": checkout_session.url,
    }
