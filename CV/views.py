# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import ListView

from .models import Cv, Formation, Company


class CvList(ListView):
    model = Cv
    context_object_name = "cv_list"


class CvView(generic.TemplateView):
    template_name = "CV/cv.html"

    def get_context_data(self, username):
        user = get_object_or_404(User, username=username)

        cv = get_object_or_404(Cv, user=user)
        formations = Formation.objects.filter(cv=cv).all()
        companies = Company.objects.filter(cv=cv).order_by('-begin').all()

        context = {
            "user": {'full_name': user.get_full_name()},
            "cv": cv,
            "formations": formations,
            "companies": companies,
        }
        return context
