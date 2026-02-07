from django.urls import path, include

from users import views

urlpatterns =[
    path('', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('emailchange', views.emailchange, name='emailchange'),
    path('emailverify', views.emailverify, name='emailverify'),
    # path('delete', views.delete, name='delete'),
]