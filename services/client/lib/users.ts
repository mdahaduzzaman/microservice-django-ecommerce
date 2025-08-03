import axios from "axios";
import { getSession } from "./get-session";

export const getUserInfo = async () => {
  const session = await getSession();
  const response = await axios.get(
    `${process.env.AUTH_KEYCLOAK_ISSUER}/protocol/openid-connect/userinfo`,
    {
      headers: {
        Authorization: `Bearer ${session?.access_token}`,
      },
    }
  );

  return response.data;
};
