from rest_framework import viewsets, status, views
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from payments.models import PaymentMethod
from payments.serializers import (
    PaymentMethodSerializer,
    CheckoutSessionSerializer,
    SessionResponseSerializer,
)
from payments.utils import get_checkout_session


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
