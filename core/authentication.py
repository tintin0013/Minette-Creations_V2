import requests
from jose import jwt
from rest_framework import authentication, exceptions


CLERK_JWKS_URL = "https://topical-lemming-46.clerk.accounts.dev/.well-known/jwks.json"


class ClerkUser:
    def __init__(self, payload):
        self.payload = payload
        self.id = payload.get("sub")
        self.is_authenticated = True

    def __str__(self):
        return f"ClerkUser {self.id}"


class ClerkAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise exceptions.AuthenticationFailed("Invalid authorization header.")

        token = parts[1]

        try:
            jwks = requests.get(CLERK_JWKS_URL).json()

            payload = jwt.decode(
                token,
                jwks,
                algorithms=["RS256"],
                options={"verify_aud": False},
            )

        except Exception:
            raise exceptions.AuthenticationFailed("Invalid token.")

        user_id = payload.get("sub")

        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid Clerk token.")

        user = ClerkUser(payload)

        return (user, None)