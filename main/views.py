from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def sign_in(request):
    return  render(request, 'sign_in.html')