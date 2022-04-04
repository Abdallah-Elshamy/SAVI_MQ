from multiprocessing.dummy import Process
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .savi import launch_mq, list_mqs, delete_mq


def parse_config(form):
    config = dict()
    config["name"] = "mq-" + form["name"]
    config["key"] = form["key"]
    config["console_username"] = form["console_username"]
    config["console_password"] = form["console_password"]
    config["flavor"] = form["flavor"]
    config["image"] = form["mq_engine"]
    config["network"] = form["network"]
    return config


def dashboard(request):
    return render(request, "dashboard.html", {
        "instances": list_mqs()
    })


def create(request):
    if request.method == "POST":
        config = parse_config(request.POST)
        # Start a process to launch the mq and return to user
        p = Process(target=launch_mq, args=(config,))
        p.start()
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "createForm.html")


def delete(request, id):
    if request.method == "POST":
        delete_mq(id)
        return HttpResponseRedirect(reverse("dashboard"))

def status(request, id):
    return HttpResponse(f"Hello, {id}!")