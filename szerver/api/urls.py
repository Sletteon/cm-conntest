from django.urls import path
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.BejegyzesekList.as_view()),
    path('het/<int:het>/', views.EHetiBejegyzesek.as_view()),
    path('delete/<int:pk>/', views.BejegyzesekTorlese.as_view()),
    path('motd', views.motd.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)