from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    categoriey = Catagory.objects.all()
    first_news = []
    for category in categoriey:
       category_first_post = News.objects.filter(category=category).order_by('-id').first()
       first_news.append(category_first_post)
    first_news = first_news[-5:]

    news = News.objects.all().order_by('-id')

    return render(request, 'index.html', {
        'categoriey': categoriey,
        'first_news': first_news,
        'news': news
    })
@login_required(login_url='login')
def category(request, pk):
    category = Catagory.objects.get(id=pk)
    news = News.objects.filter(category=category).order_by('-id')
    print(news)
    return render(request, 'category-01.html',{'news':news})

def new_detail(request, pk):
    post = News.objects.get(id=pk)
    return render(request, 'blog-detail-01.html', {'post':post})

@login_required(login_url = 'login')
def profile(resquest):
    user = User.objects.get(username=resquest.user.username)
    return render(resquest, 'profile.html', {'user':user})


