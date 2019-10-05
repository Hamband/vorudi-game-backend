from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from game.middlewares import is_logged_in
from game.models import Submission, Problem, Category
from game.utils import check_and_add_solution, get_solutions


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


def do_login(request):
    if 'username' not in request.POST or 'password' not in request.POST:
        return JsonResponse({
            'status': 'error',
            'message': 'username/password is empty'
        })

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            'status': 'ok'
        })
    else:
        return JsonResponse({
            'status': 'error'
        })


@is_logged_in
def get_new_problem(request):
    if 'category' not in request.GET:
        return JsonResponse({
            'status': 'error',
            'message': 'category is not present'
        })
    try:
        category = Category.objects.filter(pk=request.GET['category']).get()
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
            'message': 'سوال‌ها تمام شدند!'
        })


@is_logged_in
def make_new_try(request):
    if 'solution' not in request.POST:
        return JsonResponse({
            'status': 'error',
            'message': 'solution is not present'
        })
    solution = request.POST['solution']
    user = request.user
    if user.current_problem is None:
        return JsonResponse({
            'status': 'error',
            'message': 'user has no problem'
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
