from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def mainpage(request):
    return HttpResponse("This is the AICollege API.")