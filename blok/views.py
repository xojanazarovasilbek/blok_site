from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    categoriey = Catagory.objects.all()
    return render(request, 'index.html', {'categoriey':categoriey})