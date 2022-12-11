from django.urls import path
from . import views

urlpatterns=[
    path('',views.display,name="index"),
    path('get_recommendations',views.get_recommendations,name='get_recommendations')
]