from rest_framework.response import Response
from rest_framework import views
from decouple import config


class HealthCheckView(views.APIView):
    """
    View to check the health of the service.
    """

    def get(self, request):
        """
        Returns a simple health check response.
        """
        return Response(
            {
                "status": "running",
                "service": config("SERVICE_NAME", default="user-service"),
                "port": config("SERVICE_PORT", cast=int),
            }
        )
