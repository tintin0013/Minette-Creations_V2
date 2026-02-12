from django.db import models


# =========================
# USER PROFILE (Clerk bridge)
# =========================

class UserProfile(models.Model):
    """
    Stocke les informations internes liées à un user Clerk.
    Permet de différencier user normal et admin business.
    """

    clerk_user_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)

    # 🔥 AJOUTÉS
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        role = "ADMIN" if self.is_admin else "USER"
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return f"{full_name or self.clerk_user_id} ({role})"


# =========================
# CATEGORY
# =========================

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# RESOURCE
# =========================

class Resource(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="resources"
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ResourcePhoto(models.Model):
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(upload_to="resources/")
    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"Photo {self.id} for {self.resource.name}"


# =========================
# PRODUCT OPTIONS SYSTEM
# =========================

class ResourceOption(models.Model):
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="options"
    )

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.resource.name})"


class ResourceOptionValue(models.Model):
    option = models.ForeignKey(
        ResourceOption,
        on_delete=models.CASCADE,
        related_name="values"
    )

    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.value} ({self.option.name})"


# =========================
# RESERVATION SYSTEM
# =========================

class Reservation(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    # 🔥 On garde la cohérence avec UserProfile
    user_clerk_id = models.CharField(max_length=255, db_index=True)

    selected_options = models.ManyToManyField(
        ResourceOptionValue,
        related_name="reservations",
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reservation #{self.id} - {self.resource.name}"