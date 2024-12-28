from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path('holidays/<str:country>/<int:year>/',views.all_holidays,name="holidays"),
    path('holidays/search/', views.search_holiday, name='search_holiday'),
    ]