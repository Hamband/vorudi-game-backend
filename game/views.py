from django.http import JsonResponse
from rest_framework.decorators import api_view

from game.middlewares import is_logged_in
from game.models import Submission, Problem, Category, RewardCode, Team
from game.utils import check_and_add_solution, get_solutions


@api_view(["POST", "GET"])
def is_login(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'status': 'ok',
            'result': 'user',
            'user': request.user.to_dict()
        })
    return JsonResponse({
        'status': 'ok',
        'result': 'guest'
    })


# def do_login(request):
#     if 'username' not in request.data or 'password' not in request.data:
#         return JsonResponse({
#             'status': 'error',
#             'message': 'username/password is empty'
#         })
#
#     username = request.data['username']
#     password = request.data['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return JsonResponse({
#             'status': 'ok',
#             'message': 'با موفقیت وارد شدید!',
#         })
#     else:
#         return JsonResponse({
#             'status': 'error',
#             'message': 'نام کاربری یا رمزعبور غلط است!',
#         })


@api_view(["POST"])
@is_logged_in
def get_new_problem(request):
    if 'category' not in request.data:
        return JsonResponse({
            'status': 'error',
            'message': 'category is not present'
        })
    try:
        category = Category.objects.filter(pk=request.data['category']).get()
    except Category.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'category is not found'
        })
    user = request.user
    correct_solution = None
    if user.current_problem:
        correct_solution = get_solutions(user.current_problem)[0]
        user.skip_problem()

    touched_problems = set(Submission.objects.filter(user=user) \
                           .order_by('problem__id').values_list('problem__id', flat=True)
                           .distinct())
    new_problem = Problem.objects.exclude(id__in=touched_problems).filter(category=category) \
        .order_by('?').first()
    if new_problem:
        user.current_problem = new_problem
        user.save()
        return JsonResponse({
            'status': 'ok',
            'new_problem': new_problem.to_dict(),
            'correct_solution': correct_solution
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'سوال‌های این دسته تمام شدند!'
        })


@api_view(["POST"])
@is_logged_in
def make_new_try(request):
    if 'solution' not in request.data:
        return JsonResponse({
            'status': 'error',
            'message': 'solution is not present'
        })
    solution = request.data['solution']
    user = request.user
    if user.current_problem is None:
        return JsonResponse({
            'status': 'error',
            'message': 'user has no problem'
        })
    if Submission.objects.filter(problem=user.current_problem, user=user, solution=solution).count():
        return JsonResponse({
            'status': 'ok',
            'result': 'reject',
            'message': 'این پاسخ را قبلا ارسال کردید و غلط بود!'
        })
    if check_and_add_solution(user, solution):
        user.current_problem = None
        user.save()
        return JsonResponse({
            'status': 'ok',
            'result': 'accept'
        })
    return JsonResponse({
        'status': 'ok',
        'result': 'reject'
    })


@api_view(["POST"])
@is_logged_in
def check_reward_code(request):
    if 'code' not in request.data:
        return JsonResponse({
            'status': 'error',
            'message': 'code in not present'
        })

    reward_code = RewardCode.objects.filter(is_used=False, code=request.data['code']).first()
    if reward_code:
        reward_code.is_used = True
        reward_code.save()
        request.user.score += reward_code.points
        request.user.save()
        return JsonResponse({
            'status': 'ok',
            'message': '{} امتیاز به شما اصافه شد!'.format(reward_code.points)
        })
    return JsonResponse({
        'status': 'error',
        'message': 'متاسفانه کد وارد شده غلط است!'
    })


@api_view(["GET"])
@is_logged_in
def get_hint(request):
    if request.user.hint:
        return JsonResponse({
            'status': 'error',
            'message': 'شما برای این سوال راهنمایی گرفته‌اید.'
        })
    request.user.hint = True
    request.user.score += request.user.current_problem.category.hint_point
    request.user.save()
    return JsonResponse({
        'status': 'ok',
        'hint': request.user.current_problem.hint
    })


def scoreboard(request):
    teams = Team.objects.filter(is_superuser=False).order_by('-score').all()
    result_teams = []
    i = 0
    last_rank = 0
    last_score = 0
    for team in teams:
        i += 1
        if last_score != team.score:
            last_rank = i
        last_score = team.score
        result_teams.append({
            'rank': last_rank,
            'team_members': '، '.join(team.team_members.splitlines()),
            'score': team.score,
        })

    return JsonResponse({
        'status': 'ok',
        'teams': result_teams
    })


@api_view(["GET"])
def get_categories(request):
    categories = Category.objects.all()
    return JsonResponse({
        'status': 'ok',
        'categories': [category.to_dict() for category in categories]
    })
