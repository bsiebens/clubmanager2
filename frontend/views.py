from django.shortcuts import render
from django.views import View

from django.shortcuts import render


def index(request):
    return render(request, "test.html")


class IndexView(View):
    def get(self, request, *args, **kwargs):
        print("huh")
