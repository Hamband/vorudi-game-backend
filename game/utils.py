from game.models import Submission


def fix_solution(solution):
    return solution


def get_solutions(problem):
    return problem.solutions.splitlines()


def check_and_add_solution(user, solution):
    problem = user.current_problem
    solution = fix_solution(solution)
    solutions = get_solutions(problem)
    accepted = False
    for correct_solution in solutions:
        correct_solution = fix_solution(correct_solution)
        if correct_solution == solution:
            accepted = True

    if accepted:
        user.score += problem.category.accept_point
    else:
        user.score += problem.category.reject_point
    user.save()
    submission = Submission()
    submission.problem = None
    submission.user = user
    submission.solution = solution
    submission.status = Submission.ACCEPTED_SUBMISSION if accepted else Submission.REJECTED_SUBMISSION
    submission.save()
