from . import views
from django.urls import path
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.index, name='index'),
    path('results/<int:no>', cache_page(60 * 10)(views.results), name='results'),
]
