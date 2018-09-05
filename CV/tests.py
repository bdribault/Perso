from django.test import TestCase

from CV.models import Cv


def test():
    cv = Cv.objects.all()[0]
    print(cv)
    print(cv.skill_set)


test()
