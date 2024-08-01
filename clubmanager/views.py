from django.shortcuts import render


def index(request):
    """Return site?"""
    return render(request, "base.html")
