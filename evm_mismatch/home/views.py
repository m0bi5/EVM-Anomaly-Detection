from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    if request.POST:
        context={'blockNumber':request.POST['blockNumber'],'transactionHash':request.POST['transactionHash']}        
        return render(request,'voted.html',context)
    else:
        return render(request,'home.html',{})