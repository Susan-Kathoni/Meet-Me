from django.urls import path
from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import  static
from .views  import *

urlpatterns=[
    path('', views.home, name="home-page"),
    path("home/", views.datePage, name="date-page"),
        
    #User URL Routes
    # path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile-page"),
    path("user/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("block/<int:pk>/", views.blockUser, name="block"),
    
    #Posts URL Routes
    path("like/<int:pk>/", views.likePost, name="like"),
    path("new-message/<str:username>",views.WriteMessage.as_view(), name="write-message"),
    path("view-messages/", views.ViewMessages, name="view-messages"),
    path("mark-read/<int:pk>", views.MarkAsRead, name="mark-read"),
    path("delete/<int:pk>", views.DeleteMessage.as_view(), name="delete-message")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)