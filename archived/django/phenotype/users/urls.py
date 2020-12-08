from django.urls import path
from . import views

from phenotype.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    user_upload_view
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~upload/", views.model_form_upload, name='upload'),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
