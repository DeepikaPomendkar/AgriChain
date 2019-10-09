
from django.urls import path,include
from predict import views

urlpatterns = [
    path('',views.home,name='home'),
    path('analyse/',views.analyse,name='analyse'),
    path('analyse/predict',views.predict,name='predict'),
]