from django.urls import path

from . import views
from .other import export_movies_to_xlsx


urlpatterns = [
    path("", views.index, name="index"),
    path("export", export_movies_to_xlsx, name='save_as_file')
]