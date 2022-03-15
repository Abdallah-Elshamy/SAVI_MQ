from django.shortcuts import render
from django.http import HttpResponse

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

def dashboard(request):
    return render(request, "dashboard.html", {
        "instances": instances
    })


def create(request):
    return HttpResponse("Hello, world!")


def status(request, id):
    return HttpResponse(f"Hello, {id}!")