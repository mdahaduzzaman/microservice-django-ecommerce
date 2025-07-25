import requests
from django.conf import settings


class KeycloakClient:
    def __init__(self):
        self.base_url = settings.KEYCLOAK_BASE_URL
        self.admin_client_id = settings.KEYCLOAK_ADMIN_CLIENT_ID
        self.admin_client_secret = settings.KEYCLOAK_ADMIN_CLIENT_SECRET
        self.realm = settings.KEYCLOAK_REALM

    def get_admin_token(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": self.admin_client_id,
            "client_secret": self.admin_client_secret,
        }
        url = f"{self.base_url}/realms/master/protocol/openid-connect/token"
        try:
            res = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            res.raise_for_status()
            return res.json()["access_token"]
        except requests.RequestException as e:
            print(f"Error fetching admin token: {e}")
            return None

    def get_user_info(self, user_id):
        token = self.get_admin_token()
        if not token:
            return None
        url = f"{self.base_url}/admin/realms/{self.realm}/users/{user_id}"
        try:
            res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            print(f"Error fetching user info: {e}")
            return None

    def get_realm_roles(self, token: str):
        url = f"{self.base_url}/admin/realms/{self.realm}/roles"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            res = requests.get(
                url,
                headers=headers,
            )
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            print(f"Error getting realm roles: {e}")
            return []

    def get_user_roles(self, user_id):
        token = self.get_admin_token()
        url = f"{self.base_url}/admin/realms/{self.realm}/users/{user_id}/role-mappings"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            return res.json()["realmMappings"]
        except requests.RequestException as e:
            print(f"Error getting user roles: {e}")
            return []

    def assign_realm_roles(self, user_id, *role_names):
        token = self.get_admin_token()
        url = f"{self.base_url}/admin/realms/{self.realm}/users/{user_id}/role-mappings/realm"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # get all the realm roles
        all_roles = self.get_realm_roles(token)

        # Filter roles to assign
        roles_to_assign = [role for role in all_roles if role["name"] in role_names]

        response = requests.post(url, headers=headers, json=roles_to_assign)
        if response.status_code == 204:
            print(f"Successfully assigned realm roles: {role_names}")
        else:
            print(f"Error assigning roles: {response.text}")
