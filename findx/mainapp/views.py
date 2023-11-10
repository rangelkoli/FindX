from django.shortcuts import render

# Create your views here.

def signup(request):
    
    if request.method =="POST":
        return render(request, "signup.html")


def home(request):
    return render(request, "index.html")

