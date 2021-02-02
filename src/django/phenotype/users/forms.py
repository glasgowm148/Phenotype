from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Document

User = get_user_model()


class DocumentForm(forms.UserChangeForm):
    class Meta:
        model = Document
        fields = ('document', "fileID",)


class UploadFileForm(forms.UserChangeForm):
    def upload(self):
        file = self.cleaned_data["file"]
        return file

class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User

class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
       # file = self.cleaned_data["file"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])
