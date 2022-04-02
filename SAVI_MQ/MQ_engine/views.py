from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

instances = [{
    "Name": "Test",
    "Endpoint": "1.1.1.1",
    "DashboardURL": "example.com",
    "Flavor": "m1.small",
    "KeyPair": "myKey",
    "Engine": "RabbitMQ",
    "Status": "Active",
},{
    "Name": "Test",
    "Endpoint": "1.1.1.1",
    "Flavor": "m1.small",
    "KeyPair": "myKey",
    "Engine": "Mosquitto",
    "Status": "Active",
}]

def parse_config(form):
    config = dict()
    config["name"] = form["name"]
    config["key"] = form["key"]
    config["console_username"] = form["console_username"]
    config["console_password"] = form["console_password"]
    config["flavor"] = form["flavor"]
    config["mq_engine"] = form["mq_engine"]
    return config


def dashboard(request):
    return render(request, "dashboard.html", {
        "instances": instances
    })


def create(request):
    if request.method == "POST":
        config = parse_config(request.POST)
        print(config)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "createForm.html")


def status(request, id):
    return HttpResponse(f"Hello, {id}!")