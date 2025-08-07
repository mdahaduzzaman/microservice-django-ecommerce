import stripe
from decouple import config
import logging

from payments.models import PaymentMethod, SubscriptionPlan

logger = logging.getLogger(__name__)

stripe.api_key = config("STRIPE_SECRET_KEY")
stripe.api_version = "2025-04-30.basil"


def get_checkout_session(payment_method: PaymentMethod, *args, **kwargs) -> dict:
    logger.info(f"checkout_session:create {payment_method.name} {args} {kwargs}")
    if payment_method.name == "stripe":
        return create_stripe_checkout_session(
            payment_method=payment_method, *args, **kwargs
        )
    else:
        raise NotImplementedError(
            f"Payment method {payment_method.name} is not implemented."
        )


def create_stripe_checkout_session(
    payment_method: PaymentMethod,
    mode: str,
    interval: str,
    currency: str,
    success_url: str,
    cancel_url: str,
    metadata: dict,
    line_items: list,
) -> dict:

    final_line_items = []
    if mode == "subscription":
        # 1. Create or retrieve subscription plans as we need the price IDs for Stripe
        for item in line_items:
            amount = item["amount"]
            name: str = item["name"]
            description = item.get(
                "description",
                f"{name.capitalize()} {interval.capitalize()} Subscription",
            )
            plan, created = SubscriptionPlan.objects.get_or_create(
                payment_method=payment_method,
                name=name,
                interval=interval,
                defaults={
                    "monthly_price": amount if interval == "monthly" else 0,
                    "yearly_price": amount if interval == "yearly" else 0,
                    "description": description,
                },
            )
            if created:
                product = stripe.Product.create(
                    name=plan.name,
                    description=description,
                    metadata={
                        "plan_id_from_payment_service": str(plan.id),
                    },
                )

                print(f"Created new subscription plan: {plan.name} with ID: {plan.id}")

                # 2. Create a recurring price (e.g., every 30 days)
                price = stripe.Price.create(
                    unit_amount=int(
                        plan.monthly_price * 100
                        if interval == "monthly"
                        else plan.yearly_price * 100
                    ),  # amount in cents
                    currency="usd",
                    recurring={"interval": "year" if interval == "yearly" else "month"},
                    product=product.id,
                    metadata={"plan_id_from_payment_service": str(plan.id)},
                )

                # update the plan with the new price ID
                plan.monthly_price_id = (
                    price.id if interval == "monthly" else plan.monthly_price_id
                )
                plan.yearly_price_id = (
                    price.id if interval == "yearly" else plan.yearly_price_id
                )
                plan.save()
                print(f"Created new price for plan: {plan.name} with ID: {price.id}")
            else:
                price = stripe.Price.retrieve(
                    plan.monthly_price_id
                    if interval == "monthly"
                    else plan.yearly_price_id
                )

            final_line_items.append(
                {
                    "price": price.id,
                    "quantity": item["quantity"],
                }
            )
    else:
        for item in line_items:
            final_line_items.append(
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
            )

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=final_line_items,
        metadata=metadata,
        mode=mode,
        success_url=f"{success_url}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{cancel_url}?session_id={{CHECKOUT_SESSION_ID}}",
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
