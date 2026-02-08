from django.urls import path, include

from users import views

urlpatterns =[
    path('', views.profile, name='profile'),
    path('<str:username>/', views.user_profile, name='user_profile'),
    path('settings', views.settings, name='settings'),
    path('emailchange', views.emailchange, name='emailchange'),
    path('emailverify', views.emailverify, name='emailverify'),
]