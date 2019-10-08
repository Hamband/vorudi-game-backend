from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    name = models.CharField(max_length=30)
    accept_point = models.IntegerField()
    reject_point = models.IntegerField()
    skip_point = models.IntegerField()
    hint_point = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.pk,
            'name': self.name,
            'accept_point': self.accept_point,
            'reject_point': self.reject_point,
            'skip_point': self.skip_point,
            'hint_point': self.hint_point,
        }


class Problem(models.Model):
    class Meta:
        verbose_name = 'پرسش'
        verbose_name_plural = 'پرسش‌ها'

    statement = models.TextField()
    solutions = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    hint = models.TextField(default='')

    def __str__(self):
        return '{} (Solution: {})'.format(self.statement, self.solutions)

    def to_dict(self):
        return {
            'statement': self.statement,
            'category': self.category.to_dict()
        }


class Team(AbstractUser):
    class Meta:
        verbose_name = 'تیم'
        verbose_name_plural = 'تیم‌ها'

    team_members = models.TextField(default='')
    score = models.IntegerField(default=0)
    current_problem = models.ForeignKey(Problem, on_delete=models.CASCADE,
                                        null=True, blank=True)
    hint = models.BooleanField(default=False)

    def to_dict(self):
        return {
            'username': self.username,
            'team_members': self.team_members,
            'score': self.score,
            'current_problem': self.current_problem.to_dict() if self.current_problem else None,
            'hint': self.current_problem.hint if self.hint and self.current_problem else None,
        }

    def skip_problem(self):
        skip_submission = Submission()
        skip_submission.problem = self.current_problem
        skip_submission.user = self
        skip_submission.solution = None
        skip_submission.status = Submission.SKIPPED_SUBMISSION
        skip_submission.save()
        self.score += self.current_problem.category.skip_point
        self.current_problem = None
        self.hint = False
        self.save()


class Submission(models.Model):
    class Meta:
        verbose_name = 'تلاش'
        verbose_name_plural = 'تلاش‌ها'

    ACCEPTED_SUBMISSION = 1
    REJECTED_SUBMISSION = -1
    SKIPPED_SUBMISSION = -2
    STATUS_CHOICES = (
        (ACCEPTED_SUBMISSION, 'قبول'),
        (REJECTED_SUBMISSION, 'رد'),
        (SKIPPED_SUBMISSION, 'بیخیال'),
    )
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(Team, on_delete=models.CASCADE)
    solution = models.CharField(max_length=100, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return 'سوال:{} تیم:{} راه حل:{} وضعیت: {}'.format(self.problem, self.user, self.solution, self.status)


class RewardCode(models.Model):
    class Meta:
        verbose_name = 'کد جایزه'
        verbose_name_plural = 'کدهای جایزه'

    code = models.CharField(max_length=100)
    points = models.IntegerField()
    is_used = models.BooleanField()

    def __str__(self):
        return '{} ({})'.format(self.code, self.points)


class AdminSetting(models.Model):
    name = models.CharField(max_length=100)
    value = models.BooleanField()

    def __str__(self):
        return self.name
