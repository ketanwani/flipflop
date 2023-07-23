from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<rest_of_path>.*)$', views.reverse_proxy_view),
]
