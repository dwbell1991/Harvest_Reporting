from django.urls import path

from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('search', views.search, name='search'),
    path('results', views.results, name='results'),
]
