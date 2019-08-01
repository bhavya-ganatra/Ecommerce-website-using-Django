from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost
from math import ceil
# Create your views here.

def index(request):
    #return HttpResponse("You are in Blog")
    myposts = Blogpost.objects.all()
    return  render(request,'blog/index.html',{'myposts': myposts})

def blogpost(request,id):
    post = Blogpost.objects.filter(post_id = id)[0]
    print(post)
    return  render(request,'blog/blogpost.html',{'post':post,'previd':id-1,'nextid':id+1,'id':id,'length':len(Blogpost.objects.all())})