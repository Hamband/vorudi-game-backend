from django.urls import path, include

from game.views import do_login, is_login

urlpatterns = [
    path('auth/', include([
        path('login', do_login),
        path('check', is_login),
    ]))
]
