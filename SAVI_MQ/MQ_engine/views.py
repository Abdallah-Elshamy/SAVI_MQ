from django.shortcuts import render
from django.http import HttpResponse

def dashboard(request):
    return HttpResponse("Hello, world!")


def create(request):
    return HttpResponse("Hello, world!")


def status(request, id):
    return HttpResponse(f"Hello, {id}!")