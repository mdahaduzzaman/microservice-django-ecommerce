import NextAuth from "next-auth";
import Keycloak from "next-auth/providers/keycloak";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [Keycloak],
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        // First-time login, save the `access_token`, its expiry and the `refresh_token`
        return {
          ...token,
          access_token: account.access_token,
          expires_at: account.expires_at,
          refresh_token: account.refresh_token,
        };
      } else if (Date.now() < Number(token.expires_at)) {
        // Subsequent logins, but the `access_token` is still valid
        return token;
      } else {
        // Subsequent logins, but the `access_token` has expired, try to refresh it
        if (!token.refresh_token || typeof token.refresh_token !== "string") {
          throw new Error("Missing or invalid refresh_token");
        }

        try {
          const response = await fetch(
            `${process.env.AUTH_KEYCLOAK_ISSUER}/protocol/openid-connect/token`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
              },
              body: new URLSearchParams({
                grant_type: "refresh_token",
                client_id: process.env.AUTH_KEYCLOAK_ID!,
                client_secret: process.env.AUTH_KEYCLOAK_SECRET!,
                refresh_token: token.refresh_token!,
              }),
            }
          );

          const refreshed = await response.json();

          if (!response.ok) {
            throw refreshed;
          }

          console.log("refreshed access_token", refreshed);

          return {
            ...token,
            access_token: refreshed.access_token,
            refresh_token: refreshed.refresh_token ?? token.refresh_token,
            expires_at: Date.now() + refreshed.expires_in * 1000,
          };
        } catch (error) {
          console.error("Error refreshing access_token", error);
          // If we fail to refresh the token, return an error so we can handle it on the page
          token.error = "RefreshTokenError";
          return token;
        }
      }
    },
    async session({ session, token }) {
      session.error = token.error as "RefreshTokenError" | undefined;
      session.access_token = token.access_token as string;
      return session;
    },
  },
});

declare module "next-auth" {
  interface Session {
    access_token: string;
    error?: "RefreshTokenError";
  }
}
