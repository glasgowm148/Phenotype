from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
import uuid

# Model forms perform validation, 
# automatically builds the absolute path for the upload, 
# treats filename conflicts and other common tasks.
class Document(models.Model):
    fileID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    document = models.FileField(upload_to='upload_vault/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
