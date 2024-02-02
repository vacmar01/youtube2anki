from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("generate/", views.generate, name="generate"), 
    path("videos/", views.VideoListView.as_view(), name="videos"),
    path("videos/<int:pk>/", views.VideoDetailView.as_view(), name="video"),
]