from django.shortcuts import render

def handler_404(request,exception):
    return render(request,"handlers/404.html")

def handler_500(request, *args, **kwarg):
    return render(request,"handlers/500.html")