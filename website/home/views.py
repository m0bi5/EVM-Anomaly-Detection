from django.shortcuts import render,redirect
from main import run
# Create your views here.
def home(request):
    return render(request,'home.html',{})


def vote(request):
    return render(request,'vote.html',{})


def voted(request):
    r=run()
    if r[1]!=r[2]:
        return render(request,'voted.html',{'success':False,'voteRegisteredAs':r[2],'votedFor':r[1],'hash':r[0]['transactionHash'].hex()})
    else:
        return render(request,'voted.html',{'success':True,'hash':r[0]['transactionHash'].hex()})