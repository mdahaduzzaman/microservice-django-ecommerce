from rest_framework import views
from rest_framework.response import Response
from rest_framework.request import Request

from accounts.keycloak import KeycloakClient


class UserRolesView(views.APIView):
    """
    GET: List all roles for a user
    POST: Add role to user
    """

    def get(self, request: Request, user_id: str):
        client = KeycloakClient()
        roles = client.get_user_roles(user_id)
        return Response(roles)

    def post(self, request: Request, user_id: str):
        role_names = request.data.get("roles", [])
        client = KeycloakClient()
        client.assign_realm_roles(user_id, *role_names)
        return Response({"status": "success"})

