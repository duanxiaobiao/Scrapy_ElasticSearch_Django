from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def result(request):
    return render(request,'result.html')


def login(request):
    return render(request,'login.html')


def register(request):
    return render(request,'register.html')





