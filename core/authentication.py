import requests
from jose import jwt
from rest_framework import authentication, exceptions

from .models import UserProfile


CLERK_JWKS_URL = "https://topical-lemming-46.clerk.accounts.dev/.well-known/jwks.json"


class ClerkUser:
    def __init__(self, payload, profile):
        self.payload = payload
        self.id = payload.get("sub")
        self.profile = profile
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
            # 1️⃣ Lire le header pour récupérer le KID
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            # 2️⃣ Récupérer les clés publiques Clerk
            jwks = requests.get(CLERK_JWKS_URL).json()

            key = None
            for jwk in jwks["keys"]:
                if jwk["kid"] == kid:
                    key = jwk
                    break

            if key is None:
                raise exceptions.AuthenticationFailed("Public key not found.")

            # 3️⃣ Décoder le token
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                options={"verify_aud": False},
            )

        except Exception:
            raise exceptions.AuthenticationFailed("Invalid token.")

        # 🔥 Données Clerk
        user_id = payload.get("sub")
        email = payload.get("email")
        first_name = payload.get("first_name")
        last_name = payload.get("last_name")

        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid Clerk token.")

        # 🔥 Création ou récupération du profil
        profile, created = UserProfile.objects.get_or_create(
            clerk_user_id=user_id,
            defaults={
                "email": email or f"{user_id}@placeholder.local",
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        # 🔥 Mise à jour automatique si les infos changent
        updated = False

        if email and profile.email != email:
            profile.email = email
            updated = True

        if first_name and profile.first_name != first_name:
            profile.first_name = first_name
            updated = True

        if last_name and profile.last_name != last_name:
            profile.last_name = last_name
            updated = True

        if updated:
            profile.save()

        user = ClerkUser(payload, profile)

        return (user, None)