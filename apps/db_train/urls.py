from django.urls import path
from .views import TrainView
app_name = 'train'

urlpatterns = [
    path('db/', TrainView.as_view(), name='index'),
]

