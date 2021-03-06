from multiprocessing.dummy import Process
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from savi_mq_engine import launch_mq, list_mqs, delete_mq, get_mq_info


def parse_config(form):
    config = dict()
    config["name"] = form["name"]
    config["key"] = form["key"]
    config["admin_username"] = form["admin_username"]
    config["admin_password"] = form["admin_password"]
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

def info(request, id):
    return JsonResponse(get_mq_info(id))