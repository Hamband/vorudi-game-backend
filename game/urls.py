from django.urls import path, include

from game.views import is_login, get_new_problem, make_new_try, check_reward_code, get_hint, scoreboard, \
    get_categories

urlpatterns = [
    path('auth/', include([
        # path('login', do_login),
        path('get', is_login),
    ])),
    path('problem/', include([
        path('new', get_new_problem),
        path('try', make_new_try),
        path('hint', get_hint),
        path('categories', get_categories)
    ])),
    path('reward_code', check_reward_code),
    path('scoreboard', scoreboard),
]
