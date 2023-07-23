from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^admin/$', views.reverse_proxy_view),  # For /admin/
    re_path(r'^flipflop/admin/(?P<rest_of_path>.*)$', views.reverse_proxy_view),  # For /admin/ and its subpaths
]
