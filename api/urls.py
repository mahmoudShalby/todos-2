from django.urls import path
from . import views


urlpatterns = [
  path('all', views.all),
  path('new', views.new),
  path('delete', views.delete),
  path('edit', views.edit),
]
