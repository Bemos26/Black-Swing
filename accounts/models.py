from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    # We can add fields like is_member, is_student later if needed
    # For now, just inheriting allows us to extend it easily in the future
