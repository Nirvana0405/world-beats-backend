# myapp/urls.py
from django.urls import path
from .views import track_list

urlpatterns = [
    path('tracks/', track_list, name='track_list'),
]

# myapp/urls.py
from .views import add_track

urlpatterns = [
    path('add/', add_track, name='add_track'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('tracks/', views.track_list, name='track_list'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.track_list, name='track_list'),
]
