from rest_framework import viewsets, status, views
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from payments.models import PaymentMethod
from payments.serializers import (
    PaymentMethodSerializer,
    CheckoutSessionSerializer,
    SessionResponseSerializer,
    StripeSessionRequestSerializer,
    StripeSessionStatusSerializer,
)
from payments.utils import get_checkout_session, stripe


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def get_queryset(self):
        return self.queryset.filter(is_active=True)


class CheckoutSessionView(views.APIView):
    serializer_class = CheckoutSessionSerializer

    @extend_schema(
        responses={201: SessionResponseSerializer},
    )
    def post(self, request):
        serializer = CheckoutSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            session = get_checkout_session(**data)
            return Response(session, status=status.HTTP_201_CREATED)
        except NotImplementedError as e:
            return Response({"error": str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)
        except Exception as e:
            return Response(
                {
                    "error": "Failed to create checkout session. Original error: "
                    + str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class StripeSessionView(views.APIView):
    serializer_class = StripeSessionRequestSerializer

    @extend_schema(
        responses={200: StripeSessionStatusSerializer},
    )
    def post(self, request):
        session_id = request.data.get("session_id")
        if not session_id:
            return Response(
                {"error": "Missing session_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            print(f"Retrieved Stripe session: {session}")

            response_data = {
                "id": session.id,
                "payment_status": session.payment_status,
                "customer_email": session.customer_email,
                "amount_total": session.amount_total,
            }

            return Response(response_data)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
